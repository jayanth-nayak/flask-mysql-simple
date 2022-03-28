from sqlalchemy import create_engine
import flask
import json
from flask import request, render_template, redirect
import uuid
app = flask.Flask(__name__)
app.config["DEBUG"] = True
engine = create_engine('sqlite:///database.db', echo=True)

try:
    conn = engine.connect()
    conn.execute("CREATE TABLE users (name VARCHAR(45) NOT NULL,email VARCHAR(45) NOT NULL,password VARCHAR(45) NOT NULL,PRIMARY KEY (`email`));") 
except:
    pass

def execute_query(query):
    conn = engine.connect()
    return conn.execute(query) 

def get_users():
    users = execute_query("SELECT * FROM users;").fetchall()
    userdata = []
    temp = {}
    for i in users:
        temp["name"] = i[0]
        temp["email"] = i[1]
        temp["password"] = i[2]
        userdata.append(temp)
    return userdata

def insert_user(name, email, password):
    print(f"INSERT INTO users(name, email, password) VALUES('{name}', '{email}', '{password}');")
    execute_query(f"INSERT INTO users(name, email, password) VALUES('{name}', '{email}', '{password}');")

def update_password(email, password):
    print(f"UPDATE users SET password = '{password}' WHERE email='{email}';")
    execute_query(f"UPDATE users SET password = '{password}' WHERE email='{email}';")

def delete_user(email):
    execute_query(f"DELETE FROM users WHERE email='{email}';")

def find_user(email):
    user = execute_query(f"SELECT * FROM users WHERE email='{email}';").fetchone()
    # userdata = []
    # temp = {}
    # for i in users:
    #     temp["name"] = i[0]
    #     temp["email"] = i[1]
    #     temp["password"] = i[2]
    #     userdata.append(temp)
    return user


@app.route('/', methods=['GET', 'POST'])
def UsersController():
    if request.method == 'GET':
        users = get_users()
        return render_template('index.html',users=users)
        # return json.dumps(get_users())
    else:
        print(request.form["name"])
        print(request.form["email"])
        print(request.form["password"])
        try:
            insert_user(request.form["name"], request.form["email"], request.form["password"])
            # return {"message" : "done"}
            return redirect('/')
        except Exception as e:
            return {"message" : "error"}

@app.route('/updatepassword/<int:id>', methods=['GET', 'POST'])
def UpdatePassword(id):
    if request.method=='POST':
        # email=request.form['email']
        # password=request.form['password']
        update_password(request.form['email'],request.form['password'])
        return redirect('/')
    else:
        users = get_users()
        return render_template('updatepassword.html',user=users[id])

@app.route('/delete/<email>')
def DeleteUser(email):
    # email = request.args['email']
    delete_user(email)
    return redirect('/')   
app.run(host='0.0.0.0', port=5000, debug=True)
