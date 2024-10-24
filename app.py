import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

DATA_FILE = 'customers.json'

def load_customers():
    """Load customers from the JSON file."""
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_customers(customers):
    """Save customers to the JSON file."""
    with open(DATA_FILE, 'w') as file:
        json.dump(customers, file, indent=4)

@app.route('/')
def home():
    """Display the customer list with filtering and sorting options."""
    customers = load_customers()
    search_query = request.args.get('search', '').lower()
    sort_field = request.args.get('sort', '')
    sort_order = request.args.get('order', 'asc')  # Default to ascending order

    # Filter customers based on search query
    filtered_customers = [
        customer for customer in customers
        if search_query in customer['name'].lower() or search_query in customer['store'].lower()
    ]

    # Sort customers if a sort field is provided
    if sort_field in ['name', 'store', 'location']:
        filtered_customers.sort(key=lambda x: x[sort_field].lower(), reverse=(sort_order == 'desc'))

    return render_template('home.html', customers=filtered_customers, search_query=search_query, sort_field=sort_field, sort_order=sort_order)

@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    """Add a new customer to the list."""
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
    """Edit an existing customer's details."""
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
    return render_template('edit_customer.html', customer=customer)

@app.route('/delete_customer/<int:index>', methods=['POST'])
def delete_customer(index):
    """Delete a customer from the list."""
    customers = load_customers()
    customers.pop(index)
    save_customers(customers)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
