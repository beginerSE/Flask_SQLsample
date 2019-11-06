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
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    name = db.Column(db.Text())
    sex = db.Column(db.Text())
    hobby = db.Column(db.Text())

    def __init__(self, date, name, sex, hobby):
        self.date = date
        self.name = name
        self.sex = sex
        self.hobby = hobby


# データベースの作成(2回目からはエラーになるが例外処理で無視する)
try:
    db.create_all()
except:
    print('すでに作成済みです')


# トップ画面を表示
@app.route('/')
def index():
    return render_template('index.html')


# データをテーブルに登録する
@app.route('/add')
def add():
    return render_template('add.html')


# フォームからデータを取得してデータベースに登録する処理(INSERT)
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
    return render_template('redirect.html', msg='データを追加しました', ref='/')


# 登録したデータを確認する処理(SELECT)
@app.route('/select')
def select_table():
    # データベースからデータを取得する
    data = Sample_table.query.all()
    return render_template('table.html', item_list=data)


# 登録したデータを削除する処理(DELETE)
@app.route('/delete')
def delete_data():
    # 削除するuser_idを取得
    id_ = request.args["user_id"]
    # データを削除する
    delete_data = Sample_table.query.filter_by(user_id=id_).first()
    db.session.delete(delete_data)
    db.session.commit()
    data = Sample_table.query.all()
    return render_template('table.html', item_list=data)


# 登録したデータを更新する処理
@app.route('/update')
def update():
    # 更新するuser_idを取得
    id_ = request.args["user_id"]
    # データを削除する
    data = Sample_table.query.filter_by(user_id=id_)
    return render_template('update.html', item_list=data, id_=id_)


@app.route('/update_sql')
def update_sql():
    id_ = request.args["user_id"]
    data = Sample_table.query.filter_by(user_id=id_).first()
    # 日付と各データを変更
    data.date = datetime.now()
    data.name = request.args["name"]
    data.sex = request.args["gender"]
    data.hobby = request.args["hobby"]
    # 変更を保存する
    db.session.commit()
    return render_template('redirect.html', msg='データを更新しました', ref='/select')


# テスト環境起動
app.run(debug=True)
