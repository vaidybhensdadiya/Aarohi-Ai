import pymysql
from database import get_db_connection

def create_and_seed_tables():
    conn = get_db_connection()
    if not conn:
        print("[ERROR] Could not connect to database")
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

            # Clear existing data to ensure fresh seeding of 54 items
            print("Cleaning existing e-commerce data to prevent conflicts...")
            cursor.execute("DELETE FROM cart")
            try:
                cursor.execute("DELETE FROM order_items")
            except Exception:
                pass
            cursor.execute("DELETE FROM products")
            
            # 3. Seed 54 Products with INR pricing and 100% active, category-accurate image URLs
            products_data = [
                # Category: Sanitary pads (9 products)
                (
                    "Whisper Ultra Clean XL Sanitary Pads (Pack of 30)", 
                    "Sanitary pads", 
                    "Double wings for extra protection, lock-in gel technology, high absorbency for active days.", 
                    349.00, 
                    "https://images.unsplash.com/photo-1562240020-ce31ccb0fa7d?q=80&w=400&h=400&fit=crop", 
                    100
                ),
                (
                    "Stayfree Secure Cottony XL Sanitary Pads (Pack of 40)", 
                    "Sanitary pads", 
                    "Cottony soft cover for ultimate comfort and irritation-free protection during heavy flow.", 
                    299.00, 
                    "https://images.unsplash.com/photo-1562240020-ce31ccb0fa7d?q=80&w=400&h=400&fit=crop", 
                    150
                ),
                (
                    "Whisper Bindazzz Nights XXXL Pads (Pack of 10)", 
                    "Sanitary pads", 
                    "Extra-long overnight sanitary pads with a wide back for complete leak-free sleep.", 
                    240.00, 
                    "https://images.unsplash.com/photo-1562240020-ce31ccb0fa7d?q=80&w=400&h=400&fit=crop", 
                    80
                ),
                (
                    "Nua Ultra-Thin Organic Sanitary Pads (Pack of 12)", 
                    "Sanitary pads", 
                    "Chemical-free, super-absorbent organic cotton pads customizable by flow size (Heavy, Medium, Light).", 
                    199.00, 
                    "https://images.unsplash.com/photo-1562240020-ce31ccb0fa7d?q=80&w=400&h=400&fit=crop", 
                    120
                ),
                (
                    "Carmesi Eco-Friendly Biodegradable Pads (Pack of 30)", 
                    "Sanitary pads", 
                    "Made entirely of bamboo and corn fiber. Completely biodegradable and gentle on sensitive skin.", 
                    499.00, 
                    "https://images.unsplash.com/photo-1562240020-ce31ccb0fa7d?q=80&w=400&h=400&fit=crop", 
                    60
                ),
                (
                    "Bella Maxi Cotton Soft Wings Pads (Pack of 15)", 
                    "Sanitary pads", 
                    "Breathable sanitary pads with high absorption capacity. Imported from Europe, dermatologist tested.", 
                    180.00, 
                    "https://images.unsplash.com/photo-1562240020-ce31ccb0fa7d?q=80&w=400&h=400&fit=crop", 
                    90
                ),
                (
                    "Sofy Anti-Bacteria Extra Long Pads (Pack of 30)", 
                    "Sanitary pads", 
                    "Deep absorption sheet with green sheet technology for 99.9% bacteria protection and fresh scent.", 
                    375.00, 
                    "https://images.unsplash.com/photo-1562240020-ce31ccb0fa7d?q=80&w=400&h=400&fit=crop", 
                    110
                ),
                (
                    "Sanfe Bamboo Sanitary Pads (Pack of 12)", 
                    "Sanitary pads", 
                    "Natural bamboo fiber pads that prevent rashes, odor, and offer extra wide coverage for leaks.", 
                    229.00, 
                    "https://images.unsplash.com/photo-1562240020-ce31ccb0fa7d?q=80&w=400&h=400&fit=crop", 
                    70
                ),
                (
                    "Pee Safe Organic Cotton Sanitary Pads (Pack of 20)", 
                    "Sanitary pads", 
                    "100% organic cotton top sheet with biodegradable backing. Hypoallergenic and chlorine-free.", 
                    299.00, 
                    "https://images.unsplash.com/photo-1562240020-ce31ccb0fa7d?q=80&w=400&h=400&fit=crop", 
                    100
                ),

                # Category: Tampons (9 products)
                (
                    "Sirona Premium Digital Tampons - Super (Pack of 20)", 
                    "Tampons", 
                    "Fiber-lock technology for leak-proof comfort. Highly absorbent digital tampons for medium to heavy flow.", 
                    249.00, 
                    "https://images.unsplash.com/photo-1562240020-ce31ccb0fa7d?q=80&w=400&h=400&fit=crop", 
                    200
                ),
                (
                    "Pee Safe Organic Cotton Tampons - Regular (Pack of 16)", 
                    "Tampons", 
                    "100% organic cotton tampons without chemical fragrances or chlorine bleaching. Soft and comfortable.", 
                    220.00, 
                    "https://images.unsplash.com/photo-1544816155-12df9643f363?q=80&w=400&h=400&fit=crop", 
                    150
                ),
                (
                    "Tampax Compak Active Tampons - Regular (Pack of 18)", 
                    "Tampons", 
                    "Discreet plastic applicator with built-in protective skirt to prevent leaks before they happen.", 
                    599.00, 
                    "https://images.unsplash.com/photo-1608571423902-eed4a5ad8108?q=80&w=400&h=400&fit=crop", 
                    90
                ),
                (
                    "Bella Tampons Premium Comfort - Super (Pack of 16)", 
                    "Tampons", 
                    "Imported premium tampons with easy-open wrap and highly absorbent core for safe period protection.", 
                    199.00, 
                    "https://images.unsplash.com/photo-1562240020-ce31ccb0fa7d?q=80&w=400&h=400&fit=crop", 
                    110
                ),
                (
                    "Sofy Soft Tampons with Applicator - Regular (Pack of 10)", 
                    "Tampons", 
                    "Gentle applicator for hassle-free insertion. Perfect for beginners and active sports days.", 
                    350.00, 
                    "https://images.unsplash.com/photo-1544816155-12df9643f363?q=80&w=400&h=400&fit=crop", 
                    80
                ),
                (
                    "Carmesi 100% Organic Cotton Tampons - Regular (Pack of 16)", 
                    "Tampons", 
                    "Rash-free, chemical-free cotton tampons that adapt perfectly to your body shape.", 
                    280.00, 
                    "https://images.unsplash.com/photo-1608571423902-eed4a5ad8108?q=80&w=400&h=400&fit=crop", 
                    95
                ),
                (
                    "Sanfe Organic Cotton Tampons - Super Plus (Pack of 16)", 
                    "Tampons", 
                    "Ultra-absorbent tampons designed for very heavy flow. Hypoallergenic and chemical-free.", 
                    299.00, 
                    "https://images.unsplash.com/photo-1562240020-ce31ccb0fa7d?q=80&w=400&h=400&fit=crop", 
                    130
                ),
                (
                    "O.B. ProComfort Tampons - Regular (Pack of 10)", 
                    "Tampons", 
                    "Fluid-Lock technology with curved grooves to guide fluid inside the tampon core reliably.", 
                    175.00, 
                    "https://images.unsplash.com/photo-1544816155-12df9643f363?q=80&w=400&h=400&fit=crop", 
                    140
                ),
                (
                    "Sirona Premium Applicator Tampons - Super (Pack of 8)", 
                    "Tampons", 
                    "FDA-approved applicator tampons for ultra smooth insertion and leak-proof confidence.", 
                    299.00, 
                    "https://images.unsplash.com/photo-1608571423902-eed4a5ad8108?q=80&w=400&h=400&fit=crop", 
                    100
                ),

                # Category: Menstrual cups (9 products)
                (
                    "Sirona Reusable Menstrual Cup (Medium Size)", 
                    "Menstrual cups", 
                    "FDA-approved medical grade silicone cup. Provides up to 8 hours of leak protection and lasts up to 10 years.", 
                    299.00, 
                    "https://images.unsplash.com/photo-1606760227091-3dd870d97f1d?q=80&w=400&h=400&fit=crop", 
                    300
                ),
                (
                    "Pee Safe Menstrual Cup (Small Size)", 
                    "Menstrual cups", 
                    "Super soft, medical-grade silicone cup ideal for teenagers and first-time users.", 
                    349.00, 
                    "https://images.unsplash.com/photo-1606760227091-3dd870d97f1d?q=80&w=400&h=400&fit=crop", 
                    250
                ),
                (
                    "Carmesi Reusable Menstrual Cup with Pouch", 
                    "Menstrual cups", 
                    "Extra flexible silicone cup with a ribbed stem for easy removal. Comes with a breathable cotton storage pouch.", 
                    399.00, 
                    "https://images.unsplash.com/photo-1606760227091-3dd870d97f1d?q=80&w=400&h=400&fit=crop", 
                    180
                ),
                (
                    "Safecup Menstrual Cup (Large Size)", 
                    "Menstrual cups", 
                    "Premium US-FDA registered silicone cup. Ideal for women with heavy flow or after childbirth.", 
                    499.00, 
                    "https://images.unsplash.com/photo-1606760227091-3dd870d97f1d?q=80&w=400&h=400&fit=crop", 
                    120
                ),
                (
                    "Gynocup Menstrual Cup with Sterilizer Container", 
                    "Menstrual cups", 
                    "Complete set with sterilizing container. Easy to wash, maintain hygiene, and travel friendly.", 
                    449.00, 
                    "https://images.unsplash.com/photo-1606760227091-3dd870d97f1d?q=80&w=400&h=400&fit=crop", 
                    150
                ),
                (
                    "Plush Ultra Soft Menstrual Cup - Medium", 
                    "Menstrual cups", 
                    "Designed to be highly flexible for maximum comfort during sports, swimming, and sleeping.", 
                    375.00, 
                    "https://images.unsplash.com/photo-1606760227091-3dd870d97f1d?q=80&w=400&h=400&fit=crop", 
                    100
                ),
                (
                    "Everteen Menstrual Cup for Women", 
                    "Menstrual cups", 
                    "Sleek and easy-to-fold design to prevent leaks. Safe for continuous 12-hour usage.", 
                    299.00, 
                    "https://images.unsplash.com/photo-1606760227091-3dd870d97f1d?q=80&w=400&h=400&fit=crop", 
                    90
                ),
                (
                    "Sanfe Reusable Menstrual Cup with Ring Stem", 
                    "Menstrual cups", 
                    "Unique ring-stem design makes it incredibly easy to locate and pull out the cup safely.", 
                    349.00, 
                    "https://images.unsplash.com/photo-1606760227091-3dd870d97f1d?q=80&w=400&h=400&fit=crop", 
                    110
                ),
                (
                    "i-Cup Reusable Medical Grade Menstrual Cup", 
                    "Menstrual cups", 
                    "Eco-friendly, chemical-free cup designed to fit comfortably without slipping or causing irritation.", 
                    279.00, 
                    "https://images.unsplash.com/photo-1606760227091-3dd870d97f1d?q=80&w=400&h=400&fit=crop", 
                    140
                ),

                # Category: Heating pads (9 products)
                (
                    "Electric Hot Water Bag / Gel Heating Pad", 
                    "Heating pads", 
                    "Quick-charge electric gel warm bag for soothing muscle aches, back pain, and period cramps.", 
                    299.00, 
                    "https://images.unsplash.com/photo-1542838132-92c53300491e?q=80&w=400&h=400&fit=crop", 
                    250
                ),
                (
                    "Sirona Feminine Herbal Pain Relief Patches (5 Pack)", 
                    "Heating pads", 
                    "Natural cooling/heating patches with menthol and eucalyptus oils to relieve menstrual cramps up to 8 hours.", 
                    199.00, 
                    "https://images.unsplash.com/photo-1515377905703-c4788e51af15?q=80&w=400&h=400&fit=crop", 
                    400
                ),
                (
                    "Sandpuppy Heatwrap Wireless Cramp Relief Band", 
                    "Heating pads", 
                    "Portable wireless heating band with adjustable strap. Ideal for back, joint, and period cramp relief.", 
                    1499.00, 
                    "https://images.unsplash.com/photo-1519689680058-324335c77eba?q=80&w=400&h=400&fit=crop", 
                    50
                ),
                (
                    "Flamingo Orthopaedic Heating Pad", 
                    "Heating pads", 
                    "Electric heating pad with multi-level temperature control and automatic cut-off feature.", 
                    899.00, 
                    "https://images.unsplash.com/photo-1600334089648-b0d9d3028eb2?q=80&w=400&h=400&fit=crop", 
                    120
                ),
                (
                    "HealthSense HeatMate Electric Period Cramp Belt", 
                    "Heating pads", 
                    "Rechargeable waist band offering vibration massage and fast thermal heating for quick cramp relief.", 
                    1299.00, 
                    "https://images.unsplash.com/photo-1515377905703-c4788e51af15?q=80&w=400&h=400&fit=crop", 
                    80
                ),
                (
                    "JSB HF06 Electric Heating Belt", 
                    "Heating pads", 
                    "Premium electric heating belt with remote control, soft washable cover, and overheating protection.", 
                    799.00, 
                    "https://images.unsplash.com/photo-1542838132-92c53300491e?q=80&w=400&h=400&fit=crop", 
                    100
                ),
                (
                    "Pee Safe Feminine Cramp Relief Roll-On (50ml)", 
                    "Heating pads", 
                    "Ayurvedic herbal formulation containing Satva Pudina and Eucalyptus oil to soothe stomach and pelvic cramps.", 
                    199.00, 
                    "https://images.unsplash.com/photo-1515377905703-c4788e51af15?q=80&w=400&h=400&fit=crop", 
                    350
                ),
                (
                    "Vandelay Electric Heating Pad", 
                    "Heating pads", 
                    "Large flannel heating wrap with 6 heat settings and auto shut-off function for reliable pain relief.", 
                    999.00, 
                    "https://images.unsplash.com/photo-1519689680058-324335c77eba?q=80&w=400&h=400&fit=crop", 
                    60
                ),
                (
                    "Agarwals Classic Electric Hot Water Bag", 
                    "Heating pads", 
                    "Silicon-based electrical warming bag. Ready to use in 5 minutes and retains heat for 2 hours.", 
                    349.00, 
                    "https://images.unsplash.com/photo-1542838132-92c53300491e?q=80&w=400&h=400&fit=crop", 
                    150
                ),

                # Category: Intimate hygiene products (9 products)
                (
                    "VWash Plus Intimate Hygiene Wash (200ml)", 
                    "Intimate hygiene products", 
                    "Enriched with Sea Buckthorn Oil and Tea Tree Oil to maintain the optimal pH level of 3.5.", 
                    320.00, 
                    "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?q=80&w=400&h=400&fit=crop", 
                    250
                ),
                (
                    "Pee Safe Natural Intimate Wash (105ml)", 
                    "Intimate hygiene products", 
                    "Foaming intimate wash containing lemongrass essential oil and witch hazel extract. Alcohol and paraben free.", 
                    249.00, 
                    "https://images.unsplash.com/photo-1556228578-0d85b1a4d571?q=80&w=400&h=400&fit=crop", 
                    180
                ),
                (
                    "Sirona Natural Intimate Wash (100ml)", 
                    "Intimate hygiene products", 
                    "pH balanced wash with olive oil, tea tree oil, and golden jojoba oil. Restores natural skin health.", 
                    199.00, 
                    "https://images.unsplash.com/photo-1608571423902-eed4a5ad8108?q=80&w=400&h=400&fit=crop", 
                    220
                ),
                (
                    "Lactacyd Daily Feminine Intimate Wash (250ml)", 
                    "Intimate hygiene products", 
                    "Gentle daily wash formulated with lactic acid and lactoserum to prevent irritation and bad odor.", 
                    399.00, 
                    "https://images.unsplash.com/photo-1601049541289-9b1b7bbbfe19?q=80&w=400&h=400&fit=crop", 
                    160
                ),
                (
                    "Everteen Natural Intimate Wash (105ml)", 
                    "Intimate hygiene products", 
                    "Formulated with neem, sea buckthorn, aloe vera, and chamomile extracts to protect against bacterial infections.", 
                    220.00, 
                    "https://images.unsplash.com/photo-1544816155-12df9643f363?q=80&w=400&h=400&fit=crop", 
                    190
                ),
                (
                    "Clean and Dry Daily Intimate Wash (100ml)", 
                    "Intimate hygiene products", 
                    "Restores normal pH balance, brightens skin tone, and prevents common yeast and bacterial infections.", 
                    175.00, 
                    "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?q=80&w=400&h=400&fit=crop", 
                    140
                ),
                (
                    "Sebamed Feminine Intimate Wash (pH 3.8, 200ml)", 
                    "Intimate hygiene products", 
                    "Dermatologically recommended pH 3.8 wash. Supports vaginal microflora during childbearing years.", 
                    699.00, 
                    "https://images.unsplash.com/photo-1601049541289-9b1b7bbbfe19?q=80&w=400&h=400&fit=crop", 
                    120
                ),
                (
                    "Carmesi Natural Foaming Intimate Wash (120ml)", 
                    "Intimate hygiene products", 
                    "Made with 100% plant-based ingredients. Free from parabens, sulfates, and synthetic fragrances.", 
                    299.00, 
                    "https://images.unsplash.com/photo-1556228578-0d85b1a4d571?q=80&w=400&h=400&fit=crop", 
                    110
                ),
                (
                    "Sanfe Intimate Wash with Lavender Oil (100ml)", 
                    "Intimate hygiene products", 
                    "Soothing lavender-infused wash designed to neutralize odor and keep you feeling clean all day.", 
                    199.00, 
                    "https://images.unsplash.com/photo-1608571423902-eed4a5ad8108?q=80&w=400&h=400&fit=crop", 
                    150
                ),

                # Category: Pregnancy kits (9 products)
                (
                    "Prega News Pregnancy Test Kit (Pack of 5)", 
                    "Pregnancy kits", 
                    "India's No. 1 pregnancy test kit. Quick, accurate, and easy-to-read results in 5 minutes.", 
                    250.00, 
                    "https://images.unsplash.com/photo-1631815589968-fdb09a223b1e?q=80&w=400&h=400&fit=crop", 
                    500
                ),
                (
                    "i-can One Step Pregnancy Test Kit (Pack of 3)", 
                    "Pregnancy kits", 
                    "High-precision urine pregnancy test kit. Detects hCG levels accurately even on day one of a missed period.", 
                    160.00, 
                    "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?q=80&w=400&h=400&fit=crop", 
                    300
                ),
                (
                    "Clearblue Digital Pregnancy Test", 
                    "Pregnancy kits", 
                    "Shows smart countdown and gives clear digital results ('Pregnant' or 'Not Pregnant') in words.", 
                    499.00, 
                    "https://images.unsplash.com/photo-1581594693702-fbdc51b2763b?q=80&w=400&h=400&fit=crop", 
                    150
                ),
                (
                    "Velocit Pregnancy Test Kit (Pack of 2)", 
                    "Pregnancy kits", 
                    "Easy-to-use dipstick test that provides high sensitivity and clear visual result lines.", 
                    120.00, 
                    "https://images.unsplash.com/photo-1584017911766-d451b3d0e843?q=80&w=400&h=400&fit=crop", 
                    200
                ),
                (
                    "Prega News Advance One-Step Test Cassette", 
                    "Pregnancy kits", 
                    "No need for a dropper or container. Simply hold the tip in the urine stream for 5 seconds.", 
                    100.00, 
                    "https://images.unsplash.com/photo-1631815589968-fdb09a223b1e?q=80&w=400&h=400&fit=crop", 
                    220
                ),
                (
                    "Prega News Value Pack (Pack of 10)", 
                    "Pregnancy kits", 
                    "Family planning bulk pack of 10 individually packed Prega News test kits for regular monitoring.", 
                    450.00, 
                    "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?q=80&w=400&h=400&fit=crop", 
                    150
                ),
                (
                    "Preganews Ultra Early Detection Kit", 
                    "Pregnancy kits", 
                    "Dermatologist-approved early detection kit with high sensitivity for hCG hormone detection.", 
                    180.00, 
                    "https://images.unsplash.com/photo-1581594693702-fbdc51b2763b?q=80&w=400&h=400&fit=crop", 
                    180
                ),
                (
                    "Prega News 5 Test Kits Combo Pack", 
                    "Pregnancy kits", 
                    "Value pack of 5 rapid detection strips. Fast and confidential pregnancy checking.", 
                    225.00, 
                    "https://images.unsplash.com/photo-1584017911766-d451b3d0e843?q=80&w=400&h=400&fit=crop", 
                    250
                ),
                (
                    "Clearblue Rapid Detection Pregnancy Test", 
                    "Pregnancy kits", 
                    "Fast results in 1 minute. Over 99% accurate from the day you expect your period.", 
                    299.00, 
                    "https://images.unsplash.com/photo-1631815589968-fdb09a223b1e?q=80&w=400&h=400&fit=crop", 
                    160
                )
            ]
            
            insert_query = """
            INSERT INTO products (product_name, category, description, price, image_url, stock_quantity)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.executemany(insert_query, products_data)
            print(f"[SUCCESS] Successfully seeded {len(products_data)} products into the database.")
            
            conn.commit()
            
    except Exception as e:
        print(f"[ERROR] Error setting up ecommerce tables: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    create_and_seed_tables()
