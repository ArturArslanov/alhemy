from datetime import datetime

from data.users import User
from data.jobs import Jobs


def add_team(db_session):
    session = db_session.create_session()
    user = User()
    user.surname = "Scott"
    user.name = "Ridley"
    user.age = 21
    user.position = "captain"
    user.speciality = "research engineer"
    user.address = "module_1"
    user.email = "scott_chief@mars.org"
    user.set_password("cap")
    session.add(user)
    session.commit()

    user = User()
    user.surname = "Marli"
    user.name = "Rayner"
    user.age = 25
    user.position = "colonist"
    user.speciality = "dragon pilot"
    user.address = "module_3"
    user.email = "Rayner_ray@mars.org"
    user.set_password("i`m_armored")
    session.add(user)
    session.commit()

    user = User()
    user.surname = "Holmes"
    user.name = "Sherlock"
    user.age = 25
    user.position = "colonist"
    user.speciality = "detective consultant"
    user.address = "module_2"
    user.email = "Sheri_shegi@mars.org"
    user.set_password('I`m_sherlocked')
    session.add(user)
    session.commit()

    user = User()
    user.surname = "Watson"
    user.name = "John"
    user.age = 28
    user.position = "colonist"
    user.speciality = "doctor"
    user.address = "module_4"
    user.email = "John_John@mars.org"
    user.set_password('i_Love_Mary_Morstn')
    session.add(user)
    session.commit()


def add_work(db_session):
    session = db_session.create_session()
    user = session.query(User).filter(User.id == 1).first()
    job = Jobs()
    job.job = 'deployment of residential modules 1 and 2'
    job.work_size = 15
    job.collaborators = '2, 3'
    user.jobs.append(job)
    session.commit()

    user = session.query(User).filter(User.id == 2).first()
    job = Jobs()
    job.job = 'deployment of residential modules 3 and 2'
    job.work_size = 15
    job.collaborators = '1, 3'
    job.is_finished = True
    job.end_date = datetime.today()
    user.jobs.append(job)
    session.commit()
