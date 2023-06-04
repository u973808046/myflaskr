import random

from flask import Blueprint, render_template, jsonify, redirect, url_for, session

from exts import mail, db
from flask_mail import Message
from flask import request
import string
from blueprints.forms import RegisterForm,LoginForm
from models import UserModel
from werkzeug.security import generate_password_hash, check_password_hash

#/auth
from models import EmailCaptchaModel

bp = Blueprint("auth",__name__,url_prefix="/auth")

@bp.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                print("邮箱在数据库中不存在！")
                return redirect(url_for("auth.login"))
            if check_password_hash(user.password,password):
                session['user_id'] = user.id
                return redirect("/")
            else:
                print("密码错误！")
                return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            return redirect(url_for("auth.login"))



@bp.route("/register",methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user = UserModel(email=email,username=username,password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            return redirect(url_for("auth.register"))


@bp.route("/captcha/email")
def get_email_captcha():
    # /captcha/email/<email>
    # /captcha/email?email=xxx@qq.com
    email = request.args.get("email")
    #4/6:数字
    source = string.digits*4
    captcha = random.sample(source,4)
    captcha = "".join(captcha)
    message = Message(subject="博客注册验证码", recipients=[email], body=f"您的验证码是：{captcha}")
    mail.send(message)
    #用数据库的方式存储
    email_captcha = EmailCaptchaModel(email=email,captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()
    return jsonify({"code":200,"messgae":"","data": None})




@bp.route("/mail/test")
def mail_test():
    message = Message(subject="邮箱测试",recipients=["lgl19990419@163.com"],body="这是一条测试邮件，收到请给你最好的朋友v50")
    mail.send(message)
    return "邮件发送成功"
