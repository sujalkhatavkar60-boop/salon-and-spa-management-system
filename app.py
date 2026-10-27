from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sujal123@",  # Match your MySQL root password
        database="salon_db"
    )

@app.route('/', methods=['GET', 'POST'])
def index():
    db = get_db_connection()
    cursor = db.cursor()

    if request.method == 'POST':
        name = request.form['customer_name']
        phone = request.form['phone']
        service_id = request.form['service_id']
        date = request.form['booking_date']

        query = "INSERT INTO Appointments (customer_name, phone, service_id, booking_date) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (name, phone, service_id, date))
        db.commit()
        cursor.close()
        db.close()
        return "<h3>Booking Confirmed!</h3><a href='/'>Book Another</a> | <a href='/admin'>Go to Admin</a>"

    cursor.execute("SELECT * FROM Services")
    services = cursor.fetchall()
    cursor.close()
    db.close()

    return render_template('index.html', services=services)

@app.route('/admin')
def admin():
    db = get_db_connection()
    cursor = db.cursor()

    sql_join_query = '''
        SELECT 
            Appointments.booking_id, 
            Appointments.customer_name, 
            Appointments.phone, 
            Services.service_name, 
            Appointments.booking_date
        FROM Appointments
        JOIN Services ON Appointments.service_id = Services.service_id
        ORDER BY Appointments.booking_date ASC
    '''
    cursor.execute(sql_join_query)
    appointments = cursor.fetchall()
    cursor.close()
    db.close()

    return render_template('admin.html', appointments=appointments)

if __name__ == '__main__':
    app.run(debug=True)