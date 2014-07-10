#!/usr/bin/python
from flask import Flask, render_template, request, Response
from datetime import datetime
import csv

LOG_FILE = "./issue.log"

app = Flask('wifi')

@app.route('/')
def index():
    return render_template('map.html')

@app.route('/report', methods = ['POST'])
def report():
    if request.method != 'POST':
        index();

    m = request.form
    x = m['x'].replace(',', '')
    y = m['y'].replace(',', '')
    name = m['name'].replace(',', '')
    email = m['email'].replace(',', '')
    issue = m['issue'].replace(',', '')
    if name == "" or email == "" or issue == "":
        return "You're missing a field!"
    s = "%s,%d,%d,%s,%s,%s\n" % (datetime.utcnow(), int(x), int(y), name, email, issue)
    with open(LOG_FILE, "a") as f:
        print("Writing to %s: %s" % (LOG_FILE, s))
        f.write(s)

    return render_template('thanks.html', name=name)

def check_auth(username, password):
    return username == 'admin' and password == 'secret'

@app.route('/admin')
def admin():
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return Response('Could not verify your access level for that URL.\n'
                        'You have to login with proper credentials', 401,
                        {'WWW-Authenticate': 'Basic realm="Login Required"'})

    cf = open(LOG_FILE, 'rb')
    rs = csv.reader(cf)
        #for r in rs:
            #t = "%s\n%s\n%s\n%s" % (r[3], r[4], r[5], r[0])
            #problems = problems + '<circle title="%s" cx="%s" cy="%s" r=20 fill="red" />\n' % (t, r[1], r[2])

    return render_template('map_admin.html', problems=rs)
    
if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 3000)

