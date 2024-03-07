from flask import Flask, render_template, request
from flask import Flask, jsonify
import pymysql
from datetime import datetime



import mysql.connector

app = Flask(__name__)

# MySQL connection configuration
conn = mysql.connector.connect(
    host='3.110.40.237',
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

if __name__ == '__main__':
    app.run(debug=True) 


