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
    # print(bodyDict)
def extractName(page):
    soup = BeautifulSoup(page.content,'html5lib')
    tables = soup.findAll('table')[19]
    tableData = str(tables).split('td')[3]
    tableData = str(tableData).split('studNameText')[1]
    tableData = str(tableData).split('>')[1]
    tableData = str(tableData).split('<')[0]
    # soup = soup.find('td')
    return tableData
def extractCollege(page):
    soup = BeautifulSoup(page.content,'html5lib')
    tables = soup.findAll('table')[19]
    tableData = str(tables).split('td')[9]
    tableData = str(tableData).split('facNameText')[1]
    tableData = str(tableData).split('>')[1]
    tableData = str(tableData).split('<')[0]
    return tableData
def extractMajor(page):
    soup = BeautifulSoup(page.content,'html5lib')
    tables = soup.findAll('table')[19]
    tableData = str(tables).split('td')[19]
    tableData = str(tableData).split('majorName')[1]
    tableData = str(tableData).split('>')[1]
    tableData = str(tableData).split('<')[0]
    return tableData
def extractStuNumber(page):
    soup = BeautifulSoup(page.content,'html5lib')
    tables = soup.findAll('table')[19]
    tableData = str(tables).split('td')[13]
    tableData = str(tableData).split('studNo')[1]
    tableData = str(tableData).split('>')[1]
    tableData = str(tableData).split('<')[0]
    return tableData
def extractCurrentTerm(page):
    soup = BeautifulSoup(page.content,'html5lib') 
    tables = soup.findAll('form')[2]
    tableData = str(tables).split('<li>')[2]
    tableData = str(tableData).split('</li>')[0]
    currentTerm = str(tableData).split(' ')[17] + ' '+ str(tableData).split(' ')[18] +' '+str(tableData).split(' ')[19]
    return currentTerm
def extractMail(page):
    soup = BeautifulSoup(page.content,'html5lib') 
    tables = soup.findAll('form')[2]
    tableData = str(tables).split('<li>')[6]
    tableData = str(tableData).split('</li>')[0]
    current = str(tableData).split(' ')[17]
    return current
def extractWarnings(page):
    soup = BeautifulSoup(page.content,'html5lib') 
    tables = soup.findAll('form')[2]
    tableData = str(tables).split('<li>')[5]
    tableData = str(tableData).split('</li>')[0]
    current = str(tableData).split(' ')[17]
    current = str(current).split('\n')[0]
    return current
def extractCurrrentGDP(page):
    soup = BeautifulSoup(page.content,'html5lib') 
    tables = soup.findAll('form')[2]
    tableData = str(tables).split('<li>')[4]
    tableData = str(tableData).split('</li>')[0]
    current = str(tableData).split(' ')[17]
    return current
@app.route('/', methods=['POST'])
def index():
    s = requests.session()
    r = s.get('https://edugate.ksu.edu.sa/ksu/init')
    soup = BeautifulSoup(r.content, 'html5lib')
    data['com.sun.faces.VIEW'] = soup.find(
        'input', attrs={'name': 'com.sun.faces.VIEW'})['value']
    data['loginForm:username'] = request.form['loginForm:username']
    data['loginForm:password'] = request.form['loginForm:password']
    r = s.post(url, data=data,headers=headers)
    page = s.get(
        'https://edugate.ksu.edu.sa/ksu/ui/student/student_transcript/index/studentTranscriptAllIndex.faces')
    soup = BeautifulSoup(page.content, 'html5lib')
    print(request.form['loginForm:username'])
    print(request.form['loginForm:password'])
    
    bodyDict = {}
    tables = soup.findAll('table')
    
    personlPage = s.get('https://edugate.ksu.edu.sa/ksu/ui/student/homeIndex.faces')
    i = 28 
    term = 0
    while i < len(tables) - 6:
        bodyDict['term'+str(term)] = {extractYear(soup,i): extractData(soup,i+3)}
        i = i + 8 
        term = term +1
    i = 0
    finalDict = {}
    finalDict['data'] = bodyDict
    finalDict['name'] = extractName(s.get('https://edugate.ksu.edu.sa/ksu/ui/student/homeIndex.faces'))
    finalDict['college'] = extractCollege(personlPage)
    finalDict['major'] = extractMajor(personlPage)
    finalDict['stdNumber'] = extractStuNumber(personlPage)
    finalDict['currentTerm'] = extractCurrentTerm(personlPage)
    finalDict['warnings'] = extractWarnings(personlPage)
    finalDict['email'] = extractMail(personlPage)
    finalDict['gdp'] = extractCurrrentGDP(personlPage)
    # print(finalDict['data'])
    if finalDict['data']:
        finalDict['login'] = 'true'
    else:
        finalDict['login'] = 'false'    
    
    
    # print(finalDict)
  
    return finalDict



if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000, )
