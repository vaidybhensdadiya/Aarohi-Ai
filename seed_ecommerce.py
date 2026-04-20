import pymysql
from database import get_db_connection

def create_and_seed_tables():
    conn = get_db_connection()
    if not conn:
        print("❌ Could not connect to database")
        return
        
    try:
        with conn.cursor() as cursor:
            # 1. Ensure Products Table exists
            create_products_table = """
            CREATE TABLE IF NOT EXISTS products (
                id INT AUTO_INCREMENT PRIMARY KEY,
                product_name VARCHAR(255) NOT NULL,
                category VARCHAR(100) NOT NULL,
                description TEXT,
                price DECIMAL(10, 2) NOT NULL,
                image_url VARCHAR(500),
                stock_quantity INT DEFAULT 0
            )
            """
            cursor.execute(create_products_table)
            
            # 2. Ensure Cart Table exists
            create_cart_table = """
            CREATE TABLE IF NOT EXISTS cart (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                product_id INT NOT NULL,
                quantity INT DEFAULT 1,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
            )
            """
            cursor.execute(create_cart_table)
            
            # Check if products already exist to prevent duplicate seeding
            cursor.execute("SELECT COUNT(*) as count FROM products")
            result = cursor.fetchone()
            if result and result['count'] > 0:
                print("✅ Products table already seeded. Skipping insertion.")
            else:
                # 3. Seed Amazon-style Products
                products_data = [
                    (
                        "Organic Cotton Sanitary Pads (Pack of 30)", 
                        "Sanitary pads", 
                        "Ultra-thin, rash-free organic cotton sanitary pads for heavy flow. Biodegradable and eco-friendly.", 
                        15.99, 
                        "https://images.unsplash.com/photo-1629814696208-8120406df493?q=80&w=400&h=400&fit=crop", 
                        100
                    ),
                    (
                        "Reusable Menstrual Cup - Medium", 
                        "Menstrual cups", 
                        "100% Medical grade silicone reusable menstrual cup. Up to 12 hours of protection.", 
                        24.50, 
                        "https://images.unsplash.com/photo-1584308666744-24d5e4a77e26?q=80&w=400&h=400&fit=crop", 
                        50
                    ),
                    (
                        "Electric Heating Pad for Cramps", 
                        "Heating pads", 
                        "Fast-heating pad offering deep tissue relief for menstrual cramps and back pain.", 
                        35.00, 
                        "https://images.unsplash.com/photo-1585255318859-f5c15f532a32?q=80&w=400&h=400&fit=crop", 
                        25
                    ),
                    (
                        "Intimate Wash (pH balanced)", 
                        "Intimate hygiene products", 
                        "Gentle intimate foaming wash to maintain healthy pH levels and prevent infections.", 
                        12.00, 
                        "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?q=80&w=400&h=400&fit=crop", 
                        80
                    ),
                    (
                        "Digital Pregnancy Test Kit (2 Pack)", 
                        "Pregnancy kits", 
                        "Extremely precise and early detection digital pregnancy tests.", 
                        18.75, 
                        "https://images.unsplash.com/photo-1583008985551-5cedc218d6e9?q=80&w=400&h=400&fit=crop", 
                        40
                    ),
                    (
                        "Applicator Tampons (Multipack)", 
                        "Tampons", 
                        "Plastic-free applicator tampons. Leak-free core with comfortable insertion.", 
                        14.20, 
                        "https://images.unsplash.com/photo-1629815049533-3cc1d50c7657?q=80&w=400&h=400&fit=crop", 
                        90
                    ),
                    (
                        "Overnight Maxi Pads with Wings", 
                        "Sanitary pads", 
                        "Maximum protection overnight pads. Absorbs instantly to keep you dry all night.", 
                        11.50, 
                        "https://images.unsplash.com/photo-1583947581924-860bda6a5c10?q=80&w=400&h=400&fit=crop", 
                        120
                    ),
                    (
                        "Menstrual Cup Wash", 
                        "Intimate hygiene products", 
                        "Specifically formulated to clean your menstrual cup without degrading silicone.", 
                        9.99, 
                        "https://images.unsplash.com/photo-1556228578-0d85b1a4d571?q=80&w=400&h=400&fit=crop", 
                        60
                    )
                ]
                
                insert_query = """
                INSERT INTO products (product_name, category, description, price, image_url, stock_quantity)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.executemany(insert_query, products_data)
                print(f"✅ Successfully seeded {len(products_data)} products into the database.")
                
            conn.commit()
            
    except Exception as e:
        print(f"❌ Error setting up ecommerce tables: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    create_and_seed_tables()
