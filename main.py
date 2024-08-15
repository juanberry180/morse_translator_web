from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, ForeignKey
from morse import MorseCode
from messages import MessageSend
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from forms import TextForm, ContactForm, RegisterForm, LoginForm
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
Bootstrap5(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


class Base(DeclarativeBase):
    pass
    """In class we create sqlite database"""
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///morse_db.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Morse_db(db.Model):
    __tablename__ = "morse_code_sheet"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    latin_sign: Mapped[str] = mapped_column(Text, nullable=True)
    morse_sign: Mapped[str] = mapped_column(Text, nullable=True)

class User(UserMixin, db.Model):
    __tablename__ = "users_sheet"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))


with app.app_context():
    db.create_all()

@app.route('/')
def home():
    # morseCode = MorseCode()
    # for sign in morseCode.dict_morse:
    #     with app.app_context():
    #         new_sign = Morse_db(latin_sign=sign, morse_sign=morseCode.dict_morse[sign])
    #         db.session.add(new_sign)
    #         db.session.commit()
    return render_template('index.html', current_user=current_user)

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        result = db.session.execute(db.select(User).where(User.email == register_form.email.data))
        user = result.scalar()
        if user:
            flash('User are already registered, please log in instead')
            return redirect(url_for('login'))
        hashed_password = generate_password_hash(register_form.password.data, method='pbkdf2:sha256', salt_length=8)
        new_user = User(name=register_form.name.data, email=register_form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("home"))

    return render_template('registration.html', form=register_form, current_user=current_user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        result = db.session.execute(db.select(User).where(User.email == login_form.email.data))
        user = result.scalar()
        print(user.password)
        if not user:
            flash('Invalid email or password')
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, login_form.password.data):
            flash('Invalid password')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('home'))

    return render_template('login.html', form=login_form)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    contact_form = ContactForm()
    if contact_form.validate_on_submit():
        receiver_email = contact_form.email.data
        name = contact_form.name.data.encode("UTF-8")
        message_text = contact_form.message_data.data.encode("UTF-8")
        message = MessageSend(receiver_email, message_text, name)
        if message:
            return render_template('contact.html', form=contact_form, confirmation=True, current_user=current_user)

    return render_template('contact.html', form=contact_form, current_user=current_user)

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
        return render_template('translator.html', form=text_in_form, text="*".join(translated_text), current_user=current_user)

    return render_template('translator.html', form=text_in_form, current_user=current_user )


@app.route('/logout')
def logout():
    logout_user()
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

