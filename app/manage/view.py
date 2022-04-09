from flask import *
from flask_login import login_user, logout_user, login_required, current_user
from ..models import User, Record, NFT
from app import db
from . import manage


@manage.route('/', methods=['GET', 'POST'])
def manage():
    return render_template("index.html")