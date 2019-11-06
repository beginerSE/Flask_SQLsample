from flask import Flask, request, render_template
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
SQLALCHEMY_TRACK_MODIFICATIONS = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# SQLAlchemyでデータベースに接続する
db_uri = 'sqlite:///test.db'
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

db = SQLAlchemy(app) 

# データベースの仕様をpythonのクラスで定義する

class order_table(db.Model): 
    orderid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pub_date = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    goods_number = db.Column(db.Integer)
    payment = db.Column(db.Text())
    
    def __init__(self, pub_date, goods_number, payment):
        self.pub_date = pub_date
        self.goods_number = goods_number
        self.payment = payment
try:
    db.create_all() 
    print('ok')
except:
    print('すでに作成済みです')
    
