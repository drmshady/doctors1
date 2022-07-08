from datetime import datetime, date
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from doctors import db, login_manager
from flask_login import UserMixin


# from doctors import db
# from doctors import create_app
# from doctors.models import *  
# db.create_all(app=create_app())

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)
    likes = db.relationship('Like', backref='user', lazy=True)
    clinic_id = db.Column(db.Integer, db.ForeignKey('clinic.id'), nullable=False)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Clinic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100), nullable=False)
    patients = db.relationship('Patient', backref='clinic', lazy=True)
    users = db.relationship('User', backref='clinic', lazy=True)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id=db.Column(db.String(100), nullable=False)
    phone=db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    last_name=db.Column(db.String(100), nullable=False)
    occupation= db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.DateTime(), nullable=False)
    gender = db.Column(db.String, nullable=False)
    clinic_id = db.Column(db.Integer, db.ForeignKey('clinic.id'), nullable=False)
    
    def age(self):
        today = date.today()
        try:
            birth_date = self.birth_date.replace(year = today.year)
            birth_date = self.birth_date.date()
        # raised when birth date is February 29
        # and the current year is not a leap year
        except ValueError:
            birth_date = birth_date.replace(year = today.year,
                month = birth_date.month + 1, day = 1)

        if birth_date > today:
            return today.year - birth_date.year - 1
        else:
            return today.year - birth_date.year


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    likes = db.relationship('Like', backref='post', lazy=True)
    comments = db.relationship('Comment', backref='post', lazy=True)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey(
        'post.id'), nullable=False)
    