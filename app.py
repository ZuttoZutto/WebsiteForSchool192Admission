#from crypt import methods

from flask import Flask, render_template, jsonify, send_file, redirect, send_from_directory, request, url_for, \
    current_app, session
from werkzeug.test import Client
from flask_login import LoginManager, logout_user, login_required, login_user, current_user
from flask_restful import Api, abort

from tools.checks import check_user_role

from data import db_session
from data.database import Users, Exams, Parents
from forms.editexamform import EditExamForm
from datetime import date

from forms.loginform import LoginForm
from forms.registerform import RegisterForm

from resources import exam_resources, demo_resources, users_resources, subexam_resources

import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

api = Api(app)

app.register_blueprint(exams_api.blueprint)

api.add_resource(demo_resources.DemoListResource, "/api/demo/")
api.add_resource(users_resources.UserResource, "/api/users/<int:user_id>/")
api.add_resource(exam_resources.ExamsListResource, "/api/exams/")
api.add_resource(exam_resources.ExamResource, "/api/exams/<int:exam_id>/", endpoint='api_one_exam')
#api.add_resource(subexam_resources.SubexamsListResource, "/api/subexams/")
#api.add_resource(subexam_resources.SubexamResource, "/api/subexams/<int:subexam_id>/")


def send_internal_request(method, url, payload=None):
    with current_app.test_request_context():
        session_cookie = dict(session)
        headers = {'Cookie': '; '.join(f'{key}={value}' for key, value in session_cookie.items())}
        response = requests.request(method, url, headers=headers, json=payload)
        return response.json()


@login_manager.user_loader
def load_user(user_id):
    print("DERMO")
    db_sess = db_session.create_session()
    return db_sess.get(Users, user_id)

@app.route("/")
def index():
    return render_template("index.html", title="lodusa")

@app.route("/timetable")
def timetable():
    if check_user_role() == 3:
        return render_template("timetable.html")
    return abort(403, message="Forbidden")

@app.route("/demoexams")
def demoexams():
    return render_template("demoexams.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(Users).filter(Users.Email == form.email.data).first()
        if user and form.phone.data:
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)

@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(Users).filter(Users.Email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        registrated_parent = (db_sess.query(Parents).
                              filter(Parents.Name == form.parent_name.data)
                              .first())
        if registrated_parent:
            parent_id = registrated_parent.id
        else:
            parent = Parents(
                Name=form.parent_name.data,
                Phone = "setto",
                Email = "setto",
                Surname = "setto",
            )
            db_sess.add(parent)
            db_sess.commit()
            parent_id = (db_sess.query(Parents).filter(Parents.Name == form.parent_name.data).first().id)
        user = Users(
            Name=form.name.data,
            Email=form.email.data,
            Phone=form.email.data,
            LastSchool="setto",
            Surname="setto",
            ParentId=parent_id,
            RoleId=1

        )
        db_sess.add(user)
        db_sess.commit()
        return redirect("/login")
    return render_template('register.html', title='Регистрация', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route('/g.png')
def download_g_png():
    return send_from_directory('static', 'g.png', as_attachment=True)

@app.route('/exams/<int:exam_id>', methods=['GET', 'POST'])
def edit_exam(exam_id):
    print("++++++++")
    if check_user_role() == 3:
        form = EditExamForm()
        if form.validate_on_submit():
            updated_data = {
                "Name": form.name.data,
                "Date": form.date.data.isoformat()
            }
            requests.put(f"http://127.0.0.1:5000/api/exams/{exam_id}/", json=updated_data)
            return redirect("/timetable")
        else:
            #user_role_json =
            #url = url_for('api_one_exam', exam_id=exam_id)
            client = Client(app)
            exam = send_internal_request("GET", f"http://127.0.0.1:5000/api/exams/{exam_id}/")
            #exam = client.get(f'/api/exams/{exam_id}/').json
            print(exam)
            #exam = requests.get("http://127.0.0.1:5000" + url).json()
            #subexams = requests.get(f"http://127.0.0.1:5000/api/subexams/").json()
            form.name.data = exam["Name"]
            form.date.data = date.fromisoformat(exam["Date"])
        return render_template('edit_exam.html', title='Изменение данных экзамена', form=form)
    return abort(403, message="Forbidden")

@app.route('/addexam', methods=['GET', 'POST'])
def add_exam():
    if check_user_role() == 3:
        form = EditExamForm()
        if form.validate_on_submit():
            data = {
                "Name": form.name.data,
                "Date": form.date.data.isoformat()
            }
            requests.post(f"http://127.0.0.1:5000/api/exams", json=data)
            return redirect("/timetable")
        return render_template('edit_exam.html', title='Добавление нового экзамена', form=form)
    return abort(403, message="Forbidden")


if __name__ == "__main__":
    db_session.global_init("db/db.db")
    app.run()