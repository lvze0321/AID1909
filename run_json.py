import json
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:123456@localhost:3306/ajaxDB'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    uname = db.Column(db.String(30))
    upwd = db.Column(db.String(30))
    uemail = db.Column(db.String(100))

    #将本类中所有的属性封装到字典中并返回
    def to_dict(self):
        dic = {
            'id':self.id,
            'uname':self.uname,
            'upwd':self.upwd,
            'uemail':self.uemail
        }
        return dic


db.create_all()

@app.route('/01-json')
def json01():
    return render_template('01-json.html')

@app.route('/02-json-server')
def json_server():
    # dic = {'uname':'laotao','uage':30}
    # jsonStr = json.dumps(dic)
    # print(jsonStr)
    # return jsonStr

    ulist = [
        {
            "uname":"daxu",
            "uage":30
        },
        {
            "uname": "lvze",
            "uage": 30
        }
    ]
    jsonStr = json.dumps(ulist)
    print(jsonStr)
    return jsonStr

@app.route('/03-json-db')
def json_db():
    ulist = []
    users = User.query.all()
    for u in users:
        ulist.append(u.to_dict())

    jsonStr = json.dumps(ulist)
    return jsonStr

@app.route('/04-users')
def users_view():
    return render_template('04-users.html')
#04-users.html 中包含表格和 一个按钮 点击按钮显示数据
#id  姓名  年龄  邮箱
@app.route('/04-server')
def server04():
    ulist = []
    users = User.query.all()
    for u in users:
        ulist.append(u.to_dict())
    jsonStr = json.dumps(ulist)
    return jsonStr




if __name__ == '__main__':
    app.run(debug=True)