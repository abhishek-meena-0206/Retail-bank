from flask import Blueprint
from flask import Flask, render_template, session,request,redirect, url_for
from flask_mysqldb import MySQL
from flask_login import  login_required, logout_user

routeapp= Flask(__name__)

mysql=MySQL(routeapp)

route = Blueprint('app1', __name__)

@route.route('/base.html')
def base():
    return render_template('base.html')

@route.route('/')
def myname():
	return render_template('loginl.html')
@route.route('/create.html')
def fun():
	if 'username' in session:
	    return render_template('create.html')
	else:
	    return render_template('login.html')    

@route.route('/status.html')
def status():
    if 'username' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * from customerinfo")
        rows = cur.fetchall()
        mysql.connection.commit()
        cur.close()
        return render_template('status.html', name=rows)
    else:
        return redirect('/')    

@route.route('/logout.html')
def logout():
	session.pop('username',None)
	return redirect('/')


@route.route('/login.html', methods=['GET', 'POST'])
def login():

    

    if request.method=='POST':
         username=request.form['username']
         password=request.form['password']
         

         cur = mysql.connection.cursor()
         cur.execute("SELECT * from executive where username=%s and password=%s",(username,password))
         mysql.connection.commit()
         account=cur.fetchall()
        
         if account:
             session['loggedin'] = True
             
             session['username'] = username
            
             return redirect('base.html') 
                
             
         else:
             return ("wrong password or username")
    else:
    	
    	return ("fuck")