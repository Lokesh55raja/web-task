from flask import Flask, render_template, request, jsonify
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# MySQL connection configuration
conn = mysql.connector.connect(
    host='13.201.193.4',
    user='Lokie',
    password='Lokie#2000',
    database='studentdb'
)

# Function to insert student registration data into the database
@app.route('/add_student', methods=['POST'])
def add_student():
    if request.method == 'POST':
        # get form data
        registration_number = request.form['regNo']
        student_name = request.form['studentName']
        class_name = request.form['classs']
        cursor = conn.cursor()
        # Execute the INSERT query
        query = "INSERT INTO student_registration (registration_number, student_name, class) VALUES (%s, %s, %s)"
        values = (registration_number, student_name, class_name)
        cursor.execute(query, values)

        conn.commit() 
        cursor.close()

        return render_template('button.html')
    else:
        return render_template('button.html')

#Function to insert attendance.html data into the database
@app.route('/add_attendance', methods=['POST'])
def add_attendance():
    try:
        if request.method == 'POST':
            # Retrieve data from the form
            student_ids = request.form.getlist('student_id')
            names = request.form.getlist('name')
            attendances = request.form.getlist('attendance')
            date = request.args.get('date')  # Get the date from the request parameters

            # Check if all required fields are provided
            if not all(student_ids) or not all(names) or not all(attendances) or not date:
                return jsonify({'success': False, 'message': 'Missing data'})

            # Execute SQL query to insert attendance data
            cursor = conn.cursor()
            insert_query = "INSERT INTO student_table (student_id, name, attendance, date) VALUES (%s, %s, %s, %s)"
            
            # Iterate over the data lists and insert each record into the database
            for student_id, name, attendance in zip(student_ids, names, attendances):
                cursor.execute(insert_query, (student_id, name, attendance, date))

            # Commit  and close the cursor
            conn.commit()
            cursor.close()

            return jsonify({'success': True, 'message': 'Attendance added successfully'})
        else:
            return jsonify({'success': False, 'message': 'Invalid request method'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})


@app.route('/')
def home():
    return render_template('login.html')

@app.route('/button')
def button():
    return render_template('button.html')

@app.route('/attendance')
def attendance():
    return render_template('attendance.html')
    
@app.route('/register')
def register():
    return render_template('register.html')

#Function to insert attendance.html db into the view attendance log
@app.route('/get_students', methods=['GET']) 
def get_students():
    try:
        date_str = request.args.get('date')
        if not date_str:
            date_str = datetime.now().date().isoformat()  # If no date provided, use today's date

        cursor = conn.cursor()
        query = "SELECT student_id, name, attendance FROM student_table WHERE date = %s"
        cursor.execute(query, (date_str,))
        data = cursor.fetchall()
        cursor.close()
        return jsonify({'success': True, 'students': data})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})
    
@app.route('/view_attendance')
def view_attendance():
    return render_template('view_attendance.html')

#Function to insert student registration db into the attendance.html page view
@app.route('/get_students_registration', methods=['GET']) 
def get_students_registration():
    try:
        cursor = conn.cursor()
        query = "SELECT  registration_number, student_name FROM student_registration"
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        students = [{'student_id': student[0], 'name': student[1]} for student in data]
        return jsonify({'success': True, 'students': students})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


if __name__ == '__main__':
    app.run(debug=True) 
