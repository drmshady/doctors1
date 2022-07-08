from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, DateField
from wtforms.validators import DataRequired, ValidationError, Length
from doctors.models import Patient


def choice_query():
    return Choice.query

class PatientForm(FlaskForm):
    first_name = StringField('First name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    phone = StringField('phone',
                        validators=[DataRequired(),Length(10)])
    occupation = StringField('Occupation',
                        validators=[DataRequired()])
    birth_date = DateField('Date of birth',
                        validators=[DataRequired()])
    id = StringField('Id',
                        validators=[DataRequired()])
    gender= RadioField("Gender", choices=['Male','Female'])
    submit = SubmitField('Save')

    def validate_id(self, id):
        patient = Patient.query.filter_by(patient_id=id.data).first()
        if patient:
            raise ValidationError('That Id is taken.')