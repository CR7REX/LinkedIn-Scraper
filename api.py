import flask,json
from flask import jsonify
from Linkedin_Scraper import scrape
server = flask.Flask(__name__)
url = "https://www.linkedin.com/in/qishi-xing-0739b21a9/"

@server.route('/HireBeat',methods=['post'])
def test():
    return jsonify(scrape(url))

if __name__== '__main__':
    server.run(debug=True,port = 8888,host='0.0.0.0')