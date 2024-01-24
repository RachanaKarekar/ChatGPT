# app.py
import os
from flask import Flask, render_template, request, redirect, url_for, flash, session



app = Flask(__name__)
app.secret_key = 'your_secret_key'
# app.secret_key = os.urandom(24)

app = Flask(__name__)

# Mock data for product catalog (in-memory storage, replace with a database in production)
products = [
    {'id': 1, 'name': 'Plated Red Maxi Dress', 'price': 1599, 'size': 'XS-6XL', 'image': 'https://unsplash.com/photos/tyfqOL1FAQc/download'},
    {'id': 2, 'name': 'Ethnic Maxi Dress', 'price': 999, 'size': 'XS-6XL', 'image': 'https://unsplash.com/photos/QrOdhsMAQw8/download'},
    {'id': 3, 'name': 'Casual White Maxi Dress', 'price': 999, 'size': 'XS-6XL', 'image': 'https://unsplash.com/photos/aK6Z4aPdf5c/download'},
    {'id': 4, 'name': 'Black Formal Set 1', 'price': 7999, 'size': 'XS-6XL', 'image': 'https://unsplash.com/photos/A3MleA0jtoE/download'},
    {'id': 5, 'name': 'Casual White Maxi Dress with Prints', 'price': 1599, 'size': 'XS-6XL', 'image': 'https://unsplash.com/photos/Oo5sKlgIOZQ/download'},
    {'id': 6, 'name': 'Mustard Maxi Dress', 'price': 1999, 'size': 'XS-6XL', 'image': 'https://unsplash.com/photos/OT0_1I7s_j0/download'},
    {'id': 7, 'name': 'Black Formal Set 2', 'price': 4999, 'size': 'XS-6XL', 'image': 'https://unsplash.com/photos/dodzmVtjoKs/download'},
    {'id': 8, 'name': 'Black Maxi Dress', 'price': 1999, 'size': 'XS-6XL', 'image': 'https://unsplash.com/photos/fnwkZRWxWEc/download'},
    {'id': 9, 'name': 'Cream Maxi Dress', 'price': 1999, 'size': 'XS-6XL', 'image': 'https://unsplash.com/photos/D9ngHG-BPAY/download'},
    {'id': 10, 'name': 'Blue Stripped Dress', 'price': 599, 'size': 'XS-6XL', 'image': 'https://unsplash.com/photos/V7IJzp_ElQc/download'},
]

# Mock data for user registration and product catalog (in-memory storage, replace with a database in production)
users = []
cart=[]

def is_user_registered(username):
    return any(user['username'] == username for user in users)

def reset_login_attempts():
    session['login_attempts'] = 0

def is_login_attempts_exceeded():
    attempts = session.get('login_attempts', 0)
    return attempts >= 3

def increment_login_attempts():
    session['login_attempts'] = session.get('login_attempts', 0) + 1

def set_cart_for_user(username, cart):
    user = next(user for user in users if user['username'] == username)
    user['cart'] = cart

@app.route('/')
def product_catalog():
    return render_template('product_catalog.html', products=products)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the user is already registered
        if is_user_registered(username):
            flash('The user is already registered.', 'danger')
        else:
            # Register the user
            users.append({'username': username, 'password': password})
            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the user is registered
        if not any(user['username'] == username for user in users):
            flash('Please check your credentials.', 'danger')
            return render_template('login.html')

        user = next(user for user in users if user['username'] == username)

        # Check if the password is correct
        if user['password'] == password:
            reset_login_attempts()
            session['username'] = username
            session['cart'] = []  # Initialize an empty cart in the session
            set_cart_for_user(username, [])  # Initialize an empty cart for the user
            flash('Login successful. Welcome back!', 'success')
            return redirect(url_for('product_catalog'))
        else:
            increment_login_attempts()

            if is_login_attempts_exceeded():
                flash('Sorry, you\'ve exceeded login attempts for the day. Please try after 24 hours.', 'danger')
                return redirect(url_for('index'))

            flash('Please check your credentials.', 'danger')

    return render_template('login.html')

@app.route('/cart')
def cart():
    if 'username' not in session:
        flash('Please log in to view your cart.', 'info')
        return redirect(url_for('login'))

    username = session['username']
    user = next(user for user in users if user['username'] == username)

    return render_template('cart.html', user=user)

@app.route('/add_to_cart/<int:product_id>', methods=['GET', 'POST'])
def add_to_cart(product_id):
    if 'username' not in session:
        flash('Please log in to add items to your cart.', 'info')
        return redirect(url_for('login'))

    if request.method == 'POST':
        username = session['username']
        try:
            user = next(user for user in users if user['username'] == username)
        except StopIteration:
            flash('User not found. Please log in again.', 'danger')
            return redirect(url_for('login'))

        product = next((product for product in products if product['id'] == product_id), None)

        if product:
            user['cart'].append(product)
            flash(f'{product["name"]} added to your cart!', 'success')
        else:
            flash('Product not found.', 'danger')

        return redirect(url_for('product_catalog'))

    return render_template('product_catalog.html', products=products)

@app.route('/checkout')
def checkout():
    if 'username' not in session:
        flash('Please log in to proceed to checkout.', 'info')
        return redirect(url_for('login'))

    return render_template('checkout.html')

@app.route('/make_payment', methods=['POST'])
def make_payment():
    if 'username' not in session:
        flash('Please log in to make a payment.', 'info')
        return redirect(url_for('login'))

    # Process the payment (placeholder)

    # Clear the user's cart after successful payment
    username = session['username']
    user = next((user for user in users if user['username'] == username), None)

    if user:
        user['cart'] = []
        flash('Thanks for placing the order! You will receive further details on your mobile number.', 'success')
        return render_template('order_success.html')  # Render the order success template
    else:
        flash('Unable to process the order. Please try again.', 'danger')

    return redirect(url_for('product_catalog'))


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        username = request.form['username']
        new_password = request.form['new_password']

        user = next((user for user in users if user['username'] == username), None)

        if user:
            user['password'] = new_password
            flash('Password reset successful. Please log in with your new password.', 'success')
            return redirect(url_for('login'))  # Redirect to the login page after password reset
        else:
            flash('Invalid username. Please try again.', 'danger')

    return render_template('reset_password.html')

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        # No need to check the email, just redirect to the reset password page
        return redirect(url_for('reset_password'))

    return render_template('forgot_pwd.html')

if __name__ == '__main__':
    app.secret_key = 'your_secret_key'
    app.run(debug=True)
