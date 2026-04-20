"""
E-commerce services for Aarohi AI.

This module contains business logic for e-commerce operations
like product management, cart operations, and order processing.
Currently empty - will be implemented later.
"""

from database import get_db_connection

def get_all_products(category=None):
    """Fetch all products, optionally filtered by category."""
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        with conn.cursor() as cursor:
            if category:
                query = "SELECT * FROM products WHERE category = %s"
                cursor.execute(query, (category,))
            else:
                query = "SELECT * FROM products"
                cursor.execute(query)
            return cursor.fetchall()
    except Exception as e:
        print(f"Error fetching products: {e}")
        return []
    finally:
        conn.close()

def get_product_by_id(product_id):
    """Fetch a single product's details."""
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        with conn.cursor() as cursor:
            query = "SELECT * FROM products WHERE id = %s"
            cursor.execute(query, (product_id,))
            return cursor.fetchone()
    except Exception as e:
        print(f"Error fetching product details: {e}")
        return None
    finally:
        conn.close()

def add_to_cart(user_id, product_id, quantity=1):
    """Add a product to the user's cart or update quantity if it exists."""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        with conn.cursor() as cursor:
            # Check if item is already in cart
            check_query = "SELECT id, quantity FROM cart WHERE user_id = %s AND product_id = %s"
            cursor.execute(check_query, (user_id, product_id))
            existing_item = cursor.fetchone()
            
            if existing_item:
                # Update existing quantity
                new_quantity = existing_item['quantity'] + quantity
                update_query = "UPDATE cart SET quantity = %s WHERE id = %s"
                cursor.execute(update_query, (new_quantity, existing_item['id']))
            else:
                # Add new item
                insert_query = "INSERT INTO cart (user_id, product_id, quantity) VALUES (%s, %s, %s)"
                cursor.execute(insert_query, (user_id, product_id, quantity))
            
            conn.commit()
            return True
    except Exception as e:
        print(f"Error adding to cart: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def get_cart_items(user_id):
    """Retrieve all items in a user's cart along with product details."""
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        with conn.cursor() as cursor:
            query = """
                SELECT 
                    c.id as cart_id, 
                    c.quantity, 
                    p.id as product_id, 
                    p.product_name, 
                    p.price, 
                    p.image_url,
                    (p.price * c.quantity) as subtotal
                FROM cart c
                JOIN products p ON c.product_id = p.id
                WHERE c.user_id = %s
            """
            cursor.execute(query, (user_id,))
            return cursor.fetchall()
    except Exception as e:
        print(f"Error fetching cart items: {e}")
        return []
    finally:
        conn.close()

def remove_from_cart(user_id, product_id):
    """Remove a specific product from a user's cart."""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        with conn.cursor() as cursor:
            query = "DELETE FROM cart WHERE user_id = %s AND product_id = %s"
            cursor.execute(query, (user_id, product_id))
            conn.commit()
            return True
    except Exception as e:
        print(f"Error removing from cart: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def clear_cart(user_id):
    """Empty the entire cart for a user (called after successful checkout)."""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        with conn.cursor() as cursor:
            query = "DELETE FROM cart WHERE user_id = %s"
            cursor.execute(query, (user_id,))
            conn.commit()
            return True
    except Exception as e:
        print(f"Error clearing cart: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def update_cart_quantity(user_id, cart_id, quantity):
    """Update the quantity of a specific cart item."""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        with conn.cursor() as cursor:
            # Check if the cart item belongs to the user
            check_query = "SELECT id FROM cart WHERE id = %s AND user_id = %s"
            cursor.execute(check_query, (cart_id, user_id))
            if not cursor.fetchone():
                return False
                
            if quantity <= 0:
                del_query = "DELETE FROM cart WHERE id = %s"
                cursor.execute(del_query, (cart_id,))
            else:
                update_query = "UPDATE cart SET quantity = %s WHERE id = %s"
                cursor.execute(update_query, (quantity, cart_id))
            
            conn.commit()
            return True
    except Exception as e:
        print(f"Error updating cart quantity: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def place_order(user_id, total_amount, address, payment_method):
    """Move cart items to an order."""
    conn = get_db_connection()
    if not conn:
        return False
        
    try:
        with conn.cursor() as cursor:
            # Insert into orders
            order_query = """
                INSERT INTO orders (user_id, total_amount, address, payment_method)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(order_query, (user_id, total_amount, address, payment_method))
            order_id = cursor.lastrowid
            
            # Get cart items
            cart_query = """
                SELECT c.product_id, c.quantity, p.price 
                FROM cart c
                JOIN products p ON c.product_id = p.id
                WHERE c.user_id = %s
            """
            cursor.execute(cart_query, (user_id,))
            cart_items = cursor.fetchall()
            
            if not cart_items:
                conn.rollback()
                return False
                
            # Insert into order_items
            for item in cart_items:
                item_query = """
                    INSERT INTO order_items (order_id, product_id, quantity, price)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(item_query, (order_id, item['product_id'], item['quantity'], item['price']))
                
            # Clear cart
            clear_query = "DELETE FROM cart WHERE user_id = %s"
            cursor.execute(clear_query, (user_id,))
            
            conn.commit()
            return True
    except Exception as e:
        print(f"Error placing order: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()
