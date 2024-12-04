from flask import Flask,redirect,request,url_for,render_template
app=Flask(__name__)
users={"swarna@gmail.com":{"username":"swarna","mobile":9876543210,"password":"P@nvith2023","q_id":{100:{"q_text":"What is Flask?","q_ans":"It is a Python Framework"},101:{'q_text':"DBMS","q_ans":"system"}}}}
# u=['swarna@gmail.com'{"q_text":"DBMS","q_ans":"Dtabase"}]

#Welcome page in basic route
@app.route('/')
def home():
    return render_template("welcome.html")
#admin welcme page
@app.route('/admin')
def admin():
    return render_template('a_welcome.html')
#user welcome page
@app.route('/user')
def user():
    return render_template('u_welcome.html')
#creating account for users
@app.route('/u_create',methods=['GET','POST'])
def u_create():
    if request.method=='POST':
        print(request.form)
        username=request.form['uname']
        email=request.form['uemail']
        mobile=request.form['unumber']
        password=request.form['upassword']
        if email not in users:
            users[email]={'username':username,"mobile":mobile,"password":password}
            print(users)
            return redirect(url_for('u_login'))
        else:
            return 'Account Already Exists'
    return render_template('u_create.html')
#login to user account
@app.route('/u_login',methods=['GET','POST'])
def u_login():
    if request.method=='POST':
        print(request.form)
        email=request.form['uemail']
        password=request.form['upassword']
        if email in users:
            if password==users[email]['password']:
                return redirect(url_for('dashboard',uemail=email))
            else:
                return "Password is incorrect"
        return "Invalid Email"
    return render_template('u_login.html')
#viewing user dashboard
@app.route('/dashboard/<uemail>')
def dashboard(uemail):
    return render_template('u_dashboard.html',uemail=uemail)
#posting questions and answers
@app.route('/create/<uemail>',methods=['GET','POST'])
def create(uemail):
    if request.method=='POST':
        print(request.form)
        q_text = request.form['question']
        q_ans = request.form['answer']
        q_id=request.form['qid']
        users[uemail]['q_id'] = {q_id:{'q_text': q_text,'q_ans': q_ans}}
        print(users)
        return redirect(url_for('view',uemail=uemail))
    return render_template('create.html',uemail=uemail)
#updating the previous questions and answers
@app.route("/update/<uemail>/<q_no>",methods=["GET", "POST"])
def update(uemail,q_no):
    if request.method=="POST":
        q_text=request.form["question"]
        q_ans=request.form['answer'] 
        users[uemail]['q_id'][q_no]['q_text']=q_text
        users[uemail]['q_id'][q_no]['q_ans']=q_ans
        return redirect(url_for('view',uemail=uemail))
    return render_template("update.html",uemail=uemail)
#read the question and answers
@app.route('/view/<uemail>')
def view(uemail):
    return render_template("view.html",data=users,uemail=uemail)
#deleting the question and answers
@app.route('/q_delete/<uemail>/<q_no>')
def q_delete(uemail,q_no):
    users[uemail]['q_id'].pop(q_no)
    return redirect(url_for('view',uemail=uemail))
#deleting the user account 
@app.route('/delete/<uemail>')
def delete(uemail):
    users.pop(uemail)
    return redirect(url_for('home'))
#user logout 
@app.route('/logout')
def logout():
    return redirect(url_for('u_login'))

    
app.run(debug=True,use_reloader=True)
