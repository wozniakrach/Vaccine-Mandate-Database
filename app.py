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
    # query = "SELECT * FROM diagnostic;"
    # cur = mysql.connection.cursor()
    # cur.execute(query)
    # results = cur.fetchall()
    # return results[0]
    return render_template("home.j2")


@app.route('/employees', methods=["POST", "GET"])
def employees():
    # Insert a person into the Employees table
    if request.method == "POST":
        # If user presses the Add Employee button
        if request.form.get("employee-submit"):
            first_name = request.form["fname"]
            last_name = request.form["lname"]
            birthdate = request.form["birthdate"]
            termed = request.form["termed"]
            site_id = request.form["site"]
            exemption_id = request.form["exemption"]

            # Account for null exemption_id
            if exemption_id == "N/A":
                query = "INSERT INTO Employees (first_name, last_name, birthdate, termed, site_id) " \
                        "VALUES (%s, %s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (first_name, last_name, birthdate, termed, site_id))
                mysql.connection.commit()

            # No null inputs
            else:
                query = "INSERT INTO Employees (first_name, last_name, birthdate, termed, site_id, exemption_id) " \
                        "VALUES (%s, %s, %s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (first_name, last_name, birthdate, termed, site_id, exemption_id))
                mysql.connection.commit()

            # redirect back to people page
            return redirect("/Employees")

    # Separate out the request methods, in this case this is for a GET
    # Grab Employees data so we can send it to our template to display
    if request.method == "GET":
        select_query = "SELECT * FROM Employees;"
        cursor = mysql.connection.cursor()
        cursor.execute(select_query)
        data = cursor.fetchall()
        site_query = "SELECT site_id FROM Worksites;"
        cursor.execute(site_query)
        site_options = cursor.fetchall()
        exemption_query = "SELECT exemption_id FROM Exemptions;"
        cursor.execute(exemption_query)
        exemption_options = cursor.fetchall()
        return render_template("employees.j2", employees_table=data, site_options=site_options, exemption_options=exemption_options)


@app.route('/worksites')
def worksites():
    select_query = "SELECT * FROM Worksites;"
    cursor = mysql.connection.cursor()
    cursor.execute(select_query)
    data = cursor.fetchall()
    return render_template("worksites.j2", worksites_table=data)


@app.route('/exemptions')
def exemptions():
    select_query = "SELECT * FROM Exemptions;"
    cursor = mysql.connection.cursor()
    cursor.execute(select_query)
    data = cursor.fetchall()
    return render_template("exemptions.j2", exemptions_table=data)


@app.route('/vaccines')
def vaccines():
    select_query = "SELECT * FROM Vaccines;"
    cursor = mysql.connection.cursor()
    cursor.execute(select_query)
    data = cursor.fetchall()
    return render_template("vaccines.j2", vaccines_table=data)


@app.route('/employees_vaccines')
def employees_vaccines():
    select_query = "SELECT * FROM Employees_Vaccines;"
    cursor = mysql.connection.cursor()
    cursor.execute(select_query)
    data = cursor.fetchall()
    employee_query = "SELECT employee_id FROM Employees;"
    cursor.execute(employee_query)
    employee_options = cursor.fetchall()
    vaccine_query = "SELECT vaccine_id FROM Vaccines;"
    cursor.execute(vaccine_query)
    vaccine_options = cursor.fetchall()
    return render_template("employees_vaccines.j2", table_data=data, employee_options=employee_options, vaccine_options=vaccine_options)


# Listener
if __name__ == "__main__":
    # Start the app on port 3000, it will be different once hosted
    app.run(port=32999, debug=True)
