from flask import Flask, render_template, session,request,redirect, url_for
from flask_mysqldb import MySQL
from flask_login import  login_required, logout_user
from route import route




app = Flask(__name__)
app.register_blueprint(route)

app.config.from_object("model.con")

app.secret_key = "myweb"

mysql=MySQL(app)


@app.route('/<int:user>')
def status_detail(user):
    
    
    if 'username'  in session:
        cur = mysql.connection.cursor()
 
        cur.execute("SELECT * from customerinfo where ssn_id = %s",(user,))
        mysql.connection.commit()
        account=cur.fetchall()
        
        a=account
        return render_template('profile.html', p=a)
    else:
        return redirect('/')    
    






@app.route('/transfer.html')
def show_transfer():


    if 'username'  in session:
        return render_template('transfer.html') 
    else:
        return redirect('/')   	
        	   

            	
@app.route('/send_money',methods=['GET', 'POST'])
def send_money():
    if request.method == "POST":
        d=request.form
        i_d=d['id']
        target=d['target_id']
        money=d['fund']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE customerinfo SET deposit=deposit-%s where account_id=%s",(money,i_d))
        cur.execute("UPDATE customerinfo SET deposit=deposit+%s where account_id=%s",(money,target))
        mysql.connection.commit() 
        cur.close()   
        return render_template('status.html')





    	       
       


@app.route('/create.html', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        details = request.form
        ssn = details['ssn']
        
        name = details['name']
        age = details['age']
        address = details['address']
        state = details['state']
        city = details['city']
        cur = mysql.connection.cursor()
        status="Pending"
        cur.execute("INSERT INTO customerinfo(ssn_id, name, age, address, state, city,status) VALUES (%s, %s,%s, %s,%s, %s,%s)", (ssn,name,age,address,state,city,status))
        mysql.connection.commit()
        cur.execute(" SELECT * FROM customerinfo where ssn_id=%s",(ssn,))
        v=cur.fetchall()
        return render_template('profile.html', p=v)
      

@app.route('/create_account.html') 
def create_account1():
	if 'username' in session:
	    return render_template('create_account.html')  
	else:
	    return redirect('/')     

@app.route('/create_account.html/',methods=['GET', 'POST']) 
def create_account():
    if request.method == "POST":
        details=request.form
        account_type=details['type']
        i_d=details['id']
        deposit=details['deposit']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * from customerinfo where customer_id = %s",(i_d,))
        rows = cur.fetchall()
       
        
        for i in rows:
        	print(i)
        if(len(rows)==0):
            return (" no such customer exist")	
        else:
            active="Active"
            value=1
            value+=int(i_d)
            cur.execute("UPDATE customerinfo SET deposit=%s, type=%s,status=%s,account_id=%s where customer_id=%s",(deposit,account_type,active,value,i_d)) 
            mysql.connection.commit() 
            cur.close()   
            return ("success")
        

         
@app.route('/deposit.html')
def deposit():
    if 'username' in session:
        return render_template('deposit.html')
    else:
    	return redirect('/')


@app.route('/deposit.html/', methods=['GET', 'POST'])
def add_deposit():
  
    print(request.method)
    if request.method == 'POST':
        d=request.form
        customer_id= d['id']   
        account_id=d['account_id']
        deposit=d['deposit']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * from customerinfo where customer_id = %s and account_id=%s",(customer_id,account_id))
        rows = cur.fetchall()
        if rows:
            cur.execute("UPDATE customerinfo SET deposit=deposit+%s where customer_id=%s ",(deposit,customer_id))
            mysql.connection.commit()
            cur.close()
            return ("success")
        else:
    	    return ("no such details exist")
        	  





@app.route('/addcolumn')
def add_sql_column():	
    cur = mysql.connection.cursor()
    a="abhishek"
    b="9169125926"
    cur.execute("DESCRIBE customerinfo")
    
    rows = cur.fetchall()
    mysql.connection.commit()
    cur.close()
    for i in rows:
        print(i)
    return ("success")    
     

if __name__ == '__main__':
   app.run(debug = True)