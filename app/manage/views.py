from flask import *
from flask_login import login_user, logout_user, login_required, current_user
from ..models import User, Record, NFT
from .forms import MintNFTForm
from app import db
from . import manage
from web3 import Web3, HTTPProvider

web3 = Web3(HTTPProvider('http://localhost:7545'))


@manage.route('/', methods=['GET', 'POST'])
def index():
    records = Record.query.all()
    print(records[0].filename)
    return render_template("manage/index.html",
                           records=records)


@manage.route('/cast/<int:id>', methods=['GET', 'POST'])
def mint():
    record = Record.query.filter_by(id=id).first()
    form = MintNFTForm(
        name=record.name,
        description=record.description,
        introduction=record.introduction,
        author_introduction=record.author_introduction,
        tag=record.tag,
        price=record.price,
    )
    if form.validate_on_submit():
        nft = NFT(
            name=form.name,
            status=True,
            user_id=record.user_id,
            price=form.price,
            timestamp=record.timestamp,
            token_id=form.address,
        )
        db.session.add(nft)
        db.session.commit()
        flash('Mint success.')
        record.status = '成功'
        return render_template('manage/index.html', form=form)
    return render_template("manage/index.html", form=form)



@manage.route('/address', methods=['GET', 'POST'])
def address():
    return jsonify("")
