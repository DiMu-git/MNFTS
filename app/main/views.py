import uuid

from flask import *
from sqlalchemy import or_

import app
from . import main
from .forms import EditProfileForm, UpLoadNFTForm
from flask_login import login_required, current_user
from .. import db
from ..models import User, NFT, Record
from werkzeug.utils import secure_filename
import os


@main.route('/', methods=['POST', 'GET'])
def index():
    return render_template("index.html")


def random_filename(filename) :
    ext = os.path.splitext(filename) [1]
    new_filename = uuid.uuid4().hex + ext
    return new_filename


@main.route('/userpage', methods=['POST', 'GET'])
def userpage():
    records = Record.query.filter_by(user_id=current_user.id).all()
    page = request.args.get('page', 1, type=int)
    pagination = NFT.query.filter_by(owner_id=current_user.id).paginate(
        page, per_page=current_app.config['FLASKY_NFTS_PER_PAGE_PERSONAL'],
        error_out=False
    )
    nfts = pagination.items
    return render_template("userpage.html", user=current_user, records=records,
                           nfts=nfts, User=User, pagination=pagination)


@main.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = UpLoadNFTForm()
    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        form.file.data.save(os.path.join("upload_files", filename))
        record = Record(
            type=form.tag.data,
            filename=filename,
            user_id=current_user.id,
            price=form.price.data
        )
        db.session.add(record)
        db.session.commit()
        flash('Upload success.')
        return render_template('upload.html', form=form)
    return render_template('upload.html', form=form)

@main.route('/market', methods=['GET', 'POST'])
def market():
    page = request.args.get('page', 1, type=int)
    pagination = NFT.query.order_by(NFT.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_NFTS_PER_PAGE'],
        error_out=False
    )
    nfts = pagination.items
    return render_template('market.html', nfts=nfts, User=User,
                           pagination=pagination)

@main.route('/shopping_cart', methods=['GET', 'POST'])
def shopping_cart():
    page = request.args.get('page', 1, type=int)
    pagination = NFT.query.filter_by(owner_id=current_user.id).paginate(
        page, per_page=current_app.config['FLASKY_NFTS_PER_PAGE_PERSONAL'],
        error_out=False
    )
    nfts = pagination.items
    return render_template('shopping_cart.html', nfts=nfts, User=User,
                           pagination=pagination)

@main.route('/nftpage/<int:id>', methods=['GET', 'POST'])
def nftpage(id):
    nft = NFT.query.filter_by(id=id).first()
    author = User.query.filter_by(id=nft.author_id).first()
    return render_template('nftpage.html', nft=nft, author=author,
                           )

@main.route('/buy/<int:id>', methods=['GET', 'POST'])
def buy(id):
    nft = NFT.query.filter_by(id=id).first()

    return render_template("Success.html", nft=nft)