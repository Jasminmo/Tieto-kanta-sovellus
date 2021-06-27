from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, TextAreaField, StringField, validators

class UserForm(FlaskForm):
    username = StringField('Username', validators=[validators.required(), validators.Length(min=5, max=100)])
    password = PasswordField('Password', validators=[validators.required(), validators.Length(min=8, max=40)])
    is_admin = BooleanField('Is admin', validators=[validators.optional()])


class ChannelForm(FlaskForm):
    title = StringField('Title', validators=[validators.required(), validators.Length(min=5, max=100)])
    description = TextAreaField('Description', validators=[validators.optional()])
    is_secret = BooleanField('Is secret', validators=[validators.optional()])


class ChannelSettingsForm(FlaskForm):
    username = StringField('Username', validators=[validators.required(), validators.Length(min=5, max=100)])


class NewThreadForm(FlaskForm):
    title = StringField('Title', validators=[validators.required(), validators.Length(min=5, max=100)])
    content = TextAreaField('Message', validators=[validators.required(), validators.Length(min=1, max=200)])


class UpdateThreadForm(FlaskForm):
    title = StringField('Title', validators=[validators.required(), validators.Length(min=5, max=100)])


class MessageForm(FlaskForm):
    content = TextAreaField('Message', validators=[validators.required(), validators.Length(min=1, max=200)])
