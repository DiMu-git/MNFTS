import hashlib

from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from datetime import datetime


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(32))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    admin = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(32))
    location = db.Column(db.String(32))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow())
    records = db.relationship('Record', backref='user', lazy='dynamic')
    block_address = db.Column(db.String(64), default="")


    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def gravatar_hash(self):
        return hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()

    def gravatar(self, size=100, default='identicon', rating='g'):
        url = 'https://secure.gravatar.com/avatar'
        hash = self.gravatar_hash()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)

    def __init__(self, **kwargs):

        super(User, self).__init__(**kwargs)
        if self.email == current_app.config['MAIL_USERNAME']:
            self.admin = True
        else:
            self.admin = False


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# status是数字艺术品的上架
# True代表已上架
# False代表待审核
class NFT(db.Model):
    __tablename__ = 'nfts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    status = db.Column(db.Boolean, default=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    price = db.Column(db.Integer(), default=0)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    token_id = db.Column(db.String(64), default="")
    description = db.Column(db.String(64))
    introduction = db.Column(db.String(64))
    author_introduction = db.Column(db.String(64))





class Record(db.Model):
    __tablename__ = 'records'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer())
    status = db.Column(db.Enum(
        '审核中', '成功', '失败'
    ), server_default='审核中')
    filename = db.Column(db.String(64), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    price = db.Column(db.Integer(), default=0)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    name = db.Column(db.String(32))
    description = db.Column(db.String(64))
    introduction = db.Column(db.String(64))
    author_introduction = db.Column(db.String(64))


