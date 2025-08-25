from flask import Flask, render_template, url_for, request, jsonify, session, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Needed for session management

# MongoDB connection
mongo_uri = os.environ.get("MONGO_URI")  # Fetches from environment variable
client = MongoClient(mongo_uri)
db = client['Anime']

# Collections
products_collection = db['Products']
users_collection = db['Users']
orders_collection = db['Orders']
cart_collection = db['Cart']

@app.route("/")
def index():
    # Fetch featured products from database
    featured_products = list(products_collection.find({"featured": True}).limit(4))
    
    # Convert ObjectId to string for JSON serialization
    for product in featured_products:
        product['_id'] = str(product['_id'])
    
    # Get cart count for the header
    cart_count = 0
    if 'cart' in session:
        cart_count = len(session['cart'])
    
    return render_template("index.html", products=featured_products, cart_count=cart_count)

@app.route("/products")
def products():
    # Get all products
    all_products = list(products_collection.find())
    
    # Convert ObjectId to string for JSON serialization
    for product in all_products:
        product['_id'] = str(product['_id'])
        
    # Get cart count for the header
    cart_count = 0
    if 'cart' in session:
        cart_count = len(session['cart'])
        
    return render_template("products.html", products=all_products, cart_count=cart_count)

@app.route("/add_to_cart", methods=['POST'])
def add_to_cart():
    product_id = request.form.get('product_id')
    
    # Initialize cart in session if it doesn't exist
    if 'cart' not in session:
        session['cart'] = []
    
    # Add product to cart (storing just the ID)
    if product_id not in session['cart']:
        session['cart'].append(product_id)
        session.modified = True
    
    return jsonify({'success': True, 'cart_count': len(session['cart'])})

@app.route("/remove_from_cart", methods=['POST'])
def remove_from_cart():
    product_id = request.form.get('product_id')
    
    if 'cart' in session and product_id in session['cart']:
        session['cart'].remove(product_id)
        session.modified = True
    
    return jsonify({'success': True, 'cart_count': len(session['cart'])})

@app.route("/cart")
def view_cart():
    cart_items = []
    total = 0
    
    if 'cart' in session:
        for product_id in session['cart']:
            # Convert string ID back to ObjectId for querying
            try:
                product = products_collection.find_one({'_id': ObjectId(product_id)})
                if product:
                    product['_id'] = str(product['_id'])  # Convert to string for template
                    cart_items.append(product)
                    total += product['price']
            except:
                # Handle invalid ObjectId
                continue
    
    # Get cart count for the header
    cart_count = len(session['cart']) if 'cart' in session else 0
    
    return render_template("cart.html", cart_items=cart_items, total=total, cart_count=cart_count)

@app.route("/update_cart_quantity", methods=['POST'])
def update_cart_quantity():
    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity'))
    
    # Update the quantity in session
    if 'cart_quantities' not in session:
        session['cart_quantities'] = {}
    
    session['cart_quantities'][product_id] = quantity
    session.modified = True
    
    return jsonify({'success': True})

@app.route("/checkout", methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        # Process the order
        order_data = {
            'customer_info': {
                'first_name': request.form.get('firstName'),
                'last_name': request.form.get('lastName'),
                'address': request.form.get('address'),
                'city': request.form.get('city'),
                'zip_code': request.form.get('zipCode')
            },
            'payment_info': {
                'card_number': request.form.get('cardNumber'),
                'exp_date': request.form.get('expDate'),
                'cvv': request.form.get('cvv')
            },
            'items': session.get('cart', []),
            'item_quantities': session.get('cart_quantities', {}),
            'order_date': datetime.now(),
            'status': 'processing'
        }
        
        # Calculate total amount
        total_amount = 0
        if 'cart' in session:
            for product_id in session['cart']:
                product = products_collection.find_one({'_id': ObjectId(product_id)})
                if product:
                    quantity = session['cart_quantities'].get(product_id, 1)
                    total_amount += product['price'] * quantity
        
        order_data['total_amount'] = total_amount
        
        # Save order to database
        orders_collection.insert_one(order_data)
        
        # Clear the cart
        session.pop('cart', None)
        session.pop('cart_quantities', None)
        
        return redirect('/order_confirmation')
    
    # For GET request, show checkout form
    cart_count = len(session['cart']) if 'cart' in session else 0
    return render_template("checkout.html", cart_count=cart_count)

@app.route("/order_confirmation")
def order_confirmation():
    cart_count = 0
    return render_template("order_confirmation.html", cart_count=cart_count)
