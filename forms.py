from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired, Email, ValidationError
from flask_ckeditor import CKEditorField
from flask_ckeditor.utils import cleanify
import bleach


class TextForm(FlaskForm):
    """In this class we crate a form for text input in order to be translated. We are using flast_wtf form to do it."""
    text_introduced = StringField(label="", validators=[DataRequired()])
    submit = SubmitField("Send to translate!")

class ContactForm(FlaskForm):
    """In this class we crate a form in order to contact with webpage creator."""
    name = StringField(label="Name", validators=[DataRequired()])
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    message_data = CKEditorField(label='Message', validators=[DataRequired()])
    submit = SubmitField("Send a message!")

class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign Me Up!")

class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log Me In!")
