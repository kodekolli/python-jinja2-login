from flask import Flask, flash, redirect, render_template, request, session, abort
import os, socket
from flask_mysqldb import MySQL

app = Flask(__name__)

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return "Hello Boss!  <a href='/logout'>Logout</a>"

@app.route('/login', methods=['POST'])
def do_admin_login():
    fname = request.form['username']
    if request.form['password'] == 'password':
        session['logged_in'] = True
        print('Login success')
        return render_template('index.html', name=fname)
    else:
        print('wrong password!')
        return home()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

@app.route('/result',methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form

        app.config['MYSQL_HOST'] = 'wordpress-mysql'
        app.config['MYSQL_USER'] = 'root'
        app.config['MYSQL_PASSWORD'] = 'welcome'
        app.config['MYSQL_DB'] = 'mysql'

        mysql = MySQL(app)
        # Creating a connection cursor
        cursor = mysql.connection.cursor()

        cursor.execute("SHOW TABLES")
        for x in cursor:
            cursor.execute("CREATE TABLE students(curname VARCHAR(255), duration VARCHAR(255), interested VARCHAR(255))")

        if request.method == "POST":
            details = request.form
            curName = details['Course Name']
            Duration = details['Duration']
            interested = details['Interested']
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO students(curname, duration, interested) VALUES (%s, %s, %s)",(curName, Duration, interested))
            mysql.connection.commit()
            cur.close()
            return 'success'
        return render_template("result.html",result = result)

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)

    app.run(host_ip,'4000',debug=True)
