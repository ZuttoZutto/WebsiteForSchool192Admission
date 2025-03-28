from flask import Flask, render_template, jsonify, send_file, redirect, send_from_directory
from flask_login import LoginManager, logout_user, login_required, login_user
from flask_restful import Api
from data import db_session
from data.database import Users, Exams, Parents

from forms.loginform import LoginForm
from forms.registerform import RegisterForm

from resources import exam_resources, demo_resources, users_resources

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

api = Api(app)

api.add_resource(exam_resources.ExamsListResource, "/api/exams/")
api.add_resource(demo_resources.DemoListResource, "/api/demo/")
api.add_resource(users_resources.UserResource, "/api/users/<int:user_id>/")

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(Users).get(user_id)

@app.route("/")
def index():
    return render_template("index.html", title="lodusa")

@app.route("/timetable")
def timetable():
    return render_template("timetable.html")

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

if __name__ == "__main__":
    db_session.global_init("db/db.db")
    app.run()