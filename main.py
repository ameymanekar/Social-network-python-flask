from flask import *
from databace import MiniBank
import os
import pymysql as pm
from flask_mail import *
app = Flask(__name__, template_folder='templates')
app.secret_key = "abc"
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME'] = 'ameymanekar12@gmail.com'
app.config['MAIL_PASSWORD'] = 'oiszasyfivuscbsr'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mymail = Mail(app)


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/profile')
def profile():
    db = pm.connect('localhost', 'root', 'root', 'hvpm')
    mess2 = session['mess']
    cursor = db.cursor()
    sql = "select * from snuser where email = '%s'" %(mess2)

    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        return render_template('profile.html', result=result)
    except:
        print("failed")
        db.close()
    return render_template('profile.html',result=result)


@app.route('/logout')
def logout():
    session.pop('mess',None)
    session.pop('photo', None)
    session.pop('dot', None)
    session.pop('user', None)
    return render_template('index.html')


@app.route('/friends')
def friends():

    return render_template('friends.html')


@app.route('/forgotpass', methods=['POST', 'GET'])
def forgotpass():
    if request.method == 'POST':
        f1 = request.form['email']
        f2 = request.form['phoneno']

        db = pm.connect('localhost', 'root', 'root', 'hvpm')
        cursor = db.cursor()
        sql = "select * from snuser where email = '%s' and phoneno = '%s'" % (f1, f2)
        cursor.execute(sql)

        if cursor.rowcount:
            result = cursor.fetchall()
            for row in result:
                pass2 = row[4]
                user1 = row[1]
            msg = Message('amey', sender='ameymanekar12@gmail.com', recipients=[f1])
            msg.body = "hello..  "+user1+" Your Password is " +pass2
            mymail.send(msg)
            massage2 = 'Password Send, Please Check The Mail'
            return render_template('index.html', massage2=massage2)
            cursor.close()
        else:
            massage2 = 'Your Email Or Mobile No Is Incorrect'
            return render_template('index.html', massage2=massage2)

    return render_template('forgotpass.html')




@app.route('/friendreq')
def friendreq():
    mess2 = session['mess']
    db = pm.connect('localhost', 'root', 'root', 'hvpm')
    cursor = db.cursor()
    sql = "select * from friendreq where tof = '%s' " % (mess2)
    cursor.execute(sql)
    result = cursor.fetchall()
    db.close()
    return render_template('friendreq.html', result=result)



@app.route('/friends2')
def friends2():
    mess2 = session['mess']
    db = pm.connect('localhost', 'root', 'root', 'hvpm')
    cursor = db.cursor()
    sql = "select * from friends where f1 = '%s' " % (mess2)
    cursor.execute(sql)
    result = cursor.fetchall()
    db.close()

    return render_template('friends2.html', result=result)




@app.route('/accecpt', methods=['POST', 'GET'])
def accecpt():
    if request.method == 'POST':
        session.pop('dot', None)
        f1 = request.form['fromf']
        f2 = request.form['tof']
        f3 = request.form['fuser']
        f4 = request.form['aaa']
        NU = 0
        db = pm.connect('localhost', 'root', 'root', 'hvpm')
        cursor = db.cursor()
        sql1 = "insert into friends values('%d','%s','%s','%s','%s')" % (NU, f1, f2, f3, f4)
        sql2 = "insert into friends values('%d','%s','%s','%s','%s')" % (NU, f2, f1, f4, f3)
        sql3 = "delete from friendreq where tof = '%s'" % (f2)
        cursor.execute(sql1)
        cursor.execute(sql2)
        cursor.execute(sql3)
        try:
            db.commit()
            result2 = "Accepted"
            return render_template('friendreq.html', result2=result2)
        except:
            db.rollback()
            status = False
            return status

    return render_template('friendreq.html',)

@app.route('/delete', methods=['POST', 'GET'])
def delete():
    if request.method == 'POST':
        session.pop('dot', None)
        f2 = request.form['email']

        db = pm.connect('localhost', 'root', 'root', 'hvpm')
        cursor = db.cursor()

        sql3 = "delete from friendreq where tof = '%s'" % (f2)

        cursor.execute(sql3)
        try:
            db.commit()
            result2 = "Deleted"
            return render_template('friendreq.html', result2=result2)
        except:
            db.rollback()
            status = False
            return status


    return render_template('friendreq.html',)


