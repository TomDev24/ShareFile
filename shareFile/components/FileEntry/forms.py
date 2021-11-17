from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from flask_wtf.file import FileField
from wtforms.validators import DataRequired, Length, Email

class UploadFileForm(FlaskForm):
    filename = StringField( "File Name",
                            validators=[DataRequired(), Length(min=2, max=20)] )
    file = FileField("File", validators=[DataRequired()] )
    access_setting = SelectField('Privacy Setting', choices=[(2,"File open for everyone"), (1,"Link access"), (0,"Only for me")])
    submit = SubmitField("Upload File")
