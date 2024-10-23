import json
from flask import Flask, render_template, request, redirect, url_for
from wtforms import Form, StringField, TextAreaField, validators
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Secret key for CSRF protection
csrf = CSRFProtect(app)

DATA_FILE = 'customers.json'

# Load customers from the JSON file
def load_customers():
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Save customers to the JSON file
def save_customers(customers):
    with open(DATA_FILE, 'w') as file:
        json.dump(customers, file, indent=4)

# Form for adding/editing a customer
class CustomerForm(Form):
    name = StringField('Customer Name', [validators.InputRequired()])
    store = StringField('Store', [validators.InputRequired()])
    location = StringField('Location', [validators.InputRequired()])
    email = StringField('Email', [validators.Email()])
    phone = StringField('Phone Number', [validators.InputRequired()])
    description = TextAreaField('Description')

@app.route('/')
def home():
    customers = load_customers()
    search_query = request.args.get('search', '').lower()
    sort_field = request.args.get('sort', 'name')
    sort_order = request.args.get('order', 'asc')
    
    # Filter customers by search query
    filtered_customers = [
        customer for customer in customers
        if search_query in customer['name'].lower() or search_query in customer['store'].lower()
    ]
    
    # Sort customers by the specified field and order
    reverse = True if sort_order == 'desc' else False
    filtered_customers.sort(key=lambda x: x[sort_field], reverse=reverse)

    # Toggle sorting order for next click
    new_order = 'desc' if sort_order == 'asc' else 'asc'
    
    return render_template('home.html', customers=filtered_customers, search_query=search_query, sort_field=sort_field, sort_order=new_order)

@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    form = CustomerForm(request.form)
    if request.method == 'POST' and form.validate():
        customers = load_customers()
        new_customer = {
            'name': form.name.data,
            'store': form.store.data,
            'location': form.location.data,
            'email': form.email.data,
            'phone': form.phone.data,
            'description': form.description.data
        }
        customers.append(new_customer)
        save_customers(customers)
        return redirect(url_for('home'))
    return render_template('add_customer.html', form=form)

@app.route('/edit_customer/<int:index>', methods=['GET', 'POST'])
def edit_customer(index):
    customers = load_customers()
    form = CustomerForm(request.form)
    if request.method == 'POST' and form.validate():
        updated_customer = {
            'name': form.name.data,
            'store': form.store.data,
            'location': form.location.data,
            'email': form.email.data,
            'phone': form.phone.data,
            'description': form.description.data
        }
        customers[index] = updated_customer
        save_customers(customers)
        return redirect(url_for('home'))
    
    customer = customers[index]
    form.name.data = customer['name']
    form.store.data = customer['store']
    form.location.data = customer['location']
    form.email.data = customer['email']
    form.phone.data = customer['phone']
    form.description.data = customer['description']
    
    return render_template('edit_customer.html', form=form, index=index)

@app.route('/delete_customer/<int:index>', methods=['POST'])
def delete_customer(index):
    customers = load_customers()
    customers.pop(index)
    save_customers(customers)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
