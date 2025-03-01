from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)

# Function to connect to the database
def get_db_connection():
    conn = sqlite3.connect("customers.db")
    conn.row_factory = sqlite3.Row  # Returns dictionary-like rows
    return conn

# Home Route - Display Customers
@app.route('/')
def index():
    conn = get_db_connection()
    customers = conn.execute("SELECT * FROM Customers").fetchall()
    conn.close()
    return render_template("index.html", customers=customers)

# Add Customer Route
@app.route('/add', methods=['POST'])
def add_customer():
    name = request.form['client_name']
    uen = request.form['uen']
    year_end = request.form['year_end']
    date_of_incorp = request.form['date_of_incorporation']
    person = request.form['person_in_charge']
    contact = request.form['contact_number']

    conn = get_db_connection()
    conn.execute("INSERT INTO Customers (client_name, uen, year_end, date_of_incorporation, person_in_charge, contact_number) VALUES (?, ?, ?, ?, ?, ?)",
                 (name, uen, year_end, date_of_incorp, person, contact))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

# Generate PDF for a Customer
@app.route('/generate_pdf/<int:customer_id>')
def generate_pdf(customer_id):
    conn = get_db_connection()
    customer = conn.execute("SELECT * FROM Customers WHERE id=?", (customer_id,)).fetchone()
    conn.close()

    if customer:
        pdf_file = f"static/customer_{customer_id}.pdf"
        c = canvas.Canvas(pdf_file, pagesize=letter)
        c.drawString(100, 750, f"Client Name: {customer['client_name']}")
        c.drawString(100, 730, f"UEN: {customer['uen']}")
        c.drawString(100, 710, f"Year End: {customer['year_end']}")
        c.drawString(100, 690, f"Date of Incorporation: {customer['date_of_incorporation']}")
        c.drawString(100, 670, f"Person in Charge: {customer['person_in_charge']}")
        c.drawString(100, 650, f"Contact Number: {customer['contact_number']}")
        c.save()

        return f'<a href="/{pdf_file}" download>Download PDF</a>'

    return "Customer not found!"

if __name__ == "__main__":
    app.run(debug=True)
