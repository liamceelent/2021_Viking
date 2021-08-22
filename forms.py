from flask_wtf import FlaskForm
from wtforms import IntegerField, TextField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Optional, ValidationError
import models
from datetime import datetime


class Add_Movie(FlaskForm):

  def check_year(form, field):
    _current_year = int(datetime.now().year)
    if field.data > _current_year:
      raise ValidationError("You can't enter a movie from the future!")

  title = TextField('title', validators=[DataRequired()])
  year = IntegerField('year', validators=[Optional(), check_year])
  description = TextAreaField('description')


class Login_Form(FlaskForm):
  name = TextField('name', validators=[DataRequired()])
  password = TextField('password', validators=[DataRequired()])

class Forgot_Form(FlaskForm):
  email = TextField('email', validators=[DataRequired()])
