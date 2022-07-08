from flask import (render_template, url_for, flash,
                   redirect, Blueprint, request)
from flask_login import current_user, login_required
from doctors import db
from doctors.models import Patient, User
from doctors.patients.forms import PatientForm


patients = Blueprint('patients', __name__)

@patients.route("/patients", methods=['GET', 'POST'])
@login_required
def patient():
    
    clinic = current_user.clinic
    
    if request.method == "POST":
        patient_id = request.form.get("search")
        
        patients= Patient.query.filter_by(clinic_id=clinic.id,patient_id=patient_id)
    else:
        patients= Patient.query.filter_by(clinic_id=clinic.id)
    
    
        
    
    return render_template('patients/patients.html',patients=patients)




@patients.route("/add_patient", methods=['GET', 'POST'])
@login_required
def add_patient():

    
    
    clinic = current_user.clinic
    print(type(clinic.name),clinic.name)
    patients= Patient.query.filter_by(clinic_id=clinic.id)
        
    form = PatientForm()
    if form.validate_on_submit():
        
        patient = Patient(name=form.first_name.data,
        last_name=form.last_name.data, 
        phone=form.phone.data, 
        patient_id=form.id.data,
        birth_date= form.birth_date.data,
        gender=form.gender.data,
        occupation=form.occupation.data,
        clinic_id=clinic.id
        )
        db.session.add(patient)
        
        
        
        db.session.commit()
        
        
        db.session.commit()
        
        flash('Patient has been created!', 'success')
        return redirect(url_for('patients.add_patient'))
    
        
    return render_template('patients/add_patient.html', form=form, patients=patients)



