"""
E-commerce routes for Aarohi AI.

This module defines all e-commerce-related API endpoints using session-based authentication.
"""

from flask import Blueprint, jsonify, render_template, request, session, redirect, url_for, flash
from ecommerce import services as ecommerce_services

ecommerce_bp = Blueprint('ecommerce', __name__, template_folder="../templates")

@ecommerce_bp.route('/store', methods=['GET'])
def store_home():
    """Render the main store page with all products or filtered by category."""
    category = request.args.get('category')
    products = ecommerce_services.get_all_products(category)
    return render_template("store.html", products=products, active_category=category)

@ecommerce_bp.route('/product/<int:product_id>', methods=['GET'])
def product_detail(product_id):
    """Render the details of a single product."""
    product = ecommerce_services.get_product_by_id(product_id)
    if not product:
        return redirect(url_for('ecommerce.store_home'))
    return render_template("product_detail.html", product=product)

@ecommerce_bp.route('/add-to-cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    """Add a product to the user's cart."""
    if "user_id" not in session:
        return redirect(url_for("login_page"))
    
    user_id = session["user_id"]
    quantity = int(request.form.get('quantity', 1))
    
    ecommerce_services.add_to_cart(user_id, product_id, quantity)
    return redirect(url_for('ecommerce.cart_page'))

@ecommerce_bp.route('/cart', methods=['GET'])
def cart_page():
    """Render the user's shopping cart."""
    if "user_id" not in session:
        return redirect(url_for("login_page"))
        
    user_id = session["user_id"]
    cart_items = ecommerce_services.get_cart_items(user_id)
    
    # Calculate cart total
    cart_total = sum(item['subtotal'] for item in cart_items)
    
    return render_template("cart.html", cart_items=cart_items, cart_total=cart_total)

@ecommerce_bp.route('/remove-from-cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    """Remove a product entirely from the user's cart."""
    if "user_id" not in session:
        return redirect(url_for("login_page"))
        
    user_id = session["user_id"]
    ecommerce_services.remove_from_cart(user_id, product_id)
    return redirect(url_for('ecommerce.cart_page'))

@ecommerce_bp.route('/update-cart/<int:cart_id>', methods=['POST'])
def update_cart(cart_id):
    """Update the quantity of a cart item."""
    if "user_id" not in session:
        return redirect(url_for("login_page"))
        
    user_id = session["user_id"]
    quantity = int(request.form.get('quantity', 1))
    ecommerce_services.update_cart_quantity(user_id, cart_id, quantity)
    return redirect(url_for('ecommerce.cart_page'))

@ecommerce_bp.route('/checkout', methods=['GET'])
def checkout_page():
    """Render a basic checkout summary."""
    if "user_id" not in session:
        return redirect(url_for("login_page"))
        
    user_id = session["user_id"]
    cart_items = ecommerce_services.get_cart_items(user_id)
    if not cart_items:
        return redirect(url_for('ecommerce.store_home'))
        
    cart_total = sum(item['subtotal'] for item in cart_items)
    return render_template("checkout.html", cart_items=cart_items, cart_total=cart_total, success=False)

@ecommerce_bp.route('/place-order', methods=['POST'])
def place_order():
    """Process the order."""
    if "user_id" not in session:
        return redirect(url_for("login_page"))
        
    user_id = session["user_id"]
    
    address = request.form.get('address')
    payment_method = request.form.get('payment_method')
    
    cart_items = ecommerce_services.get_cart_items(user_id)
    if not cart_items:
        return redirect(url_for('ecommerce.store_home'))
        
    cart_total = sum(item['subtotal'] for item in cart_items)
    
    success = ecommerce_services.place_order(user_id, cart_total, address, payment_method)
    if success:
        flash("Order placed successfully")
        return redirect(url_for('dashboard_page'))
    else:
        flash("Failed to place order.", "error")
        return redirect(url_for('ecommerce.checkout_page'))

