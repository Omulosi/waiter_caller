from flask_wtf import Form
from wtforms import SubmitField, TextField
from wtforms import validators

class CreateTableForm(Form):
    tablenumber = TextField('tablenumber',
                            validators=[validators.DataRequired()])
    submit = SubmitField('createtablesubmit',
                        validators=[validators.DataRequired()])