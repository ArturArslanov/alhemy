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


class CreateDepForm(FlaskForm):
    db_session.global_init(bd_path)
    session = db_session.create_session()
    users = session.query(User.id, User.name).all()
    chief = RadioField('шеф команды', validators=[DataRequired()],
                       choices=[(i[0], i[1]) for i in users], default=1)
    title = StringField('название', validators=[DataRequired()])
    my_choices = [(i[0], i[1]) for i in users]
    members = MultiCheckboxField(label='участники команды',
                                 choices=my_choices,
                                 coerce=int)
    email = EmailField('Почта депортамента', validators=[DataRequired()])
    submit = SubmitField('создать')
