from random import randint
from sqlalchemy.exc import IntegrityError
from faker import Faker
from . import db
from .models import User, NFT

Faker.seed(0)
fake = Faker(['it_IT', 'en_US', 'ja_JP', 'zh_TW'])

def users(count=10):
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
                price=fake.random_number(fix_len=False),
                token_id=fake.sha256(raw_output=False),
                status=True,
                description=fake.text(),
                introduction=fake.text(),
                author_introduction=fake.text()
                )
        db.session.add(n)
    db.session.commit()
