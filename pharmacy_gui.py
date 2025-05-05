from flask import Flask, render_template, request, redirect, url_for, flash
import pyodbc
from flask import jsonify

app = Flask(__name__)
app.secret_key = "supersecretkey"

class PharmacyApp:
    def __init__(self):
        self.conn_str = (
            r"DRIVER={ODBC Driver 17 for SQL Server};"
            r"SERVER=ABUOELHASSAN\SQLEXPRESS;"
            r"DATABASE=PharmacySystem;"
            r"UID=sa;"
            r"PWD=Aa123456789;"
            r"TrustServerCertificate=yes;"
            r"Connection Timeout=30;"
            r"Encrypt=yes;"
        )

    def get_medicine_names(self):
        try:
            connection = pyodbc.connect(self.conn_str)
            cursor = connection.cursor()
            cursor.execute("SELECT DISTINCT Name FROM Medicines")
            medicines = [row.Name for row in cursor.fetchall()]
            cursor.close()
            connection.close()
            return medicines
        except Exception as e:
            print(f"Error fetching medicine names: {e}")
            return []

pharmacy_app = PharmacyApp()

@app.route('/')
def login_screen():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if not username or not password:
        flash("Please fill all fields!")
        return redirect(url_for('login_screen'))

    try:
        connection = pyodbc.connect(pharmacy_app.conn_str)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM Admins WHERE Username = ? AND Password = ?", (username, password))
        admin = cursor.fetchone()
        if admin:
            cursor.close()
            connection.close()
            return redirect(url_for('admin_screen'))

        cursor.execute("SELECT * FROM Patients WHERE Username = ? AND Password = ?", (username, password))
        patient = cursor.fetchone()
        if patient:
            cursor.close()
            connection.close()
            return redirect(url_for('patient_screen'))

        flash("Invalid username or password!")
        cursor.close()
        connection.close()
        return redirect(url_for('login_screen'))

    except Exception as e:
        flash(str(e))
        return redirect(url_for('login_screen'))

@app.route('/admin')
def admin_screen():
    return render_template('admin.html')

@app.route('/add_pharmacy', methods=['POST'])
def add_pharmacy():
    name = request.form['pharmacy_name']
    address = request.form['pharmacy_address']
    phone = request.form['pharmacy_phone']

    if name and address:
        try:
            connection = pyodbc.connect(pharmacy_app.conn_str)
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO Pharmacies (Name, Address, Phone) VALUES (?, ?, ?)",
                (name, address, phone)
            )
            connection.commit()
            flash("Pharmacy added successfully!")
            cursor.close()
            connection.close()
        except Exception as e:
            flash(str(e))
    else:
        flash("Please fill Name and Address!")
    return redirect(url_for('admin_screen'))

@app.route('/add_medicine', methods=['POST'])
def add_medicine():
    name = request.form['medicine_name']
    pharmacy_id = request.form['medicine_pharmacy_id']
    available = 'medicine_available' in request.form

    if name:
        try:
            connection = pyodbc.connect(pharmacy_app.conn_str)
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO Medicines (Name, PharmacyID, Available) VALUES (?, ?, ?)",
                (name, int(pharmacy_id) if pharmacy_id else None, 1 if available else 0)
            )
            connection.commit()
            flash("Medicine added successfully!")
            cursor.close()
            connection.close()
        except Exception as e:
            flash(str(e))
    else:
        flash("Please fill Medicine Name!")
    return redirect(url_for('admin_screen'))

@app.route('/patient')
def patient_screen():
    medicines = pharmacy_app.get_medicine_names()
    return render_template('patient.html', medicines=medicines)

@app.route('/search_medicine', methods=['POST'])
def search_medicine():
    medicine_name = request.form['medicine_name']
    if not medicine_name:
        flash("Please enter a medicine name!")
        return redirect(url_for('patient_screen'))

    try:
        connection = pyodbc.connect(pharmacy_app.conn_str)
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT m.Name, m.Available, p.Name AS PharmacyName, p.Address
            FROM Medicines m
            LEFT JOIN Pharmacies p ON m.PharmacyID = p.PharmacyID
            WHERE m.Name LIKE ?
            """,
            (f"%{medicine_name}%",)
        )
        rows = cursor.fetchall()
        results = []
        for row in rows:
            results.append({
                'medicine_name': row.Name if row.Name else "غير متوفر",
                'available': "Yes" if row.Available else "No",
                'pharmacy_name': row.PharmacyName if row.PharmacyName else "غير متوفر",
                'address': row.Address if row.Address else "غير متوفر"
            })
        cursor.close()
        connection.close()
        return render_template('patient.html', medicines=pharmacy_app.get_medicine_names(), results=results)
    except Exception as e:
        flash(str(e))
        return redirect(url_for('patient_screen'))

@app.route('/logout')
def logout():
    return redirect(url_for('login_screen'))

if __name__ == "__main__":
    import os
    port = int(os.getenv("PORT", 5000))  # ياخد الـ Port من المتغير البيئي، لو مش موجود يستخدم 5000
    app.run(debug=True, host='0.0.0.0', port=port)