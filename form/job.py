from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField, SubmitField, IntegerField, \
    StringField, SelectField, RadioField, SelectMultipleField, FieldList, HiddenField, widgets
from wtforms.validators import DataRequired

from config import bd_path
from data import db_session
from data.users import User


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class CreateJobForm(FlaskForm):
    db_session.global_init(bd_path)
    session = db_session.create_session()
    users = session.query(User.id, User.name).all()
    team_leader = RadioField('лидер команды', validators=[DataRequired()],
                             choices=[(i[0], i[1]) for i in users], default=1)
    job = StringField('название', validators=[DataRequired()])
    work_size = SelectField('work size', validators=[DataRequired()], choices=[str(i) for i in
                                                                               range(1000)],
                            default=15)
    my_choices = [(i[0], i[1]) for i in users]
    collaborators = MultiCheckboxField(label='участники команды',
                                       choices=my_choices,
                                       coerce=int)
    is_finished = BooleanField('is finished?', default=False)
    submit = SubmitField('создать')
