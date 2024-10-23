import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

DATA_FILE = 'customers.json'

def load_customers():
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_customers(customers):
    with open(DATA_FILE, 'w') as file:
        json.dump(customers, file, indent=4)

@app.route('/')
def home():
    customers = load_customers() 
    search_query = request.args.get('search', '').lower()
    filtered_customers = [
        customer for customer in customers 
        if search_query in customer['name'].lower() or search_query in customer['store'].lower()
    ]
    return render_template('home.html', customers=filtered_customers, search_query=request.args.get('search', ''))

@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        customers = load_customers()
        new_customer = {
            'name': request.form['name'],
            'store': request.form['store'],
            'location': request.form['location'],
            'email': request.form['email'],
            'phone': request.form['phone'],
            'description': request.form['description']
        }
        customers.append(new_customer)
        save_customers(customers)
        return redirect(url_for('home'))
    return render_template('add_customer.html')

@app.route('/edit_customer/<int:index>', methods=['GET', 'POST'])
def edit_customer(index):
    customers = load_customers()
    if request.method == 'POST':
        updated_customer = {
            'name': request.form['name'],
            'store': request.form['store'],
            'location': request.form['location'],
            'email': request.form['email'],
            'phone': request.form['phone'],
            'description': request.form['description']
        }
        customers[index] = updated_customer
        save_customers(customers)
        return redirect(url_for('home'))
    customer = customers[index]
    return render_template('edit_customer.html', customer=customer, index=index)

@app.route('/delete_customer/<int:index>', methods=['POST'])
def delete_customer(index):
    customers = load_customers()
    customers.pop(index)
    save_customers(customers)
    return redirect(url_for('home'))

@app.route('/sort_customers/<string:field>')
def sort_customers(field):
    customers = load_customers()
    sorted_customers = sorted(customers, key=lambda x: x[field])
    return render_template('home.html', customers=sorted_customers)

if __name__ == '__main__':
    app.run(debug=True)
