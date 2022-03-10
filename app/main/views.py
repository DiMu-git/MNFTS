import uuid

from flask import *
from sqlalchemy import or_

import app
from . import main
from .forms import EditProfileForm, UpLoadNFTForm
from flask_login import login_required, current_user
from .. import db
from ..models import User, NFT
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
    nft = NFT.query.filter_by(author_id=current_user.id).first()
    return render_template("userpage.html", user=current_user, nft=nft)

@main.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UpLoadNFTForm()
    if form.validate_on_submit():
        f = form.file.data
        filename = random_filename(f.filename)
        f.save(os.path.join("upload_files", filename))
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
    return render_template('market.html', nfts=nfts,User=User,
                           pagination=pagination)

@main.route('/nftpage/<int:id>', methods=['GET', 'POST'])
def nftpage(id):
    nft = NFT.query.filter_by(id=id).first()
    author=User.query.filter_by(id=nft.author_id).first()
    return render_template('nftpage.html', nft=nft,author=author,
                           )
