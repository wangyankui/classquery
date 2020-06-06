from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import datetime
from test import *
app = Flask(__name__)


@app.route('/')
def loginn():
    return render_template('login.html')



@app.route('/validate', methods=['POST'])
def validate():

    if request.method == 'POST':
        user=request.form['user']
        password = request.form['password']
        print(user)
        print(password)
        #调用数据库数据进行比对
        if(login(conn,user,password)):
            return redirect(url_for('index'))

    return redirect(url_for('login'))


@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/youke')
def youke():
    return render_template('youke.html')



@app.route('/query1')
def query1():
    return render_template('query1.html')

@app.route('/query2')
def query2():
    return render_template('query2.html')

@app.route('/yuyue')
def yuyue():
    return render_template('yuyue.html')

@app.route('/qxyy')
def qxyy():
    return render_template('qxyy.html')

@app.route('/change_state')
def change_state():
    return render_template('change_state.html')

@app.route('/tuijian')
def tuijian():
    return render_template('tuijian.html')

if __name__ == '__main__':
    app.run(debug=True)