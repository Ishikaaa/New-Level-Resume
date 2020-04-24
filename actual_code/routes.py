from flask import Blueprint,render_template, request, redirect, url_for
from werkzeug.security import check_password_hash
from .extensions import db
from flask_login import login_user,  login_required, current_user, logout_user
from .models import Admin,User,University,Degree,Specialisation,Education,Technical,User_technical,Language,User_language,User_course,Project,User_project,Job,User_job,Course
# to send message from .py file to .html file
from sqlalchemy import and_
from flask import Markup,flash,session
import datetime
from cryptography.fernet import Fernet

main = Blueprint('main',__name__)

main.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
key = Fernet.generate_key() #this is your "password"
cipher_suite = Fernet(key)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/login' , methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['log_username'].lower()
        password = request.form['log_password']
        if  username.count("@")==1:  
            admin = Admin.query.filter_by(username=username).first()
            if admin:
                if check_password_hash(admin.password,password):
                    login_user(admin)                                                    
                    return redirect(url_for('main.success'))
                else:
                    message = Markup("You entered wrong password")
                    flash(message)
                    return redirect(url_for('main.login'))
            else:
                message = Markup("You are not registered with us")
                flash(message)
                return redirect(url_for('main.login'))          
        else:
                message = Markup("Enter valid username")
                flash(message)
                return redirect(url_for('main.login'))
    return render_template('login.html')

@main.route('/register', methods = ['GET','POST'])
def register():
    if request.method == 'POST':
        name=request.form['register_username']
        password=request.form['register_password']
        question = request.form['register_question']
        answer = request.form['register_answer']
        if name.count("@")==1:
            try:
                admin = Admin.query.filter_by(username=name).first()
                if not admin: #because if admin is not found it does not throws error but returns NONE
                    raise error
                message = Markup("This username is already registered")
                flash(message)
                return render_template('login.html')
            except:
                if name.split("@")[0].lower()!="admin":
                    string = "admin@"+name.split("@")[1]
                    admin = Admin.query.filter_by(username=string).first()
                    if not admin:
                        flash("The domain name is not registered")
                        return render_template('login.html')
                if name.split("@")[0].lower()=="admin":
                    admin = Admin(username = name.lower(), unhashed_password = password,question=question.lower(), unhashed_answer = answer.lower(),role=1)
                else:
                    admin = Admin(username = name.lower(), unhashed_password = password,question=question.lower(), unhashed_answer = answer.lower())
                db.session.add(admin)
                db.session.commit()  
                message = Markup("Thanks for registration as admin!<br/>Wait for permission")
                flash(message)
                return redirect(url_for('main.login'))
        else:
            message = Markup("Enter valid username")
            flash(message)
            return redirect(url_for('main.login'))

    return render_template('login.html')

@main.route('/forget', methods = ['GET','POST'])
def forget():
    if request.method=='POST':
        name = request.form['username']
        question = request.form['question']
        answer = request.form['answer']
        if (name.count("@")==1):
            admin=Admin.query.filter_by(username=name.lower()).first()
            if admin and admin.question==question and check_password_hash(admin.answer,answer):
                error="Next Page"
                arr = bytes(admin.username, 'utf-8')                 # converting string into bytes
                session['name_user'] = cipher_suite.encrypt(arr)    # encrypting_text and storing in session                
                return render_template('forget.html',error=error)
            else:
                flash('Your details are incorrect1')
                return redirect(url_for('main.forget'))
        else:
            flash('Your details are incorrect2')
            return redirect(url_for('main.forget'))
    flash("")
    return render_template('forget.html')

@main.route('/forget1', methods = ['POST'])
def forget1():       
    username = session['name_user']
    session.pop('name_user', None)
    session.clear()
    new_password=request.form['new_password']
    repeat_password=request.form['repeat_password']
    decoded_text = cipher_suite.decrypt(username).decode("utf-8")  #decrypt username stored in session
    admin = Admin.query.filter_by(username=decoded_text).first()
    admin.unhashed_password=new_password
    db.session.add(admin)
    db.session.commit()
    flash('Password Changed')
    return redirect(url_for('main.login'))


