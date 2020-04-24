from .extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

class Admin(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username= db.Column(db.Text, nullable = False, unique = True)
    password = db.Column(db.Text , nullable =False)
    question = db.Column(db.Text, nullable = False)
    answer = db.Column(db.Text, nullable = False)
    active = db.Column(db.Boolean,default=False)  #0 for inactive 1 for active
    role = db.Column(db.Boolean,default=False)   #0 for user 1 for admin

    @property
    def unhashed_password(self):
        raise AttributeError('Cannot view unhashed password !')
    
    @unhashed_password.setter # This is setter. Anytime we initialise the value or set it the code here will execute.
    def unhashed_password(self,unhashed_password):
        self.password = generate_password_hash(unhashed_password)

    @property
    def unhashed_answer(self):
        raise AttributeError('Cannot view unhashed answer !')
    @unhashed_answer.setter
    def unhashed_answer(self,answer):
        self.answer = generate_password_hash(answer)


class User(db.Model):
    user_id = db.Column(db.Integer,db.ForeignKey('admin.id'), primary_key=True)
    name=db.Column(db.Text)
    about= db.Column(db.Text)
    address= db.Column(db.Text)
    email= db.Column(db.Text)
    phone= db.Column(db.Text)
    github= db.Column(db.Text)
    resume= db.Column(db.Text)
    linkedin= db.Column(db.Text)
    hackerrank= db.Column(db.Text)
    achievements= db.Column(db.Text)
    educations = db.relationship('Education',backref='user')
    user_technicals= db.relationship('User_technical',backref='user')
    user_languages= db.relationship('User_language',backref='user')
    user_courses= db.relationship('User_course',backref='user')
    user_projects= db.relationship('User_project',backref='user')
    user_jobs= db.relationship('User_job',backref='user')

class University(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name = db.Column(db.Text,nullable = False)
    educations = db.relationship('Education',backref='university')


class Degree(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.Text,nullable = False)
    educations = db.relationship('Education',backref='degree')


class Specialisation(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.Text,nullable = False)
    educations = db.relationship('Education',backref='specialisation')


class Education(db.Model):
    user_id = db.Column(db.Integer,db.ForeignKey('user.user_id'),nullable=False,primary_key=True)
    degree_id = db.Column(db.Integer,db.ForeignKey('degree.id'),nullable=False,primary_key=True)
    univ_id = db.Column(db.Integer,db.ForeignKey('university.id'),nullable=False)
    spec_id = db.Column(db.Integer,db.ForeignKey('specialisation.id'),nullable=False)
    start=db.Column(db.Date,nullable=False)
    end = db.Column(db.Date)
    marks = db.Column(db.Integer,nullable=False)
    description = db.Column (db.Text)
    deg_link = db.Column(db.Text)


class Technical(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.Text,nullable = False)
    user_technicals= db.relationship('User_technical',backref='technical')


class User_technical(db.Model):
    user_id = db.Column(db.Integer,db.ForeignKey('user.user_id'),nullable=False,primary_key=True)
    tech_id = db.Column(db.Integer,db.ForeignKey('technical.id'),nullable=False,primary_key=True)
    rating = db.Column(db.Integer,default=1)


class Language(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.Text,nullable = False)
    user_languages= db.relationship('User_language',backref='language')


class User_language(db.Model):
    user_id = db.Column(db.Integer,db.ForeignKey('user.user_id'),nullable=False,primary_key=True)
    lang_id = db.Column(db.Integer,db.ForeignKey('language.id'),nullable=False,primary_key=True)
    reading = db.Column(db.Boolean,default=0)
    writing = db.Column(db.Boolean,default=0)
    speaking = db.Column(db.Boolean,default=0)


class Course(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.Text,nullable = False)
    user_courses= db.relationship('User_course',backref='course')


class User_course(db.Model):
    user_id = db.Column(db.Integer,db.ForeignKey('user.user_id'),nullable=False,primary_key=True)
    course_id = db.Column(db.Integer,db.ForeignKey('course.id'),nullable=False,primary_key=True)
    start=db.Column(db.Date,nullable=False)
    end = db.Column(db.Date)
    certificate= db.Column(db.Text)
    institution= db.Column(db.Text, nullable = False)
    description= db.Column(db.Text, nullable = False)


class Project(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.Text,nullable = False)
    user_projects= db.relationship('User_project',backref='project')


class User_project(db.Model):
    user_id = db.Column(db.Integer,db.ForeignKey('user.user_id'),nullable=False,primary_key=True)
    project_id = db.Column(db.Integer,db.ForeignKey('project.id'),nullable=False,primary_key=True)
    start=db.Column(db.Date,nullable=False)
    end = db.Column(db.Date)
    language= db.Column(db.Text)
    software= db.Column(db.Text)
    institution= db.Column(db.Text, nullable = False) # it can be self also
    description= db.Column(db.Text, nullable = False)
    link= db.Column(db.Text)


class Job(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.Text,nullable = False)
    user_jobs= db.relationship('User_job',backref='job')


class User_job(db.Model):
    user_id = db.Column(db.Integer,db.ForeignKey('user.user_id'),nullable=False,primary_key=True)
    job_id = db.Column(db.Integer,db.ForeignKey('job.id'),nullable=False,primary_key=True)
    start=db.Column(db.Date,nullable=False)
    end = db.Column(db.Date)
    status= db.Column(db.Boolean) # 0 for job and 1 for internship
    role= db.Column(db.Text)
    salary= db.Column(db.Text)
    description= db.Column(db.Text, nullable = False)
    link= db.Column(db.Text) # company ka link agr dena ho toh
