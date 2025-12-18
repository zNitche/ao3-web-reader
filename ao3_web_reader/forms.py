from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, ValidationError, SelectField
from wtforms.validators import DataRequired
from ao3_web_reader.utils import works_utils
from ao3_web_reader.consts import MessagesConsts
from ao3_web_reader import models


class FormBase(FlaskForm):
    def __init__(self, user: models.User | None = None):
        super().__init__()

        self._user = user

        self.html_ignored_fields = ["CSRFTokenField"]


class LoginForm(FormBase):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])


class AddWorkForm(FormBase):
    work_id = StringField("Work ID", validators=[DataRequired()])
    tag_name = SelectField("Tag", choices=[], validators=[DataRequired()])

    def validate_work_id(self, work_id):
        if not self._user:
            raise Exception("error while validating work_id, user is None")

        if not works_utils.check_if_work_is_accessible(work_id.data):
            raise ValidationError(MessagesConsts.CANT_ACCESS_WORK)

        work = models.Work.query.filter_by(work_id=work_id.data, owner_id=self._user.id).first()

        if work:
            raise ValidationError(MessagesConsts.WORK_ALREADY_ADDED)

    def validate_tag_name(self, tag_name):
        if not self._user:
            raise Exception("error while validating tag_name, user is None")

        tag = models.Tag.query.filter_by(name=tag_name.data, owner_id=self._user.id).first()

        if not tag:
            raise ValidationError(MessagesConsts.TAG_DOESNT_EXIST)


class AddTagForm(FormBase):
    tag_name = StringField("Tag name", validators=[DataRequired()])

    def validate_tag_name(self, tag_name):
        if not self._user:
            raise Exception("error while validating tag_name, user is None")

        tag = models.Tag.query.filter_by(name=tag_name.data).first()

        if tag and tag.owner_id == self._user.id:
            raise ValidationError(MessagesConsts.TAG_ALREADY_ADDED)
