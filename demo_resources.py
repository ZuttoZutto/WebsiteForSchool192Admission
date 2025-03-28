from flask import session, jsonify, render_template
from flask_restful import Resource, abort, reqparse
from data import db_session
from data.database import DemoExams


def abort_if_exam_not_found(exam_id):
    session = db_session.create_session()
    exam = session.query("Exams").get(exam_id)
    if not exam:
        abort(404, message=f"Demo {exam_id} not found")

parser = reqparse.RequestParser()
parser.add_argument("id", required=True)
parser.add_argument("Name", required=True)
parser.add_argument("Date", required=True)

class DemoListResource(Resource):
    def get(self):
        session = db_session.create_session()
        demos = session.query(DemoExams).all()
        return jsonify([item.to_dict(
            only=("id", "Name", "FilePath")) for item in demos])

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        exam = Exams(
            id=args["id"],
            Name=args["Name"],
            Date=args["Date"]
        )
        session.add(exam)
        session.commit()
        return jsonify({"id": exam.id})