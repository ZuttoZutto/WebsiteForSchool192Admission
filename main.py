from flask import Flask, render_template, redirect, request, make_response, session, abort, jsonify
from data import db_session
from data.usersOLD import User
from data.news import News
from forms.user import RegisterForm
from flask_login import LoginManager, login_required, logout_user, current_user
from forms.user import LoginForm
from forms.news import NewsForm
from flask_login import login_user
from data import db_session, news_api
from flask_restful import reqparse, abort, Api, Resource
from news_resources import NewsListResource, NewsResource

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)



if __name__ == '__main__':
    app.run()