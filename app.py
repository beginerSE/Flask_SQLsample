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
class Sample_table(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    name_ = db.Column(db.Integer)
    sex = db.Column(db.Text())
    hobby = db.Column(db.Text())

    def __init__(self, pub_date, name, sex, hobby):
        self.pub_date = pub_date
        self.name = name
        self.sex = sex
        self.hobby = hobby


# データベースの作成(2回目からはエラーになるが例外処理で無視する)
try:
    db.create_all()
    print('ok')
except:
    print('すでに作成済みです')


# トップ画面を表示
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add_sql')
def add_sql():

    # 日付を取得
    date = datetime.now()

    # 入力フォームのデータを取得
    name = request.args["name"]
    sex = request.args["gender"]
    hobby = request.args["hobby"]

    # テーブルにデータを追加する
    add_data = Sample_table(date, name, sex, hobby)
    db.session.add(add_data)

    # テーブルへの変更を保存する
    db.session.commit()

    return render_template('redirect.html')


# テスト環境起動
app.run(debug=True)