@app.route('/sendreq', methods=['POST', 'GET'])
def sendreq():
    if request.method == 'POST':
        fromf =  request.form['email']
        tof = request.form['email2']
        uname = request.form['uname']
        user = request.form['user']
        mess2 = session['mess']
        db = pm.connect('localhost', 'root', 'root', 'hvpm')
        cursor = db.cursor()
        sql = "select * from friends where f1 = '%s' and f2 = '%s' " % (fromf, tof)
        cursor.execute(sql)
        if cursor.rowcount:
            message = "Already Friends..!!!"
            return render_template("friends.html", result2=message)
            cursor.close()
        else:
            if fromf == mess2:
                message = "You are sending request to yourself..!!!"
                return render_template("friends.html", result2=message)

            else:
                NU = 0
                db = pm.connect('localhost', 'root', 'root', 'hvpm')
                cursor = db.cursor()
                sql = "insert into friendreq values('%d','%s','%s','%s','%s')" % ( NU , tof, fromf, uname, user)
                cursor.execute(sql)
                try:
                     db.commit()
                     result2 = "Friend Request Sent"
                     return render_template('friends.html', result2=result2 )
                except:
                     db.rollback()
                     status = False
                     return status
        return render_template('sendreq.html')


@app.route('/viewpro', methods=['POST', 'GET'])
def viewpro():
    if request.method == 'POST':
        f = request.form['email']
        db = pm.connect('localhost', 'root', 'root', 'hvpm')
        cursor = db.cursor()
        cursor2 = db.cursor()
        sql = "select * from snuser where email = '%s'" % (f)
        sql2 = "select * from photoloc where email = '%s'" % (f)
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor2.execute(sql2)
        result2 = cursor2.fetchall()


        return render_template('viewpro.html', result=result ,result2=result2)
        db.close()
    return render_template('viewpro.html')



@app.route('/viewpro2', methods=['POST', 'GET'])
def viewpro2():
    if request.method == 'POST':
        f = request.form['email']
        db = pm.connect('localhost', 'root', 'root', 'hvpm')
        cursor = db.cursor()
        cursor2 = db.cursor()
        sql = "select * from snuser where email = '%s'" % (f)
        sql2 = "select * from photoloc where email = '%s'" % (f)
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor2.execute(sql2)
        result2 = cursor2.fetchall()



        return render_template('viewpro2.html', result=result ,result2=result2)
        db.close()
    return render_template('viewpro2.html')





@app.route('/searchriend', methods=['POST', 'GET'])
def searchriend():
    if request.method == 'POST':
        friend = request.form['search']
        db = pm.connect('localhost', 'root', 'root', 'hvpm')

        cursor = db.cursor()
        sql = "select * from snuser where uname like '%s'" %( friend+ "%")

        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            mess2 = session['mess']
            sql4 = "select * from snuser where email = '%s'" % (mess2)
            if cursor.execute(sql4):
                result4 = cursor.fetchall()
                for row4 in result4:
                    user4 = row4[1]
                    session['user'] = user4

            return render_template("friends.html", result=result)

        except:
            print("failed")
            db.close()
    return render_template('friends.html')



@app.route('/setting',  methods=['POST', 'GET'])
def setting():
    if request.method == 'POST':
         email = request.form['email']
         opass = request.form['opass']
         npass = request.form['npass']

         db = pm.connect('localhost', 'root', 'root', 'hvpm')
         cursor = db.cursor()
         sql = "select * from snuser where password = '%s' and email = '%s' " % (opass,email)
         cursor.execute(sql)
         con = MiniBank()
         if cursor.rowcount:
             if con.updatepass(email,npass) == True:
                 message = "Password Updated !!!"
                 return render_template('setting.html', message=message)
             else:
                  message = " failed, please try again !!!"
                  return render_template('setting.html', message=message)
                  cursor.close()
         else:

             message = "Old Password is incorrect"
             return render_template("setting.html", message=message)


    return render_template('setting.html')


@app.route('/home')
def home():
    mess2 = session['mess']
    db = pm.connect('localhost', 'root', 'root', 'hvpm')
    cursor = db.cursor()
    sql = "select * from photoloc where email = '%s'" % (mess2)
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        user1 = row[2]
        session['photo'] = user1


    return render_template('home.html',message=mess2)


