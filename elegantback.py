# Orders page route

from flask import Flask, request, jsonify, render_template,session , flash , redirect , url_for
# from authlib.integrations.flask_client import OAuth
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import re
from flask_cors import CORS
from datetime import datetime
import sqlite3
import smtplib
from email.mime.text import MIMEText
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
import random

app = Flask(__name__)
CORS(app) 

products = [
    {"id": 1, "name": "Golden Ring", "price": 1599, "img": "ring1.png", "category": "ring"},
    {"id": 2, "name": "Diamond Ring", "price": 849, "img": "ring2.png", "category": "ring"},
    {"id": 3, "name": "Silver Ring", "price": 499, "img": "ring3.png", "category": "ring"},
    {"id": 4, "name": "Pearl Bangle", "price": 2199, "img": "bangle2.png", "category": "bangle"},
    {"id": 5, "name": "Modern Ring", "price": 399, "img": "ring5.png", "category": "ring"},
    {"id": 6, "name": "Modern Ring", "price": 399, "img": "bangle3.png", "category": "ring"},
    {"id": 7, "name": "Modern Ring", "price": 399, "img": "bangle4.png", "category": "ring"},
    {"id": 8, "name": "Modern Ring", "price": 399, "img": "bangle5.png", "category": "ring"},
]


# Database Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "hello@123"

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'karanrathour1811@gmail.com'  # change this
app.config['MAIL_PASSWORD'] = 'obdk pwaa odav olsz'     # change this
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

db = SQLAlchemy(app)
serializer = URLSafeTimedSerializer(app.secret_key)

# -------------------
# Database Model
# -------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow) 

# -------------------
# Utility Functions
# -------------------
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email)

# -------------------
# Routes
# -------------------
@app.route('/')
def home():
    # Check if user is logged in
    user_logged_in = 'user_id' in session
    username = session.get('username', '')
    return render_template('index.html', products=products, user_logged_in=user_logged_in, username=username)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = int(request.json['id'])

    # product find karo
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        return jsonify({"success": False, "message": "Product not found"}), 404

    # cart session me rakho
    if "cart" not in session:
        session["cart"] = []

    cart = session["cart"]

    # check if already exists
    for item in cart:
        if item["id"] == product_id:
            item["quantity"] += 1
            break
    else:
        cart.append({"id": product["id"], "name": product["name"], "price": product["price"], "quantity": 1})

    session["cart"] = cart
    return jsonify({"success": True, "cart": cart})

@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    return render_template('bangle_cart.html', cart_items=cart_items)

@app.route('/forgot_pass', methods=['GET', 'POST'])
def forgot_pass():
    if request.method == 'GET':
        return render_template('forgotpass.html', otp_sent=False)
    # POST
    if 'otp_sent' not in session:
        # Step 1: Email submitted
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if not user:
            flash('No account found with that email.', 'danger')
            return render_template('forgotpass.html', otp_sent=False, email=email)
        otp = str(random.randint(100000, 999999))
        session['reset_email'] = email
        session['reset_otp'] = otp
        session['otp_sent'] = True
        subject = 'Elegant Bangles Password Reset OTP'
        body = f'Your OTP for password reset is: {otp}\n\nDo not share this code with anyone.'
        send_email(email, subject, body)
        flash('An OTP has been sent to your email. Please enter it below.', 'info')
        return render_template('forgotpass.html', otp_sent=True, email=email)
    else:
        # Step 2: OTP and new password submitted
        user_otp = request.form.get('otp')
        password = request.form.get('password')
        if user_otp != session.get('reset_otp'):
            flash('Invalid OTP. Please try again.', 'danger')
            return render_template('forgotpass.html', otp_sent=True, email=session.get('reset_email'))
        if not password or len(password) < 6:
            flash('Password must be at least 6 characters.', 'danger')
            return render_template('forgotpass.html', otp_sent=True, email=session.get('reset_email'))
        user = User.query.filter_by(email=session.get('reset_email')).first()
        if not user:
            flash('User not found.', 'danger')
            return render_template('forgotpass.html', otp_sent=False)
        user.password_hash = generate_password_hash(password)
        db.session.commit()
        # Clear session
        session.pop('reset_email', None)
        session.pop('reset_otp', None)
        session.pop('otp_sent', None)
        flash('Your password has been reset. Please log in.', 'success')
        return redirect(url_for('login'))