@main.route('/success', methods = ["GET",'POST'])
@login_required
def success():
    name=current_user.username
    if name.split("@")[0].lower()=="admin":
        pending=Admin.query.filter(and_(Admin.username.startswith("admin@"), Admin.active == 0)).all()
        approved=Admin.query.filter(and_(Admin.username.startswith("admin@"),Admin.active == 1)).all()
        return render_template("adminsuccess.html",pending=pending,approved=approved)
    elif name.split("@")[0].lower!="admin":
        user_id=current_user.id 
        user=User.query.filter_by(user_id=user_id).first()
        return render_template('usersuccess.html',user=user)
    return render_template('usersuccess.html')

@main.route("/get_data",methods=["POST"])
@login_required
def getdata():
    user_id = current_user.id 
    name = request.form['user_name']
    about= request.form['user_about']
    address= request.form['user_address']
    email= request.form['user_email']
    phone= request.form['user_phone']
    github= request.form['user_github']
    resume= request.form['user_resume']
    linkedin= request.form['user_linkedin']
    hackerrank= request.form['user_hackerrank']
    achievements= request.form['user_achievements']
    user=User.query.filter_by(user_id=user_id).first()
    if user:
        user.name=name
        user.about=about
        user.address=address
        user.email=email
        user.phone=phone
        user.github=github
        user.resume=resume
        user.linkedin=linkedin
        user.hackerrank=hackerrank
        user.achievements=achievements
    else:
        user=User(user_id=user_id,name=name,about=about,address=address,email=email,phone=phone,github=github,resume=resume,linkedin=linkedin,hackerrank=hackerrank,achievements=achievements)
        db.session.add(user)
    db.session.commit()  
    return redirect(url_for('main.success'))

@main.route("/get_education",methods=["POST"])
@login_required
def getEducation():
    univer = request.form["user_education_university"].lower()
    degree = request.form["user_education_degree"].lower()
    spec = request.form["user_education_specialization"].lower()
    degree_data=Degree.query.filter_by(name=degree).first()
    uni_data = University.query.filter_by(name=univer).first()
    spec_data = Specialisation.query.filter_by(name=spec).first()
    if not degree_data:
        deg = Degree(name=degree)
        db.session.add(deg)
        db.session.commit()  
        degree_data=Degree.query.filter_by(name=degree).first()
    if not uni_data:
        uni = University(name=univer)
        db.session.add(uni)
        db.session.commit()  
        uni_data = University.query.filter_by(name=univer).first()
    if not spec_data:
        spe = Specialisation(name=spec)
        db.session.add(spe)
        db.session.commit()  
        spec_data = Specialisation.query.filter_by(name=spec).first()
    user_id = current_user.id
    degree_id = degree_data.id
    univ_id = uni_data.id
    spec_id = spec_data.id
    start=datetime.datetime.strptime(request.form['user_education_startdate'], "%Y-%m").date()
    end=datetime.datetime.strptime(request.form['user_education_enddate'], "%Y-%m").date()
    marks= request.form['user_education_marks']
    description = request.form['user_education_description']
    deg_link = request.form['user_education_certificate']
    edu = Education(user_id=user_id,degree_id=degree_id,univ_id=univ_id,spec_id=spec_id,start=start,end=end,marks=marks,description=description,deg_link=deg_link)
    db.session.add(edu)
    db.session.commit()  
    return redirect(url_for('main.success'))

@main.route("/get_technical",methods=["POST"])
@login_required
def getTechnical():
    tech_name=request.form["user_skills"].lower()
    tech=Technical.query.filter_by(name=tech_name).first()
    if not tech:
        tech = Technical(name=tech_name)
        db.session.add(tech)
        db.session.commit()  
        tech=Technical.query.filter_by(name=tech_name).first()
    user_id = current_user.id
    tech_id = tech.id
    rating = request.form["user_rating"]
    tech=User_technical(user_id=user_id,tech_id=tech_id,rating=rating)
    db.session.add(tech)
    db.session.commit()  
    return redirect(url_for('main.success'))

@main.route("/get_language",methods=["POST"])
@login_required
def get_language():
    language = request.form["user_languages"].lower()
    lang = Language.query.filter_by(name=language).first()
    if not lang:
        lang = Language(name=language)
        db.session.add(lang)
        db.session.commit()  
        lang=Language.query.filter_by(name=language).first()
    user_id=current_user.id 
    lang_id=lang.id
    reading =int(request.form["user_reading"])
    writing = int(request.form["user_writing"])
    speaking = int(request.form["user_speaking"])
    lang = User_language(user_id=user_id,lang_id=lang_id,reading=reading,writing=writing,speaking=speaking)
    db.session.add(lang)
    db.session.commit()  
    return redirect(url_for('main.success'))
    
