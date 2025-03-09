from sqlalchemy import create_engine, Column, Integer, String, Date, Numeric, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

class Classes(Base):
    __tablename__ = 'Classes'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    ProfileId = Column(Integer, ForeignKey('Profiles.id'), nullable=False)
    Number = Column(Integer, nullable=False)
    Letter = Column(String)

class Exams(Base):
    __tablename__ = 'Exams'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    Name = Column(String, unique=True, nullable=False)
    Date = Column(Date, nullable=False)

class Profiles(Base):
    __tablename__ = 'Profiles'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    Name = Column(String, unique=True, nullable=False)

class Messages(Base):
    __tablename__ = 'Messages'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    UserId = Column(Integer, ForeignKey('Users.id'), nullable=False)
    TitleId = Column(Integer, ForeignKey('MessageTitles.id'), nullable=False)
    TextId = Column(Integer, ForeignKey('MessageTexts.id'), nullable=False)

class Parents(Base):
    __tablename__ = 'Parents'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    Name = Column(String, nullable=False)
    Surname = Column(String, nullable=False)
    Phone = Column(String, nullable=False)
    Email = Column(String, nullable=False)

class Roles(Base):
    __tablename__ = 'Roles'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    Role = Column(String, unique=True, nullable=False)

class MarksList(Base):
    __tablename__ = 'MarksList'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    UserId = Column(Integer, ForeignKey('Users.id'), nullable=False)
    SubexamId = Column(Integer, ForeignKey('Subexams.id'), nullable=False)
    Date = Column(Date, nullable=False)
    Mark = Column(Numeric, nullable=False)

class ExamsList(Base):
    __tablename__ = 'ExamsList'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    ClassId = Column(Integer, ForeignKey('Classes.id'), nullable=False)
    ExamId = Column(Integer, ForeignKey('Exams.id'), nullable=False)

class DemoExams(Base):
    __tablename__ = 'DemoExams'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    Name = Column(String, unique=True, nullable=False)
    FilePath = Column(String, nullable=False)

class StudentsList(Base):
    __tablename__ = 'StudentsList'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    UserId = Column(Integer, ForeignKey('Users.id'), nullable=False)
    ClassId = Column(Integer, ForeignKey('Classes.id'), nullable=False)

class MessageTitles(Base):
    __tablename__ = 'MessageTitles'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    Title = Column(String)

class MessageTexts(Base):
    __tablename__ = 'MessageTexts'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    Text = Column(String)

class Comments(Base):
    __tablename__ = 'Comments'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    MarkId = Column(Integer, ForeignKey('MarksList.id'), nullable=False)
    Comment = Column(String, nullable=False)

class UserClasses(Base):
    __tablename__ = 'UserClasses'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    ClassId = Column(Integer, ForeignKey('Classes.id'), nullable=False)
    UserId = Column(Integer, ForeignKey('Users.id'), nullable=False)

class AdditionalInformation(Base):
    __tablename__ = 'AdditionalInformation'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    UserId = Column(Integer, ForeignKey('Users.id'), nullable=False)
    n = Column(Integer, nullable=False)

class Subexams(Base):
    __tablename__ = 'Subexams'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    Name = Column(String, nullable=False)
    ExamId = Column(Integer, ForeignKey('Exams.id'), nullable=False)
    NumberOfSubexam = Column(Integer, nullable=False)