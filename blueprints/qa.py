from flask import Blueprint, request, render_template, g, redirect, url_for

from blueprints.forms import QuestionForm
from models import myQuestionModel
from exts import db
bp = Blueprint("qa",__name__,url_prefix="/")

@bp.route("/")
def index():
    questions = myQuestionModel.query.order_by(myQuestionModel.create_time.desc()).all()
    return render_template("index.html",questions=questions)

@bp.route("qa/public",methods=['GET','POST'])
def public_qa():
    if request.method == 'GET':
        return render_template("public_question.html")
    else:
        form = QuestionForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            question = myQuestionModel(title=title,content=content,author=g.user)
            db.session.add(question)
            db.session.commit()

            return redirect("/")
        else:
            print(form.errors)
            return redirect(url_for("qa.public_question"))

@bp.route("/qa/detail/<qa_id>")
def qa_detail(qa_id):
    question = myQuestionModel.query.get(qa_id)
    return render_template("detail.html",question=question)
