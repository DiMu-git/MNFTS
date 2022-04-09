from flask_wtf import Form, FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, IntegerField, FileField, SelectField
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
    tag = SelectField(
        label='类别',
        validators=[DataRequired('请选择标签')],
        render_kw={
            'class': 'form-control'
        },
        choices=[(1, '图片'), (2, '音频'), (3, '视频'), (4, '文档')],
        default=1,
        coerce=int
    )
    file = FileField('Upload File')
    price = IntegerField('USD')
    submit = SubmitField('提交')


