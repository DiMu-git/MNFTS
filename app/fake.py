from random import randint
from sqlalchemy.exc import IntegrityError
from faker import Faker
from . import db
from .models import User, NFT


def users(count=100):
    fake = Faker()
    i = 0
    while i < count:
        u = User(email=fake.email(),
                 username=fake.user_name(),
                 password='password',
                 confirmed=True,
                 name=fake.name(),
                 location=fake.city(),
                 about_me=fake.text(),
                 member_since=fake.past_date())
        db.session.add(u)
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()


def nfts(count=100):
    fake = Faker()
    user_count = User.query.count()
    for i in range(count):
        u_id = User.query.offset(randint(0, user_count - 1)).first().id
        n = NFT(name=fake.name(),
                 timestamp=fake.past_date(),
                 author_id=u_id,
                owner_id=u_id,
                price=1,
                filename=fake.name(),
                upload_since=fake.past_date())
        db.session.add(n)
    db.session.commit()
