import data
from data.database import Exams, DemoExams, Users
from data import db_session
import datetime

db_session.global_init("db/db.db")
db_sess = data.db_session.create_session()
user = Users(
            Name="3",
            Email="t@t.com",
            Phone="3",
            LastSchool="setto",
            Surname="setto",
            ParentId=1,
            RoleId=3

        )
db_sess.add(user)
db_sess.commit()