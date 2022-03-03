from datetime import datetime

from flask import Flask, render_template, redirect
from flask_login import login_user, LoginManager, login_required, logout_user

from add_team import add_team, add_work
from data import db_session
from config import secret_key, bd_path, params
from data.jobs import Jobs
from data.users import User
from form.job import CreateJobForm
from form.login import LoginForm
from form.register import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key
login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init(bd_path)
    session = db_session.create_session()
    if not bool(session.query(User).all()):
        add_team(db_session)
    if not bool(session.query(Jobs).all()):
        add_work(db_session)

    app.run(port=8081, host='127.0.0.2')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/addjob', methods=['GET', 'POST'])
@app.route('/create_job', methods=['GET', 'POST'])
def create_job():
    form = CreateJobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == form.team_leader.data).first()
        job = Jobs(job=form.job.data,
                   work_size=form.work_size.data,
                   collaborators=', '.join(map(str, form.collaborators.data)))
        user.jobs.append(job)
        db_sess.commit()
        return redirect('/')
    return render_template('create_job.html', title='Авторизация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/')
@app.route('/index')
def index():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    return render_template('index.html', **params, jobs=jobs)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            address=form.address.data,
            speciality=form.speciality.data,
            position=form.position.data,
            age=form.age.data,
            surname=form.surname.data)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('register.html', title1='Регистрация', form=form, **params)


if __name__ == '__main__':
    main()
