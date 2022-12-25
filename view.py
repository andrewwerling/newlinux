from flask import Flask, request, redirect, render_template
import os
import json
import pymysql

app = Flask(__name__)

#--------------------------------------
# error occurs within this section
# comment it out to run the app
config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'Password123!',
    'database': 'demo'
}
# connection for MariaDB
connection = pymysql.connect(**config)
# create a connection cursor
cursor = connection.cursor()
#--------------------------------------

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# Create an Account page
@app.route('/create-account', methods=['GET', 'POST'])
def createAccount():
    if request.method == 'POST':
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        email = request.form['email']
        password = request.form['password']
        confirmPassword = request.form['confirmPassword']

        if password != confirmPassword:
            return 'Password does not match'
        else:
            with connection:
                sql = 'INSERT INTO users (username, password) VALUES (%s, %s)'
                cursor.execute(sql, (firstName, lastName, email, password))
                cursor.commit()

        return thankYou()
    return render_template('create-account.html')

# Login to Account page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']        

        with connection:
            sql = 'SELECT * FROM users WHERE username = %s AND password = %s'
            cursor.execute(sql, (email, password))
            result = cursor.fetchone()

            if result:
                return 'Logged in successfully'
            else:
                return 'Incorrect login details'
    return render_template('login.html')

# Thank You page
@app.route('/thank-you')
def thankYou():
    return render_template('thank-you.html')

# Contact page
@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=True, host='localhost', port=port)
