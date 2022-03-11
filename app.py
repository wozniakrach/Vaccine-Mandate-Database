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
    return render_template("home.j2")


@app.route('/employees', methods=["POST", "GET"])
def employees():
    # Insert a person into the Employees table
    if request.method == "POST":
        if request.form.get("employee-submit"):
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            birthdate = request.form["birthdate"]
            termed = request.form["termed"]
            site_id = request.form["site_id"]
            exemption_id = request.form["exemption_id"]

            # Account for null exemption_id
            if exemption_id == "-1":
                query = "INSERT INTO Employees (first_name, last_name, birthdate, termed, site_id) VALUES (%s, %s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (first_name, last_name, birthdate, termed, site_id))
                mysql.connection.commit()

            # If there are no null inputs
            else:
                query = "INSERT INTO Employees (first_name, last_name, birthdate, termed, site_id, exemption_id) VALUES (%s, %s, %s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (first_name, last_name, birthdate, termed, site_id, exemption_id))
                mysql.connection.commit()
                
            # redirect back to Employees page
            return redirect("/employees")

    # Display Employees table
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


@app.route('/worksites', methods=["POST", "GET"])
def worksites():
     # Insert a worksite into the Worksites table
    if request.method == "POST":
        if request.form.get("worksite-submit"):
            location = request.form["location"]
            department = request.form["department"]
            manager_first = request.form["manager_first"]
            manager_last = request.form["manager_last"]

            # No null inputs allowed
            query = "INSERT INTO Worksites (location, department, manager_first, manager_last) VALUES (%s, %s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (location, department, manager_first, manager_last))
            mysql.connection.commit()

        # Redirect back to Worksites page
        return redirect("/worksites")

    # Display Worksites table
    if request.method == "GET":
        select_query = "SELECT * FROM Worksites;"
        cursor = mysql.connection.cursor()
        cursor.execute(select_query)
        data = cursor.fetchall()
        return render_template("worksites.j2", worksites_table=data)


@app.route('/exemptions', methods=["POST", "GET"])
def exemptions():
    # Insert an exemption into the Exemptions table
    if request.method == "POST":
        if request.form.get("exemption-submit"):
            exemption_status = request.form["exemption_status"]
            exemption_type = request.form["exemption_type"]

            # Account for null exemption_type
            if not exemption_type:
                query = "INSERT INTO Exemptions (exemption_status) VALUES (%s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (exemption_status))
                mysql.connection.commit()

            # No null inputs
            else:
                query = "INSERT INTO Exemptions (exemption_status, exemption_type) VALUES (%s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (exemption_status, exemption_type))
                mysql.connection.commit()

            # redirect back to Exemptions page
            return redirect("/exemptions")

    # Display Exemptions table
    select_query = "SELECT * FROM Exemptions;"
    cursor = mysql.connection.cursor()
    cursor.execute(select_query)
    data = cursor.fetchall()
    return render_template("exemptions.j2", exemptions_table=data)


@app.route('/vaccines', methods=["POST", "GET"])
def vaccines():
    # Insert a vaccine into the Vaccines table
    if request.method == "POST":
        if request.form.get("vaccine-submit"):
            vaccine_manufacturer = request.form["vaccine_manufacturer"]

            # No null inputs allowed
            query = "INSERT INTO Vaccines (vaccine_manufacturer) VALUES (%s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (vaccine_manufacturer))
            mysql.connection.commit()

        # Redirect back to Vaccines page
        return redirect("/vaccines")

    select_query = "SELECT * FROM Vaccines;"
    cursor = mysql.connection.cursor()
    cursor.execute(select_query)
    data = cursor.fetchall()
    return render_template("vaccines.j2", vaccines_table=data)


@app.route('/employees_vaccines', methods=["POST", "GET"])
def employees_vaccines():
    # Insert record of vaccines given to employees in the Employees_Vaccines table
    if request.method == "POST":
        if request.form.get("emp_vacc-submit"):
            employee_id = request.form["employee_id"]
            vaccine_id = request.form["vaccine_id"]
            date_administered = request.form["date_administered"]
            dose = request.form["dose"]

            # No null inputs allowed
            query = "INSERT INTO Employees_Vaccines (employee_id, vaccine_id, date_administered, dose) VALUES (%s, %s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (employee_id, vaccine_id, date_administered, dose))
            mysql.connection.commit()

            # Redirect back to Employees_Vaccines page
            return redirect("/employees_vaccines")

        # Display filtered results if search was made
        elif request.form.get("search-submit"):
            employee_id = request.form["employee_id"]
            search_query = "SELECT * FROM Employees_Vaccines WHERE employee_id = %s;"
            cursor = mysql.connection.cursor()
            cursor.execute(search_query, employee_id)
            results = cursor.fetchall()
            employee_query = "SELECT employee_id FROM Employees;"
            cursor.execute(employee_query)
            employee_options = cursor.fetchall()
            vaccine_query = "SELECT vaccine_id FROM Vaccines;"
            cursor.execute(vaccine_query)
            vaccine_options = cursor.fetchall()
            search_query = "SELECT DISTINCT employee_id FROM Employees_Vaccines;"
            cursor.execute(search_query)
            search_options = cursor.fetchall()
            return render_template("employees_vaccines.j2", table_data=results, employee_options=employee_options, vaccine_options=vaccine_options, search_options=search_options)
    else:
        # Display Employees_Vaccines table
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
        search_query = "SELECT DISTINCT employee_id FROM Employees_Vaccines;"
        cursor.execute(search_query)
        search_options = cursor.fetchall()
        return render_template("employees_vaccines.j2", table_data=data, employee_options=employee_options, vaccine_options=vaccine_options, search_options=search_options)


# Listener
if __name__ == "__main__":
    # Start the app on port 3000, it will be different once hosted
    app.run(port=32999, debug=True)
