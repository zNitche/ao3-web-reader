from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, ValidationError
from wtforms.validators import DataRequired
from ao3_web_reader.utils import works_utils
from ao3_web_reader.consts import MessagesConsts


class FormBase(FlaskForm):
    def __init__(self):
        super().__init__()

        self.html_ignored_fields = ["CSRFTokenField"]


class LoginForm(FormBase):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])


class AddWorkForm(FormBase):
    work_id = StringField("Work ID", validators=[DataRequired()])

    def validate_work_id(self, work_id):
        if not works_utils.check_if_work_exists(work_id.data):
            raise ValidationError(MessagesConsts.WORK_DOESNT_EXIST)