@app.route('/checklogin', methods=['POST', 'GET'])
def checklogin():
    if request.method == 'POST':
        log = request.form['txt1']
        pas = request.form['txt2']
        m = MiniBank()
        if m.checklogin(log,pas) == True:
            session['mess'] = log
            mess2 = session['mess']
            db = pm.connect('localhost', 'root', 'root', 'hvpm')
            cursor = db.cursor()
            sql = "select * from photoloc where email = '%s'" % (mess2)
            if cursor.execute(sql):
                 result = cursor.fetchall()
                 for row in result:
                     user1 = row[2]
                     session['photo'] = user1
            else:
                session.pop('photo', None)
                return render_template('home.html',message=session['mess'])
            cursor3 = db.cursor()
            sql3 = "select * from friendreq where tof = '%s'" % (mess2)
            if  cursor3.execute(sql3):
                  if cursor3.rowcount:
                         result3 = cursor3.fetchall()
                         for row3 in result3:
                            user3 = row3[1]
                            session['dot'] = user3
            else:
                    return render_template('home.html',message=session['mess'])

            db.close()
            return render_template('home.html',message=session['mess'])

        else:
            message = "Login Failed !!!"
            return render_template('index.html', message=message)
        m.die()
        return render_template('home.html',message=session['mess'])

    return render_template('home.html',message=session['mess'])








@app.route('/showdata')
def showdata():
    db = pm.connect('localhost', 'root', 'root', 'hvpm')

    cursor = db.cursor()
    sql = "select * from users"

    try:
        cursor.execute(sql)
        result = cursor.fetchall()

        return render_template("message.html", aa=result)

    except:
         print("failed")
         db.close()


@app.route('/updatedata')
def updatedata():
    db = pm.connect('localhost', 'root', 'root', 'hvpm')

    cursor = db.cursor()
    sql = "select * from users"

    try:
        cursor.execute(sql)
        result = cursor.fetchall()

        return render_template("message.html", aa=result)

    except:
         print("failed")
         db.close()

@app.route('/success', methods = ['POST'])
def success():
    if request.method == 'POST':
        db = pm.connect('localhost', 'root', 'root', 'hvpm')
        cursor = db.cursor()
        f = request.files['file']
        path = "static/images/profile/"+session['mess']
        b = session['mess']
        c ="/../"+ path+"/"+b+f.filename


        NU = 0
        sql = "insert into photoloc values('%d','%s','%s')" % (NU ,b ,c)
        cursor.execute(sql)
        db.commit()


        f.save( path +"/"+b+f.filename)
        print(c)

        mess2 = session['mess']

        cursor2 = db.cursor()
        sql2 = "select * from photoloc where email = '%s'" % (mess2)
        cursor2.execute(sql2)
        result = cursor2.fetchall()
        for row in result:
            user1 = row[2]
            session['photo'] = user1

        return render_template("home.html")




@app.route('/doStoreLogin',methods=['POST','GET'])
def doStoreLogin():
    if request.method=='POST':

        email=request.form['txtemail1']
        pass1=request.form['pass']

        uname = request.form['Username']
        phoneno = request.form['phone']
        dob =  request.form['DOB']
        loc = request.form['loc']
        gen = request.form['gender']
        db = pm.connect('localhost', 'root', 'root', 'hvpm')
        cursor = db.cursor()
        sql = "select * from snuser where email = '%s' " %(email)
        cursor.execute(sql)
        con=MiniBank()
        if cursor.rowcount:
            message = "Email Already Exists..!!!"
            return render_template("index.html", message=message)
            cursor.close()
        else:
             if con.storeLogin(email,pass1,uname,phoneno,dob,loc,gen)==True:
                 path = "static/images/profile/" + email
                 os.mkdir(path)
                 session.pop('mess', None)
                 session.pop('photo', None)
                 session.pop('dot', None)
                 session.pop('user', None)
                 message="Signup Successful !!!"
             else:
                 message="Signup failed, please try again !!!"
                 return render_template('index.html', message=message)
    return render_template('index.html',message=message)




if __name__ == '__main__':
    app.run(debug=True)

