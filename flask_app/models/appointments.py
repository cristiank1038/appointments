from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from datetime import date, datetime

class Appointment:
    def __init__(self, data):
        self.id = data ['id']
        self.task_name = data['task_name']
        self.task_date = data['task_date']
        self.status = data['status']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    def time_validator(self):
        now = datetime.today()
        return now

    @classmethod
    def save(cls, formulario):
        query = "INSERT INTO appointments (task_name, task_date, status, user_id) VALUES (%(task_name)s, %(task_date)s, %(status)s, %(user_id)s)"
        newId = connectToMySQL('esquema_appointments').query_db(query, formulario)
        return newId

    #Me trae todas las tareas de todos los usuarios
    @classmethod
    def get_user_tasks(cls, formulario):
        query = "SELECT appointments.*, first_name FROM appointments LEFT JOIN users ON users.id = appointments.user_id;"
        results = connectToMySQL('esquema_appointments').query_db(query, formulario)
        appointments = []
        for appointment in results:
            appointments.append(cls(appointment))
        return appointments
    
    #Me trae solo las tareas filtradas por usuario en sesión
    @classmethod
    def get_tasks(cls, formulario):
        query = "SELECT appointments.*, first_name FROM appointments LEFT JOIN users ON users.id = appointments.user_id WHERE user_id = %(id)s;"
        results = connectToMySQL('esquema_appointments').query_db(query, formulario)
        appointments = []
        for appointment in results:
            appointments.append(cls(appointment))
        return appointments

    @classmethod
    def get_by_id(cls, formulario):
        query = "SELECT appointments.*, first_name FROM appointments LEFT JOIN users ON users.id = appointments.user_id WHERE appointments.id = %(id)s"
        result = connectToMySQL('esquema_appointments').query_db(query, formulario)
        appointment = cls(result[0]) #Creamos una instancia de la tarea
        return appointment

    @classmethod
    def delete(cls, formulario):
        query = "DELETE FROM appointments WHERE id = %(id)s"
        result = connectToMySQL('esquema_appointments').query_db(query, formulario)
        return result
    
    @classmethod
    def update(cls, formulario):
        query = "UPDATE appointments SET task_name = %(task_name)s, task_date = %(task_date)s, status = %(status)s WHERE id = %(id)s"
        result = connectToMySQL('esquema_appointments').query_db(query, formulario)
        return result

    @staticmethod
    def validate_appointment(formulario):
        is_valid = True
        
        if len(formulario['task_name']) < 3:
            flash('The task name must have at least 3 characters', "tarea")
            is_valid = False
        
        if formulario['task_date'] == "":
            flash("Please enter a date", "tarea")
            is_valid = False
            
        if len(formulario['status']) < 1:
            flash('Must choose a status', "tarea")
            is_valid = False

        return is_valid