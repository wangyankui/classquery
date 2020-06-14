from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import datetime
from test import *
app = Flask(__name__)


@app.route('/')
def loginn():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register1', methods=['POST'])
def rejister1():

    if request.method == 'POST':
        type=request.form['type']
        password = request.form['password']
        id = request.form['id']
        name = request.form['name']
        re=zhuce(conn,type,id,name,password)
        if re==1:
            return redirect(url_for('loginn'))
        else:
            return redirect(url_for('register'))
        #print(user)
        #print(password)
        #调用数据库数据进行比对


@app.route('/validate', methods=['POST'])
def validate():

    if request.method == 'POST':
        user=request.form['user']
        password = request.form['password']
        #print(user)
        #print(password)
        #调用数据库数据进行比对
        if(login(conn,user,password)):
            return redirect(url_for('index'))

    return redirect(url_for('login'))


@app.route('/index')
def index():
    return render_template('index.html')

#查询有课
@app.route('/youke')
def youke():
    return render_template('youke.html')

#返回有课结果
@app.route('/isyouke', methods=['POST'])
def isyouke():

    if request.method == 'POST':
        classroom=request.form['classroom']
        week = request.form['week']
        week=int(week)
        hour = request.form['hour']
        hour=int(hour)
        #调用数据库数据进行比对
        you=issyouke(conn,classroom,week,hour)
        if(you!=0):
            you=list(you)
            course={}
            course['course1']=you[0]
            return render_template('youkejieguo.html',**course)
        else:
            return 'No Class'




@app.route('/query1')
def query1():
    return render_template('query1.html')

@app.route('/query2',methods=['POST'])
def query2():
    if request.method == 'POST':
        classroom=request.form['classroom']
        q=query(conn,classroom)
        return render_template('query2.html',q=q)

@app.route('/yuyue0')
def yuyue0():
    return render_template('yuyue.html')

@app.route('/yuyue1',methods=['POST'])
def yuyue1():
    if request.method == 'POST':
        room=request.form['roomNum']
        userID = request.form['userID']
        time = request.form['time']
        Num = request.form['Num']

        y=yuyue(conn,room,userID,time,Num)
        if y==1:
            return 'Failed appointment, class is in progress'
        elif y==2:
            return "Reservation failed, no seat available"
        elif y==3:
            return "Make an appointment success"
        elif y==4:
            return "The appointment failed and the classroom was occupied"
        elif y==5:
            return "Failed appointment, this classroom does not exist"


@app.route('/qxyy0')
def qxyy0():
    return render_template('qxyy.html')

@app.route('/qxyy1',methods=['POST'])
def qxyy1():
    if request.method == 'POST':
        room=request.form['roomNum']
        userID = request.form['userID']
        time = request.form['time']
        Num = request.form['Num']

        qy=qxyy(conn,userID,room,time,Num)
        return "Success to cancel"


@app.route('/change_state0')
def change_state0():
    return render_template('change_state.html')

@app.route('/change',methods=['POST'])
def change():
    if request.method == 'POST':
        room=request.form['roomNum']
        userID = request.form['userID']
        attri = request.form['attribute']
        va = request.form['value']

        ch=change_state(conn,userID,room,attri,va)
        if ch==1:
            return "Success to change"
        else:
            return "Sorry, you are not an administrator and cannot do this"

@app.route('/tuijian0')
def tuijian0():
    return render_template('tuijian.html')

@app.route('/tuijian1',methods=['POST'])
def tuijian1():
    if request.method == 'POST':
        loc = request.form['loc']
        size = request.form['size']
        electronic = request.form['electronic']
        manyMedia = request.form['manyMedia']
        wifi = request.form['wifi']
        airConditione = request.form['airConditione']

        ch=tuijian(conn,loc,size,electronic,manyMedia,wifi,airConditione)
        ch1=[list(ch[0]),list(ch[1])]
        ch2={}
        ch2['classrooms']=ch1
        return render_template('tuijianjieguo.html',**ch2)

if __name__ == '__main__':
    app.run(debug=True)