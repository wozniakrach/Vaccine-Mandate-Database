from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_wozniakr'
app.config['MYSQL_PASSWORD'] = '5824'
app.config['MYSQL_DB'] = 'cs340_wozniakr'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)


# Routes
@app.route('/')
def root():
    #query = "SELECT * FROM diagnostic;"
    #cur = mysql.connection.cursor()
    #cur.execute(query)
    #results = cur.fetchall()
    #return results[0]
    return render_template("home.html")

@app.route('/employees', methods=["POST", "GET"])
def employees():
    if request.method == "POST":
        if request.form.get("employee-submit"):
            fname = request.form["fname"]
            lname = request.form["lname"]
            birthdate = request.form["birthdate"]
            termed = request.form["termed"]
            site = request.form["site"]
            exemption = request.form["exemption"]
            if exemption == "N/A":
                exemption = None
            insert_query = "INSERT INTO Employees (first_name, last_name, birthdate, termed, site_id, exemption_id) VALUES (%s, %s, %s, %s, %s, %s)" % (fname, lname, birthdate, termed, site, exemption)
            print(insert_query)
    select_query = "SELECT * FROM Employees;"
    cursor = mysql.connection.cursor()
    cursor.execute(select_query)
    data = cursor.fetchall()
    return render_template("employees.j2", employees_table=data)

@app.route('/worksites')
def worksites():
    return render_template("worksites.html")

@app.route('/exemptions')
def exemptions():
    return render_template("exemptions.html")

@app.route('/vaccines')
def vaccines():
    return render_template("vaccines.html")

@app.route('/employees_vaccines')
def employees_vaccines():
    return render_template("employees_vaccines.html")


# Listener
if __name__ == "__main__":

    #Start the app on port 3000, it will be different once hosted
    app.run(port=32999, debug=True)
