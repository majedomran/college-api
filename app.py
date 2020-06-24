# app.py
from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import html5lib
# import pandas as pd

app = Flask(__name__)
app.debug = True


@app.route('/post/', methods=['POST'])
def post_something():
    param = request.form.get('name')
    print(param)
    # You can add the test cases you made in the previous function, but in our case here you are just testing the POST functionality
    if param:
        return jsonify({
            "Message": f"Welcome {name} to our awesome platform!!",
            # Add this option to distinct the POST request
            "METHOD": "POST"
        })
    else:
        return jsonify({
            "ERROR": "no name found, please send a name."
        })


# A welcome message to test our server
data = {
    'loginForm:userType': '1',
    'loginForm': 'loginForm',
    'loginForm:_idcl': 'loginForm:loginUsersLink'
}
body = []
url = 'https://edugate.ksu.edu.sa/ksu/init'

def extractYear(soup,index):
    testRow =  soup.findAll('table')[index].find_all('span')
    te =  str(testRow).split('>')[1]
    te = str(te).split('<')[0]
    te = str(te).split('\xa0')[0]
    return te
def extractData(soup,index):
    bodyDict = {}
    table = soup.findAll('table')[index]
    row_marker = 0
    coursIndex = 0
    for row in table.find_all('tr'):
        column_marker = 0
        columns = row.find_all('td')
        coursIndex = coursIndex+1
        for column in columns:
            if(column_marker == 0 and coursIndex != 0):
                bodyDict['course'+str(coursIndex - 2)] = {'number': column.get_text()}
            if(column_marker == 1):
                bodyDict['course'+str(coursIndex - 2)]['name'] = column.get_text()
            if(column_marker == 2):
                bodyDict['course'+str(coursIndex - 2)]['hours'] = column.get_text()
            if(column_marker == 3):
                bodyDict['course'+str(coursIndex - 2)]['points'] = column.get_text()
            if(column_marker == 4):
                bodyDict['course'+str(coursIndex - 2)]['grade'] = column.get_text()
            column_marker += 1
    return bodyDict
    print(bodyDict)
def loginAuth(username,password):
    s = requests.session()
    r = s.get(url)
    soup = BeautifulSoup(r.content, 'html5lib')
    data['com.sun.faces.VIEW'] = soup.find(
        'input', attrs={'name': 'com.sun.faces.VIEW'})['value']
    data['loginForm:username'] = username
    data['loginForm:password'] = password
    r = s.post(url, data=data)
    page = s.get(
        'https://edugate.ksu.edu.sa/ksu/ui/student/student_transcript/index/studentTranscriptAllIndex.faces')
    soup = BeautifulSoup(page.content, 'html5lib')
    return soup
@app.route('/', methods=['POST'])
def index():
    # 28 31 start here
    # 39
    # 47
    # 55
    # 63
    # delta 8
    
    bodyDict = {}
    soup = loginAuth(request.form['loginForm:username'],request.form['loginForm:password'])
    tables = soup.findAll('table')
    # bodyDict[extractYear(soup,28)] = extractData(soup,31)
    # print(extractYear(soup,28))
    i = 28 
    while i < len(tables) - 2:
        bodyDict[extractYear(soup,i)] = extractData(soup,i+3)
        i = i + 8 
        print(i )
        print('////')
    
    
    print(bodyDict)

    # print(extractYear(soup,60))
    # print(extractData(soup,63))
    
    
    
    
  
    return bodyDict



if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000, debug=True)
