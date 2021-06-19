from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, validators


class NewThreadForm(FlaskForm):
    title = StringField('Title', validators=[validators.required(), validators.Length(min=5, max=40)])
    content = TextAreaField('Message', validators=[validators.required(), validators.Length(min=1, max=140)])


class UpdateThreadForm(FlaskForm):
    title = StringField('Title', validators=[validators.required(), validators.Length(min=5, max=40)])