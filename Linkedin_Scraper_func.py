from selenium import webdriver
from bs4 import BeautifulSoup
import time
import sys

def scrape(url):
    # Creating a webdriver instance
    driver = webdriver.Chrome()
    
    # Opening linkedIn's login page
    driver.get("https://linkedin.com/uas/login")
    
    # waiting for the page to load
    time.sleep(2)
    
    # entering username
    username = driver.find_element_by_id("username")
    username.send_keys("xxx@xxx.com")  # Your linkedin email
    
    # entering password
    pword = driver.find_element_by_id("password")
    pword.send_keys("xxx")  # Your linkedin password        
    
    # Clicking on the log in button
    # Format (syntax) of writing XPath --> 
    # //tagname[@attribute='value']
    driver.find_element_by_xpath("//button[@type='submit']").click()
    time.sleep(2)

    driver.get(url)
    info = {'name':[], 'title':[], 'skills':[], 'experience':[]}
    src = driver.page_source  
    soup = BeautifulSoup(src, 'html.parser')
    intro = soup.find('div', {'class': 'pv-text-details__left-panel'})

    
    name_loc = intro.find("h1")
    # Extracting the Name
    name = name_loc.get_text().strip()
    # strip() is used to remove any extra blank spaces
    works_at_loc = intro.find("div", {'class': 'text-body-medium'})
    # this gives us the HTML of the tag in which the Company Name is present
    # Extracting the Company Name
    title = works_at_loc.get_text().strip()


    driver.get(driver.current_url + 'details/skills')
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    time.sleep(1)
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    time.sleep(1)
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    time.sleep(1)
    src = driver.page_source  
    soup = BeautifulSoup(src, 'html.parser')
    intro = soup.find_all('span', {'class': "mr1 hoverable-link-text t-bold"}) + soup.find_all('span', {'class': "mr1 t-bold"})
    skills = []
    for i in intro:
        skill = i.find('span', {'aria-hidden': 'true'}).get_text()
        if skill == 'Messaging' or not skill or skill in skills:
            continue
        skills.append(skill)

    driver.get(driver.current_url.replace("skills", "experience"))
    time.sleep(2)
    src = driver.page_source  
    soup = BeautifulSoup(src, 'html.parser')
    exps = soup.find_all('div',{'class': 'display-flex flex-column full-width align-self-center'})
    experience = []
    tmp = []
    for exp in exps:
        if exp.find('span', {'class': 'mr1 t-bold'}):
            if tmp:
                experience.append(tmp)
                tmp = []
            title = exp.find('span', {'class': 'mr1 t-bold'}).find('span', {'aria-hidden': 'true'}).get_text()
            company = exp.find('span', {'class': 't-14 t-normal'}).find('span', {'aria-hidden': 'true'}).get_text()
            time = exp.find('span', {'class': 't-14 t-normal t-black--light'}).find('span', {'aria-hidden': 'true'}).get_text()
            experience.append([title, company, time])
        if exp.find('span', {'class': 'mr1 hoverable-link-text t-bold'}):
            if exp.find('span', {'class': 't-14 t-normal'}):
                if tmp:
                    experience.append(tmp)
                tmp = []
                company = exp.find('span', {'class': 'mr1 hoverable-link-text t-bold'}).find('span', {'aria-hidden': 'true'}).get_text()
                time = exp.find('span', {'class': 't-14 t-normal'}).find('span', {'aria-hidden': 'true'}).get_text()
                tmp.append([company, time])
            else:
                title = exp.find('span', {'class': 'mr1 hoverable-link-text t-bold'}).find('span', {'aria-hidden': 'true'}).get_text()
                time = exp.find('span', {'class': 't-14 t-normal t-black--light'}).find('span', {'aria-hidden': 'true'}).get_text()
                tmp.append([title, time])
    if tmp:
        experience.append(tmp)
    driver.quit()
    info['name'] = name
    info['title'] = title
    info['experience'] = experience
    info['skills'] = skills
    return info