@main.route("/get_course",methods=["POST"])
@login_required
def get_course():
    course = request.form["user_course_name"].lower()
    cour = Course.query.filter_by(name=course).first()
    if not cour:
        cour = Course(name=course)
        db.session.add(cour)
        db.session.commit()  
        cour=Course.query.filter_by(name=course).first()
    user_id = current_user.id
    course_id = cour.id
    start=datetime.datetime.strptime(request.form['user_course_startdate'], "%Y-%m").date()
    end=datetime.datetime.strptime(request.form['user_course_enddate'], "%Y-%m").date()
    certificate = request.form["user_course_certificate_url"]
    institution = request.form["user_course_institutename"]
    description = request.form["user_course_description"]
    cour = User_course(user_id=user_id,course_id=course_id,start=start,end=end,certificate=certificate,institution=institution,description=description)
    db.session.add(cour)
    db.session.commit()  
    return redirect(url_for('main.success'))

@main.route("/get_project",methods=["POST"])
@login_required
def get_project():
    project = request.form["user_project_name"].lower()
    proj = Project.query.filter_by(name=project).first()
    if not proj:
        proj = Project(name=project)
        db.session.add(proj)    
        db.session.commit()  
        proj=Project.query.filter_by(name=project).first()
    user_id = current_user.id
    project_id = proj.id
    start=datetime.datetime.strptime(request.form['user_project_startdate'], "%Y-%m").date()
    end=datetime.datetime.strptime(request.form['user_project_enddate'], "%Y-%m").date()
    language= request.form["user_project_language"]
    software= request.form["user_project_software"]
    institution= request.form["user_project_institution"]
    description= request.form["user_project_description"]
    link= request.form["user_project_link"]
    proj = User_project(user_id=user_id,project_id=project_id,start=start,end=end,language=language,software=software,institution=institution,description=description,link=link)
    db.session.add(proj)
    db.session.commit()  
    return redirect(url_for('main.success'))

@main.route("/get_job",methods=["POST"])
@login_required
def get_job():
    job = request.form["user_job_company_name"].lower()
    j = Job.query.filter_by(name=job).first()
    if not j:
        j = Job(name=job)
        db.session.add(j)
        db.session.commit()  
        j=Job.query.filter_by(name=job).first()
    user_id = current_user.id
    job_id = j.id
    start=datetime.datetime.strptime(request.form['user_job_startdate'], "%Y-%m").date()
    end=datetime.datetime.strptime(request.form['user_job_enddate'], "%Y-%m").date()
    status= request.form["user_job_status"]
    role= request.form["user_job_role"]
    salary= request.form["user_job_salary"]
    description= request.form["user_job_description"]
    link= request.form["user_job_link"]
    if status.lower()=='internship':
        status_bool=1
    else:
        status_bool=0
    j = User_job(user_id=user_id,job_id=job_id,start=start,end=end,status=status_bool,role=role,salary=salary,description=description,link=link)
    db.session.add(j)
    db.session.commit()  
    return redirect(url_for('main.success'))

@main.route("/changeAnswer",methods=["POST"])
@login_required
def changeAnswer():
    new_question=request.form['user_new_question']
    new_answer=request.form['user_new_answer']
    admin = Admin.query.filter_by(username=current_user.username).first()
    admin.unhashed_answer=new_answer
    admin.question=new_question
    db.session.add(admin)
    db.session.commit()
    return redirect(url_for('main.success'))

@main.route("/changePassword",methods=["POST"])
@login_required
def changePassword():
    new_password=request.form['user_new_password']
    admin = Admin.query.filter_by(username=current_user.username).first()
    admin.unhashed_password=new_password
    db.session.add(admin)
    db.session.commit()
    return redirect(url_for('main.success'))

@main.route('/approve/<int:id>',methods = ["POST"])
@login_required
def approve(id):
    user = Admin.query.get(id)
    return redirect(url_for('main.success'),user=user)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main.route('/', defaults={'path': ''})
@main.route('/<path:path>')
def catch_all(path):    
    return render_template('not_found.html')

