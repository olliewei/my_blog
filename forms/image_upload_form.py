from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import SubmitField
from wtforms.validators import DataRequired


class ImageUploadForm(FlaskForm):
    image_file = FileField('choose the image',validators=[DataRequired()])
    submit = SubmitField('Upload')
