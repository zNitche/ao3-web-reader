from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired


class FormBase(FlaskForm):
    def __init__(self):
        super().__init__()

        self.html_ignored_fields = ["CSRFTokenField"]


class LoginForm(FormBase):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])


class AddWorkForm(FormBase):
    work_id = StringField("Work ID", validators=[DataRequired()])
