import pymysql
from database import get_db_connection

def setup_ecommerce_tables():
    conn = get_db_connection()
    if not conn:
        print("Could not connect to database")
        return
        
    try:
        with conn.cursor() as cursor:
            # Create cart table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cart (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    product_id INT NOT NULL,
                    quantity INT DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
                )
            """)
            print("Successfully created 'cart' table (if it didn't exist).")
            
            # Create orders table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    total_amount DECIMAL(10, 2) NOT NULL,
                    address TEXT NOT NULL,
                    payment_method VARCHAR(50) NOT NULL,
                    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)
            print("Successfully created 'orders' table (if it didn't exist).")
            
            # Create order_items table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS order_items (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    order_id INT NOT NULL,
                    product_id INT NOT NULL,
                    quantity INT NOT NULL,
                    price DECIMAL(10, 2) NOT NULL,
                    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
                    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
                )
            """)
            print("Successfully created 'order_items' table (if it didn't exist).")
            
            conn.commit()
    except Exception as e:
        print(f"Error setting up e-commerce tables: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    setup_ecommerce_tables()
