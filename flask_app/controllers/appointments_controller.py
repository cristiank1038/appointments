from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.appointments import Appointment
from flask_app.models.users import User

@app.route('/appointments/add')
def new_appointment():
    if 'usuario_id' not in session:
        return redirect('/')

    formulario = {
        "id": session['usuario_id']
    }
    user = User.get_by_id(formulario)
    return render_template('new_appointment.html', user = user)

@app.route('/create/appointment', methods = ['POST'])
def create_appointment():
    if 'usuario_id' not in session:
        return redirect('/')
    
    if not Appointment.validate_appointment(request.form):
        return redirect('/appointments/add')
    
    Appointment.save(request.form)
    return redirect('/appointments')

@app.route('/edit/appointment/<int:id>')
def edit_appointment(id):
    if 'usuario_id' not in session:
        return redirect('/')
    
    formulario = {
        "id": session['usuario_id']
    }
    user = User.get_by_id(formulario)
    formulario_task = { "id": id }
    appointment = Appointment.get_by_id(formulario_task)
    return render_template('edit_appointment.html', user = user, appointment = appointment)

@app.route('/delete/appointment/<int:id>')
def delete_appointment(id):
    if 'usuario_id' not in session:
        return redirect('/')
    
    formulario_task = { "id": id }
    Appointment.delete(formulario_task)
    return redirect('/appointments')

@app.route('/update/appointment', methods=['POST'])
def update_appointment():
    if 'usuario_id' not in session:
        return redirect('/')
    
    if not Appointment.validate_appointment(request.form):
        return redirect('/edit/appointment/'+request.form['id'])
    
    Appointment.update(request.form)
    return redirect('/appointments')