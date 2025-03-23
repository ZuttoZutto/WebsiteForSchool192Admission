from os import abort

import flask
from flask import render_template

from data import db_session
from data.database import Exams
from tools.checks import check_user_role

blueprint = flask.Blueprint(
    'exams_api',
    __name__,
    template_folder='templates'
)


@blueprint.route("/timetable")
def timetable():
    if check_user_role() == 3:
        return render_template("timetable.html")
    return abort(403, message="Forbidden")