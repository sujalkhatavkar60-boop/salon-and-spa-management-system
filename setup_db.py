import mysql.connector

# Connect to MySQL Server
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sujal123@"  # Enter your MySQL root password here
)
cursor = db.cursor()

# Create Database
cursor.execute("CREATE DATABASE IF NOT EXISTS salon_db")
cursor.execute("USE salon_db")

# Create Services Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Services (
        service_id INT AUTO_INCREMENT PRIMARY KEY,
        service_name VARCHAR(50) NOT NULL,
        price DECIMAL(10, 2) NOT NULL
    )
''')

# Create Appointments Table with Foreign Key
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Appointments (
        booking_id INT AUTO_INCREMENT PRIMARY KEY,
        customer_name VARCHAR(100) NOT NULL,
        phone VARCHAR(15) NOT NULL,
        service_id INT,
        booking_date DATE NOT NULL,
        FOREIGN KEY (service_id) REFERENCES Services(service_id)
    )
''')

# Insert Default Services if empty
cursor.execute("SELECT COUNT(*) FROM Services")
if cursor.fetchone()[0] == 0:
    services_data = [
        ('Classic Haircut', 500.00),
        ('Deep Tissue Massage', 1500.00),
        ('Basic Facial', 800.00)
    ]
    cursor.executemany("INSERT INTO Services (service_name, price) VALUES (%s, %s)", services_data)
    print("Inserted initial service items.")

db.commit()
db.close()
print("MySQL database setup completed successfully.")