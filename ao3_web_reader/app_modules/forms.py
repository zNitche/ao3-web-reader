from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, ValidationError, SelectField
from wtforms.validators import DataRequired
from flask_login import current_user
from ao3_web_reader.utils import works_utils
from ao3_web_reader.consts import MessagesConsts
from ao3_web_reader import models


class FormBase(FlaskForm):
    def __init__(self):
        super().__init__()

        self.html_ignored_fields = ["CSRFTokenField"]


class LoginForm(FormBase):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])


class AddWorkForm(FormBase):
    work_id = StringField("Work ID", validators=[DataRequired()])
    tag_name = SelectField("Tag", choices=[], validators=[DataRequired()])

    def validate_work_id(self, work_id):
        if not works_utils.check_if_work_exists(work_id.data):
            raise ValidationError(MessagesConsts.WORK_DOESNT_EXIST)

        work = models.Work.query.filter_by(work_id=work_id.data, owner_id=current_user.id).first()

        if work:
            raise ValidationError(MessagesConsts.WORK_ALREADY_ADDED)

    def validate_tag_name(self, tag_name):
        tag = models.Tag.query.filter_by(name=tag_name.data, owner_id=current_user.id).first()

        if not tag:
            raise ValidationError(MessagesConsts.TAG_DOESNT_EXIST)


class AddTagForm(FormBase):
    tag_name = StringField("Tag name", validators=[DataRequired()])

    def validate_tag_name(self, tag_name):
        tag = models.Tag.query.filter_by(name=tag_name.data).first()

        if tag and tag.owner_id == current_user.id:
            raise ValidationError(MessagesConsts.TAG_ALREADY_ADDED)
