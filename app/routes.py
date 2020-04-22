from random import randint
from datetime import datetime, timedelta
from flask import jsonify, render_template, request, redirect, flash, session, url_for
from app import app, db, login_manager, bcrypt
from .models import Event, User
from .forms import EventForm, LoginForm
from flask_login import login_user, current_user

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.get(form.email.data)
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                user.authenticated = True
                login_user(user, remember=True)
                return redirect("/")
    return render_template("login.html", form=form)

@app.route("/create_user", methods=["GET", "POST"])
def create_user():
    form = LoginForm()
    print('we are here')
    if request.method == 'POST':
        print('try to submit')
        if form.validate_on_submit():
            print('done!')
            email = request.form.get('email')
            password = request.form.get('password')
            user = User(email=email, password=bcrypt.generate_password_hash(password).decode('utf-8'))
            db.session.add(user)
            db.session.commit()
            return redirect("/login")
    return render_template("create_user.html", form=form)



@app.route('/', methods=["GET", "POST"])
def index():
    events = db.session.query(Event).order_by(Event.start.desc()).all()
    if current_user:
        user = current_user.email
    return render_template('index.html', events=events, user=user)

@app.route('/add_event', methods=['POST', 'GET'])
def add_event():
    event_form = EventForm()
    if request.method == 'POST':
        if event_form.validate_on_submit():
            author = current_user.email
            start = request.form.get('start')
            start_format = datetime.strptime(start, '%Y-%m-%d')
            end = request.form.get('end')
            end_format = datetime.strptime(end, '%Y-%m-%d')
            title = request.form.get('title')
            text = request.form.get('text')
            event = Event(
                author=author, 
                start=start_format, 
                end=end_format, 
                title=title, 
                text=text)
            db.session.add(event)
            db.session.commit()
            return redirect('/')
        error = "Form was not validated"
        return render_template('error.html',form=event_form, error = error)        
    return render_template('add_event.html', form=event_form)

@app.route('/event/<int:event_id>', methods=['GET', 'POST'])
def event(event_id):
    event = db.session.query(Event).filter(Event._id==int(event_id)).first()
    event_form = EventForm(obj=event)
    if request.method == 'POST':
        if event and event_form.validate(): 
            author = event.author
            if author != current_user.email:
                error = "You can't edit this event. Access error."
                return render_template('error.html',form=event_form, error = error)
            start = request.form.get('start')
            start_format = datetime.strptime(start, '%Y-%m-%d')
            end = request.form.get('end')
            end_format = datetime.strptime(end, '%Y-%m-%d')
            title = request.form.get('title')
            text = request.form.get('text')
            event.title = title
            event.text = text
            event.start = start_format
            event.end = end_format
            db.session.commit()
            return redirect('/')
        error = "Form was not validated"
        return render_template('error.html',form=event_form, error = error)        
    return render_template('edit_event.html', form=event_form)