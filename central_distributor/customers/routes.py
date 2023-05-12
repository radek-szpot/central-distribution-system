from flask import Flask, render_template, request
from models import Customer

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Retrieve form data and create a new customer account
        customer_id = request.form['customer_id']
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        customer = Customer(customer_id, name, email, password)
        customer.create_account()

        # Redirect to login page or dashboard
        return render_template('login.html')

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Retrieve form data and perform customer login
        email = request.form['email']
        password = request.form['password']

        customer = Customer(email=email, password=password)
        if customer.login():
            # Redirect to dashboard
            return render_template('dashboard.html')

        # Invalid login, show error message
        return render_template('login.html', error=True)

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    # Display the customer's dashboard
    return render_template('dashboard.html')


if __name__ == '__main__':
    app.run()
