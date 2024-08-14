from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap5
from forms import TextForm, ContactForm
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, ForeignKey
from morse import MorseCode
from messages import MessageSend
from wtforms import StringField, SubmitField, validators
from wtforms.validators import DataRequired, Email, ValidationError
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
Bootstrap5(app)


class Base(DeclarativeBase):
    pass
    """In class we create sqlite database"""
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///morse_db.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Morse_db(db.Model):
    __tablename__ = "morse_sheet"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    latin_sign: Mapped[str] = mapped_column(Text, nullable=True)
    morse_sign: Mapped[str] = mapped_column(Text, nullable=True)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    morseCode = MorseCode()
    for sign in morseCode.dict_morse:
        with app.app_context():
            new_sign = Morse_db(latin_sign=sign, morse_sign=morseCode.dict_morse[sign])
            db.session.add(new_sign)
            db.session.commit()
    return render_template('index.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    contact_form = ContactForm()
    if contact_form.validate_on_submit():
        receiver_email = contact_form.email.data
        name = contact_form.name.data.encode("UTF-8")
        message_text = contact_form.message_data.data.encode("UTF-8")
        message = MessageSend(receiver_email, message_text, name)
        if message:
            return render_template('contact.html', form=contact_form, confirmation=True)

    return render_template('contact.html', form=contact_form)

@app.route('/translator', methods=['GET', 'POST'])
def translator():
    text_in_form = TextForm()
    if text_in_form.validate_on_submit():
        original_text_small = []
        translated_text = []
        for sign in list(text_in_form.text_introduced.data):
            original_text_small.append(sign.lower())
        for sign in original_text_small:
            result = db.session.execute(db.select(Morse_db).where(Morse_db.latin_sign == sign)).scalar()
            if result:
                translated_text.append(result.morse_sign)
            elif sign == " ":
                translated_text.append("")
            else:
                translated_text.append(f' sign "{sign}" can not be translated')
        return render_template('translator.html', form=text_in_form, text="*".join(translated_text))

    return render_template('translator.html', form=text_in_form)

if __name__ == '__main__':
    app.run(debug=True)

