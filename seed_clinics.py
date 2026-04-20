import pymysql
from database import get_db_connection

def seed():
    conn = get_db_connection()
    if not conn:
        print("Could not connect to database")
        return
        
    clinics_data = [
        ("Asha Women's Care", "Dr. Smita Patel", "Gynecology", "Maharashtra", "Pune", "101, MG Road, Pune", "9876543210", "https://maps.google.com/"),
        ("LifeCare Maternity", "Dr. Neha Sharma", "Obstetrics & Gynecology", "Maharashtra", "Mumbai", "Bandra West, Mumbai", "9876543211", "https://maps.google.com/"),
        ("City Gynecology Hub", "Dr. Aditi Rao", "Women's Health", "Delhi", "New Delhi", "Connaught Place, New Delhi", "9876543212", "https://maps.google.com/"),
        ("Safe Beginnings Clinic", "Dr. Pooja Iyer", "Obstetrics", "Karnataka", "Bengaluru", "Koramangala, Bengaluru", "9876543213", "https://maps.google.com/"),
        ("Nurture Well Clinic", "Dr. Ritu Desai", "Gynecology & Obstetrics", "Gujarat", "Ahmedabad", "SG Highway, Ahmedabad", "9876543214", "https://maps.google.com/"),
        ("Eve's Wellness Center", "Dr. Kavita Singh", "Reproductive Health", "Tamil Nadu", "Chennai", "Adyar, Chennai", "9876543215", "https://maps.google.com/"),
        ("Blossom Maternity Home", "Dr. Meena Gupta", "Obstetrics & Gynecology", "Maharashtra", "Nagpur", "Civil Lines, Nagpur", "9876543216", "https://maps.google.com/"),
        ("Care for Her Clinic", "Dr. Shalini Verma", "Gynecology", "Uttar Pradesh", "Lucknow", "Gomti Nagar, Lucknow", "9876543217", "https://maps.google.com/"),
        ("Divine Motherhood Center", "Dr. Aisha Khan", "Women's Health", "Telangana", "Hyderabad", "Banjara Hills, Hyderabad", "9876543218", "https://maps.google.com/"),
        ("Vitality Women's Clinic", "Dr. Sunita Reddy", "Endocrinology & Women's Health", "Andhra Pradesh", "Visakhapatnam", "MVP Colony, Vizag", "9876543219", "https://maps.google.com/")
    ]

    try:
        with conn.cursor() as cursor:
            # Check what columns exist so we don't crash if optional ones are missing from the table schema
            cursor.execute("DESCRIBE clinics")
            columns_info = cursor.fetchall()
            existing_cols = [col['Field'] for col in columns_info]
            
            insert_cols = ['clinic_name', 'doctor_name', 'specialization', 'state', 'city', 'address']
            data_indices = [0, 1, 2, 3, 4, 5]
            
            if 'contact_number' in existing_cols:
                insert_cols.append('contact_number')
                data_indices.append(6)
            if 'google_maps_link' in existing_cols:
                insert_cols.append('google_maps_link')
                data_indices.append(7)
                
            col_list_str = ', '.join(insert_cols)
            val_placeholder = ', '.join(['%s'] * len(insert_cols))
            
            query = f"INSERT INTO clinics ({col_list_str}) VALUES ({val_placeholder})"
            
            success_count = 0
            for clinic in clinics_data:
                # build the tuple matching the columns present
                insert_data = tuple(clinic[i] for i in data_indices)
                try:
                    cursor.execute(query, insert_data)
                    success_count += 1
                except Exception as inner_e:
                    print(f"Skipping insert for {clinic[0]} due to: {inner_e}")
            print(f"Successfully added {success_count} clinics to the database.")
    except Exception as e:
        print(f"Error seeding data: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    seed()
