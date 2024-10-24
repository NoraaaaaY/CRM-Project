from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Path to the JSON file
JSON_FILE = 'customers.json'

# Load customers from the JSON file
def load_customers():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r') as f:
            return json.load(f)
    return []

# Save customers to the JSON file
def save_customers(customers):
    with open(JSON_FILE, 'w') as f:
        json.dump(customers, f, indent=4)

# Home route
@app.route('/', methods=['GET', 'POST'])
def home():
    customers = load_customers()
    if request.method == 'POST':
        search_query = request.form.get('search', '')
        customers = [c for c in customers if search_query.lower() in c['name'].lower()]
        return render_template('home.html', customers=customers, search_query=search_query)

    return render_template('home.html', customers=customers)

# Add customer route
@app.route('/add', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        
        new_customer = {
            'id': len(load_customers()) + 1,  # Assign an ID
            'name': name,
            'email': email,
            'phone': phone
        }

        customers = load_customers()
        customers.append(new_customer)
        save_customers(customers)

        flash('Customer added successfully!')
        return redirect(url_for('home'))

    return render_template('customer.html')

# Edit customer route
@app.route('/edit/<int:customer_id>', methods=['GET', 'POST'])
def edit_customer(customer_id):
    customers = load_customers()
    customer = next((c for c in customers if c['id'] == customer_id), None)

    if request.method == 'POST':
        customer['name'] = request.form['name']
        customer['email'] = request.form['email']
        customer['phone'] = request.form['phone']

        save_customers(customers)

        flash('Customer updated successfully!')
        return redirect(url_for('home'))

    return render_template('edit_customer.html', customer=customer)

# Delete customer route
@app.route('/delete/<int:customer_id>', methods=['POST'])
def delete_customer(customer_id):
    customers = load_customers()
    customers = [c for c in customers if c['id'] != customer_id]
    save_customers(customers)

    flash('Customer deleted successfully!')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