def send_email(to, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = app.config['MAIL_USERNAME']
    msg['To'] = to
    try:
        with smtplib.SMTP(app.config['MAIL_SERVER'], app.config['MAIL_PORT']) as server:
            server.starttls()
            server.login(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            server.sendmail(app.config['MAIL_USERNAME'], [to], msg.as_string())
    except Exception as e:
        print('Email send failed:', e)

@app.route("/health")
def health():
    return "OK", 200

@app.route('/index')
def coustumer_care():
    return render_template('coustcare.html')

@app.route('/coustmure_care')
def index_home():
    return render_template('index.html')

@app.route('/shop')
def shop():
    return render_template('index.html')

@app.route('/checkout')
def checkout():
    cart_items = session.get('cart', [])
    return render_template('checkout.html', cart_items=cart_items)

@app.route('/orders')
def orders():
    if 'user_id' not in session:
        flash('Please log in to view your orders.', 'danger')
        return redirect(url_for('login'))
    # Placeholder: no real order data yet
    orders = []
    return render_template('orders.html', orders=orders)
# Profile page route
@app.route('/profile')
def profile():
    if 'user_id' not in session:
        flash('Please log in to view your profile.', 'danger')
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    user_data = {
        'username': user.username,
        'email': user.email,
        'joined': user.created_at.strftime('%d %b %Y') if user.created_at else ''
    } if user else None
    return render_template('profile.html', user=user_data)


@app.route("/place_order", methods=["POST"])
def place_order():
    # yaha order ka data save kar lo (DB me)
    # example: Order.create(user=session["user_id"], cart=session["cart"])

    return render_template("order_placed.html")



# Signup API
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')

    if request.method == 'POST':
        # Expecting JSON request
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'Request must be JSON'}), 400

        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')

        # Validation
        if not username or not email or not password:
            return jsonify({'success': False, 'message': 'All fields are required'}), 400
        if len(password) < 6:
            return jsonify({'success': False, 'message': 'Password must be at least 6 characters'}), 400
        if not is_valid_email(email):
            return jsonify({'success': False, 'message': 'Invalid email format'}), 400

        # Duplicate check
        if User.query.filter_by(email=email).first():
            return jsonify({'success': False, 'message': 'Email already registered'}), 400

        # Save user
        password_hash = generate_password_hash(password)
        new_user = User(username=username, email=email, password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()

        # Automatically log in the user after successful signup
        session['user_id'] = new_user.id
        session['username'] = new_user.username

        return jsonify({'success': True, 'message': 'Signup successful', 'redirect': '/'}), 201



# Login API
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'GET':
        return render_template('login.html')

    # POST request handle karo

    if request.method == 'POST':
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'Request must be JSON'}), 400
            
        email = data.get('email', '').strip()
        password = data.get('password', '')
    
        if email and password:
            user = User.query.filter_by(email=email).first()
            if user and check_password_hash(user.password_hash, password):
                session['user_id'] = user.id
                session['username'] = user.username
                return jsonify({'success': True, 'message': 'Login successful', 'redirect': '/'}), 200
            else:
                return jsonify({'success': False, 'message': 'Invalid email or password'}), 401
        else:
            return jsonify({'success': False, 'message': 'Email and password are required'}), 400
    
    return render_template('login.html')


# ---------- Logout ----------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/product_showcase')
def product_showcase():
    return render_template("product_showcase.html", products=products)

# -------------------
# Initialize DB
# -------------------
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run( host='0.0.0.0', debug=True, port=5000)

