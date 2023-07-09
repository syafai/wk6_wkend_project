from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

class UserLoginForm(FlaskForm):
    username = StringField('username', validators = [DataRequired()])
    email = StringField('email', validators = [DataRequired(), Email()])
    password = PasswordField('password', validators = [DataRequired()])
    submit_button = SubmitField()


class CharacterForm(FlaskForm):
    fname = StringField('First Name')
    lname = StringField('Last Name')
    superhero_name = StringField('Superhero Name')
    description = StringField('Description')
    weakness = StringField('Weakness')
    normal_job = StringField('Normal Job')
    team = StringField('Team')
    gender = StringField('Gender')
    submit_button = SubmitField()