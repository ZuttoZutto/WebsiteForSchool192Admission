from flask import session, jsonify, render_template
from flask_restful import Resource, abort, reqparse

from data import db_session
from data.database import Exams
from datetime import date
from tools.checks import check_user_role

def abort_if_exam_not_found(exam_id):
    session = db_session.create_session()
    exam = session.query(Exams).get(exam_id)
    if not exam:
        abort(404, message=f"Exam {exam_id} not found")

parser = reqparse.RequestParser()
parser.add_argument("Name", required=True)
parser.add_argument("Date", required=True)

class ExamsListResource(Resource):
    def get(self):
        if check_user_role() == 3:
            session = db_session.create_session()
            exams = session.query(Exams).all()
            return jsonify([item.to_dict(
                only=("id", "Name", "Date")) for item in exams])
        return abort(403, message="Forbidden")

    def post(self):
        if check_user_role() == 3:
            args = parser.parse_args()
            session = db_session.create_session()
            exam = Exams(
                Name=args["Name"],
                Date=date.fromisoformat(args["Date"])
            )
            session.add(exam)
            session.commit()
            return jsonify({"id": exam.id})
        return abort(403, message="Forbidden")

class ExamResource(Resource):
    def get(self, exam_id):
        print("CGERRR---------------------------")
        if check_user_role() == 3:
            abort_if_exam_not_found(exam_id)
            session = db_session.create_session()
            exam = session.query(Exams).get(exam_id)
            return jsonify(exam.to_dict(only=("id", "Name", "Date")))
        return abort(403, message="Forbidden")

    def put(self, exam_id):
        if check_user_role() == 3:
            args = parser.parse_args()
            abort_if_exam_not_found(exam_id)
            session = db_session.create_session()
            exam = session.query(Exams).get(exam_id)
            exam.Name = args["Name"]
            exam.Date = date.fromisoformat(args["Date"])
            session.commit()
            return jsonify({"message": "Success"})
        return abort(403, message="Forbidden")





