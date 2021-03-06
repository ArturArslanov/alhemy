from datetime import datetime

from flask import Flask, render_template, redirect, request
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.exceptions import abort

from add_team import add_team, add_work
from data import db_session
from config import secret_key, bd_path, params
from data.jobs import Jobs
from data.users import User
from form.deportaments import CreateDepForm
from form.job import CreateJobForm
from form.login import LoginForm
from form.register import RegisterForm
from data.departments import Department

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
        db_sess.merge(user)
        db_sess.commit()
        return redirect('/')
    return render_template('create_job.html', title1='создание работы', form=form, **params)


@app.route('/addjob/<int:id>', methods=['GET', 'POST'])
@app.route('/create_job/<int:id>', methods=['GET', 'POST'])
@app.route('/updatejob/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = CreateJobForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == id).first()
        if job and current_user.id in (1, job.team_leader):
            form.job.data = job.job
            form.collaborators.data = list(map(int, job.collaborators.split(', ')))
            form.is_finished.data = job.is_finished
            form.work_size.data = str(job.work_size)
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == id).first()
        if job and current_user.id in (1, job.team_leader):
            job.job = form.job.data
            job.collaborators = ', '.join(map(str, form.collaborators.data))
            job.is_finished = form.is_finished.data
            job.work_size = form.work_size.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('create_job.html',
                           title1='Редактирование работы',
                           form=form, **params
                           )


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
                               form=form, **params)
    return render_template('login.html', title1='Авторизация', form=form, **params)


@app.route('/delete_job/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == id).first()
    if job and current_user.id in (1, job.team_leader):
        db_sess.delete(job)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/')
@app.route('/index')
def index():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    return render_template('index.html', **params, jobs=jobs)


@app.route('/departaments')
@app.route('/dep')
def dep():
    session = db_session.create_session()
    deps = session.query(Department).all()
    return render_template('dep.html', **params, deps=deps)


@app.route('/adddep', methods=['GET', 'POST'])
@app.route('/create_dep', methods=['GET', 'POST'])
def create_dep():
    form = CreateDepForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == form.chief.data).first()
        dep = Department(title=form.title.data,
                         email=form.email.data,
                         members=', '.join(map(str, form.members.data)))
        user.departments.append(dep)
        db_sess.merge(user)
        db_sess.commit()
        return redirect('/dep')
    return render_template('create_dep.html', title1='создание депортамента', form=form, **params)


@app.route('/update_dep/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_deps(id):
    form = CreateDepForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        dep = db_sess.query(Department).filter(Department.id == id).first()
        if dep and current_user.id in (1, dep.chief):
            form.title.data = dep.title
            form.members.data = list(map(int, dep.members.split(', ')))
            form.email.data = dep.email
            form.chief.data = str(dep.chief)
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        dep = db_sess.query(Department).filter(Department.id == id).first()
        if dep and current_user.id in (1, dep.chief):
            dep.title = form.title.data
            dep.members = ', '.join(map(str, form.members.data))
            dep.email = form.email.data
            dep.chief = form.chief.data
            db_sess.commit()
            return redirect('/dep')
        else:
            abort(404)
    return render_template('create_dep.html',
                           title1='Редактирование департамента',
                           form=form, **params
                           )


@app.route('/delete_dep/<int:id>', methods=['GET', 'POST'])
@login_required
def dep_delete(id):
    db_sess = db_session.create_session()
    dep = db_sess.query(Department).filter(Department.id == id).first()
    if dep and current_user.id in (1, dep.chief):
        db_sess.delete(dep)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/dep')


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
            return render_template('register.html', title1='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают", **params)
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title1='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть", **params)
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
