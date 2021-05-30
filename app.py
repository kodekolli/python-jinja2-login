from flask import Flask, flash, redirect, render_template, request, session, abort
import os, socket
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = os.getenv("MYSQL_HOST")
app.config['MYSQL_USER'] = os.getenv("MYSQL_USER")
app.config['MYSQL_PASSWORD'] = os.getenv("MYSQL_PASSWORD")
app.config['MYSQL_DB'] = os.getenv("MYSQL_DB")
mysql = MySQL(app)


@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return "Hello Boss!  <a href='/logout'>Logout</a>"

@app.route('/login', methods=['POST'])
def do_admin_login():
    try:
        fname = request.form['username']
        fpwd = request.form['password']
        print(fpwd)
        cursor = mysql.connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS login(username VARCHAR(255), password VARCHAR(255))")
        chkuser = cursor.execute("select username from login where username='%s'" %(fname))
        if chkuser == 0:
            print("User does not exist,creating the user.")
            cursor.execute("INSERT INTO login (username, password) VALUES (%s, %s)",(fname, fpwd))
            mysql.connection.commit()
            return render_template('index.html', name=fname)
        else:
            print("User exist, Login with username & password")
            cursor.execute("select password from login where username='%s'" %(fname))
            mypwd = cursor.fetchall()
            for x in mypwd:
                db_pwd = (str(x).strip("(").strip(")").strip(",").strip("'"))
                if db_pwd == fpwd:
                    print("password matched")
                    return render_template('index.html', name=fname)
                else:
                    print('wrong password!')
                    return home()
    except Exception as e:
        print(e)

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

@app.route('/result',methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form

        # Creating a connection cursor
        cursor = mysql.connection.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS students(curname VARCHAR(255), duration VARCHAR(255), interested VARCHAR(255))")

        if request.method == "POST":
            details = request.form
            curName = details['Course Name']
            Duration = details['Duration']
            interested = details['Interested']
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO students(curname, duration, interested) VALUES (%s, %s, %s)",(curName, Duration, interested))
            mysql.connection.commit()
            cur.close()
        return render_template("result.html",result = result)

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)

    app.run(host_ip,'4000',debug=True)
