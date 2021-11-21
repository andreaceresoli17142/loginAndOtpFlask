from os import error
from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
from logsyslib import LoginManager
import sys, threading, re

loginManager = LoginManager()

validateMailRegex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
validatePwRegex = re.compile(r'^[A-Za-z0-9@#$%^&+=]{8,}$')

#DONE: inserisci il limite di tempo in tokendata
#DONE: controlla input
#DONE: sostituisci le liste in logsyslib con i dizionari
#TODO: css e styling

app = Flask(__name__)

@app.route('/', methods=['GET'])
def mainPath():
    return render_template('index.html')
    # error = request.args.get("er")
    # print("testing output", file=sys.stdout)

@app.route('/login', methods=['POST'])
def loginPath():
    if request.form['email'] == None or request.form['password'] == None :
        error = ' please insert email and password.'
        return render_template('index.html', error=error)
    print("looking for user", file=sys.stdout)
    if loginManager.login(request.form['email'].lower(), request.form['password']):
        x = threading.Thread(target=loginManager.requestOtp, args=( request.form['email'], ), daemon=True )
        x.start()
        print("redirecting to otp", file=sys.stdout)
        return render_template('verifyOtp.html', otpEmail=request.form['email'])

    error = ' incorrect login info.'
    return render_template('index.html', error=error)

@app.route('/otp', methods=['POST'])
def verifyWithOtpPath():
    if request.form['otpToken'] == None :
        error = ' otp token invalid.'
        return render_template('index.html', error=error)

    if loginManager.verifyOtp(request.form['email'], request.form['otpToken']):
        return render_template('secureArea.html')

    error = ' otp token is invalid or has expired.'
    return render_template('index.html', error=error)

@app.route('/signUp', methods=['GET', 'POST'])
def signUpPath():
    if request.method == 'POST':
        if request.form['email'] == None or request.form['password'] == None or request.form['user'] == None:
            error = ' please insert email, password and username'
            return render_template('signUp.html', error=error)

        if not re.fullmatch(validateMailRegex, request.form['email']):
            error = ' invalid email.'
            return render_template('signUp.html', error=error)

        if not re.fullmatch(validatePwRegex, request.form['password']):
            error = ' invalid password.'
            return render_template('signUp.html', error=error)

        if loginManager.addUser(request.form['user'], request.form['email'], request.form['password']):
            return render_template('index.html')
        error = ' username or email is already used'
        return render_template('signUp.html', error=error)
    return render_template('signUp.html')


if __name__ == "__main__":
    app.run(debug=True)