from flask import session, jsonify, render_template
from flask_restful import Resource, abort, reqparse
from data import db_session
from data.database import DemoExams, Subexams
from tools.checks import check_user_role


def abort_if_exam_not_found(subexam_id):
    session = db_session.create_session()
    exam = session.query(Subexams).get(subexam_id)
    if not exam:
        abort(404, message=f"Subexam {subexam_id} not found")

parser = reqparse.RequestParser()
parser.add_argument("Name", required=True)
parser.add_argument("ExamId")
parser.add_argument("NumberOfSubexam")

class SubexamsListResource(Resource):
    def get(self):
        if check_user_role() == 3:
            session = db_session.create_session()
            subexams = session.query(Subexams).all()
            return jsonify([item.to_dict(
                only=("id", "Name", "ExamId", "NumberOfSubexam")) for item in subexams])
        return abort(403, message="Forbidden")

    def post(self):
        if check_user_role() == 3:
            args = parser.parse_args()
            session = db_session.create_session()
            subexam = Subexams(
                Name=args["Name"],
                ExamId=args["ExamId"],
                NumberOfSubexam=args["NumberOfSubexam"]
            )
            session.add(subexam)
            session.commit()
            return jsonify({"id": subexam.id})
        return abort(403, message="Forbidden")


class SubexamResource(Resource):
    def get(self, subexam_id):
        if check_user_role() == 3:
            abort_if_exam_not_found(subexam_id)
            session = db_session.create_session()
            subexam = session.query(Subexams).get(subexam_id)
            return jsonify(subexam.to_dict(only=("id", "Name", "Date")))
        return abort(403, message="Forbidden")

    def put(self, subexam_id):
        if check_user_role() == 3:
            args = parser.parse_args()
            abort_if_exam_not_found(subexam_id)
            session = db_session.create_session()
            subexam = session.query(Subexams).get(subexam_id)
            subexam.Name = args["Name"]
            session.commit()
            return jsonify({"message": "Success"})
        return abort(403, message="Forbidden")