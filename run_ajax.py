#! /usr/bin/env python3
import json

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/ajaxDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    uname = db.Column(db.String(30))
    upwd = db.Column(db.String(30))
    uemail = db.Column(db.String(100))

db.create_all()

@app.route('/01-ajax-get')
def ajax_get():
    return render_template('01-ajax-get.html')

@app.route('/01-server')
def server01():
    return "这是ajax发送的get请求的响应"


@app.route('/02-ajax-get')
def ajax_get02():
    return render_template('02-ajax-get.html')
#02-ajax-get.html包含
#input type='text' name='uname'
#button id = 'btnGet'
#div id = 'show'
@app.route('/02-server')
def server02():
    uname = request.args.get('uname')
    return '欢迎'+uname


@app.route('/03-register')
def register():
    return render_template('03-register.html')

@app.route('/03-checkuname')
def checkuname():
    uname = request.args.get('uname')
    user = User.query.filter_by(uname = uname).first()
    if user:
        return '1'
    else:
        return '0'


@app.route('/03-reg',methods=['POST'])
def reg():
    uname = request.form.get('uname')
    upwd = request.form.get('upwd')
    uemail = request.form.get('uemail')

    user = User()
    user.uname = uname
    user.upwd = upwd
    user.uemail = uemail

    try:
        db.session.add(user)
        db.session.commit()
        return '注册成功'
    except Exception as e:
        print(e)
        return '注册失败'


@app.route('/04-post')
def post():
    return  render_template('04-post.html')

@app.route('/04-server',methods = ['POST'])
def server04():
    uname = request.form['uname']
    return '欢迎'+uname


@app.route('/05-jq-ajax')
def jq_ajax():
    return render_template('05-jq-ajax.html')

@app.route('/05-server')
def server05():
    return '这是使用$.ajax()发送的get请求'
    # list = [
    #     {'uname':'刘姥姥','uage':80},
    #     {'uname':'嫦娥','uage':28},
    #     {'uname':'貂蝉','uage':28}
    # ]
    # return json.dumps(list)

@app.route('/06-jq-post')
def jq_post():
    return render_template('06-jq-post.html')

@app.route('/06-server',methods=['POST'])
def server06():
    uname = request.form.get('uname')
    user = User.query.filter_by(uname=uname).first()
    if user:
        res = {'code':200,'data':'欢迎:'+uname}
    else:
        res = {'code':201,'data':'找不到用户'}
    return json.dumps(res)


@app.route('/07-register')
def jq_register():
    return render_template('07-register-jq.html')
@app.route('/07-checkuname')
def checkuname_view():
    uname = request.args.get('uname')
    user = User.query.filter_by(uname=uname).first()
    if user:
        dic = {'code':201,'data':'uname already exist'}
    else:
        dic = {'code':200,'data':'OK'}
    return json.dumps(dic)

@app.route('/07-server',methods=['POST'])
def server07():
    uname = request.form.get('uname')
    upwd = request.form.get('upwd')
    uemail = request.form.get('uemail')
    user = User()
    user.uname = uname
    user.upwd = upwd
    user.uemail = uemail
    try:
        db.session.add(user)
        db.session.commit()
        dic = {
            'code':200,
            'data':'register success'
        }
    except Exception as e:
        print(e)
        dic = {
            'code':202,
            'data':'register failed'
        }
    return json.dumps(dic)






if __name__ == '__main__':
    app.run(debug=True)