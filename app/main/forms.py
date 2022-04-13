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
    name = StringField('NFT Name', render_kw={'class': 'borders', 'placeholder': ' 请输入作品名称'})
    description = TextAreaField('Description', render_kw={'class': 'borders', 'placeholder': ' 请输入作品描述'})
    introduction = TextAreaField("Introduction", render_kw={'class': 'borders', 'placeholder': ' 请输入作品简介'})
    author_introduction = TextAreaField("Author_Introduction", render_kw={'class': 'borders', 'placeholder': ' 请输入作者简介'})
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
        coerce=int,
    )
    file = FileField('Upload File', render_kw={'class': 'uploading-file'})
    price = IntegerField('USD', render_kw={'class': 'borders', 'placeholder': ' 请输入作品价格'})
    submit = SubmitField('提交', render_kw={'class': 'submit-button'})


