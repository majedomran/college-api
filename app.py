# app.py
from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import html5lib

app = Flask(__name__)


@app.route('/getmsg/', methods=['GET'])
def respond():
    # Retrieve the name from url parameter
    name = request.args.get("name", None)

    # For debugging
    print(f"got name {name}")

    response = {}

    # Check if user sent a name at all
    if not name:
        response["ERROR"] = "no name found, please send a name."
    # Check if the user entered a number not a name
    elif str(name).isdigit():
        response["ERROR"] = "name can't be numeric."
    # Now the user entered a valid name
    else:
        response["MESSAGE"] = f"Welcome {name} to our awesome platform!!"

    # Return the response in json format
    return jsonify(response)


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
  'loginForm:username': '439101835',
  'loginForm:password': '1113583775',
  'loginForm': 'loginForm',
  'loginForm:_idcl': 'loginForm:loginUsersLink'
}
url = 'https://edugate.ksu.edu.sa/ksu/init'

@app.route('/')
def index():
    s = requests.session()
    r = s.get(url)
    soup = BeautifulSoup(r.content, 'html5lib')
    data['com.sun.faces.VIEW'] = soup.find('input', attrs={'name': 'com.sun.faces.VIEW'})['value']

    r = s.post(url, data=data)
    page = s.get('https://edugate.ksu.edu.sa/ksu/ui/student/student_transcript/index/studentTranscriptAllIndex.faces')
  
    return page.text

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
