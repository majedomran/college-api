import flask
from flask import request, jsonify
import requests
from bs4 import BeautifulSoup
import html5lib

app = flask.Flask(__name__)
app.config["DEBUG"] = True

data = {
    'loginForm:userType': '1',
    'loginForm': 'loginForm',
    'loginForm:_idcl': 'loginForm:loginUsersLink'
}
headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'Origin': 'https://edugate.ksu.edu.sa',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Referer': 'https://edugate.ksu.edu.sa/ksu/ui/home.faces',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8,ar;q=0.7',
}
url = 'https://edugate.ksu.edu.sa/ksu/init'

@app.route('/api/college', methods=['POST'])
def college_scrape():
        
        s = requests.session()
        r = s.get(url)
        soup = BeautifulSoup(r.content, 'html5lib')
        data['com.sun.faces.VIEW'] = soup.find(
            'input', attrs={'name': 'com.sun.faces.VIEW'})['value']
        data['loginForm:username'] =request.form['loginForm:username'] 
        data['loginForm:password'] =request.form['loginForm:password'] 
        r = s.post(url, data=data)
        page = s.get(
            'https://edugate.ksu.edu.sa/ksu/ui/student/student_transcript/index/studentTranscriptAllIndex.faces')
        return page.text


app.run()
