from flask_wtf import Form, FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, IntegerField, FileField
from wtforms.fields import DateField, FileField
from wtforms.validators import DataRequired


class EditProfileForm(FlaskForm):
    name = StringField('Real name')
    location = StringField('Location')
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')


class UpLoadNFTForm(FlaskForm):
    name = StringField('NFT Name')
    description = TextAreaField('Description')
    introduction = TextAreaField("Introduction")
    author_introduction = TextAreaField("Author_Introduction")
    # file = FileField('Upload File', validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png',
    #                                                                          'gif', 'mp3', 'mp4',
    #                                                                          'doc', 'avi', 'pdf'])])
    file = FileField('Upload File')
    price = IntegerField('USD')
    submit = SubmitField('提交')


