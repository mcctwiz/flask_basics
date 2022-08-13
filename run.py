from audioop import add
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import time
import json


app = Flask(__name__)

app.config.update(
    SECRET_KEY='5h1dnQnndbHlZXpRy3PG9gHw4xGq9g1E',
    SQLALCHEMY_DATABASE_URI='postgresql://inntbumy:5h1dnQnndbHlZXpRy3PG9gHw4xGq9g1E@rajje.db.elephantsql.com/inntbumy',
    SQLALCHEMY_TRACK_NOTIFICATIONS=False
)

# CREATE OUT DATABASE OBJECT
db = SQLAlchemy(app)


@app.route('/')
def homepage():
    today = time.ctime()
    return render_template('index.html',myTime=today)


@app.route('/tables/')
def create_table():
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    my_data = data
    return render_template('using_macro.html',user_data=my_data)

def add_db_items():
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
            
    i = 0
    while i < len(data):    
        for dic in data:
            # user var to create class object
            a = UserInfo(dic['first_name'], dic['last_name'],dic['email'],
                         dic['phone_num'],dic['address'],dic['city'],dic['state'],dic['zip'])
            
            # From class use the db session to add and commit before next loop
            db.session.add(a)
            db.session.commit()
            i += 1




#==================DATABASE CLASSES==================#
class UserInfo(db.Model):
    # Set the table name
    __tablename__ = 'userinfo'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(120))
    phone_num = db.Column(db.String(20))
    address = db.Column(db.String(150))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    zip_code = db.Column(db.Integer)
    
    def __init__(self, fname, lname, email, phone, addr, city, state, zip):
        self.first_name = fname
        self.last_name = lname
        self.email = email
        self.phone_num = phone
        self.address = addr
        self.city = city
        self.state = state
        self. zip_code = zip
        
        
    def __repr__(self):
        return f'{self.first_name} {self.last_name} has been added'
    
        
    
    
    

if __name__ == '__main__':
    # TO CREATE THE DATABSE USE THE FOLLOW
    db.create_all()
    app.run(debug=True)