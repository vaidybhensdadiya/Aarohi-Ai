"""
Clinics services for Aarohi AI.

This module contains business logic for clinics operations
like clinic search, appointment booking, and location services.
"""

from database import get_db_connection

def get_nearby_clinics(state=None, city=None):
    """
    Fetch nearby gynecologist clinics from the database based on optional filters.
    
    Args:
        state (str): State to filter by.
        city (str): City to filter by.
        
    Returns:
        list: A list of clinic dictionaries.
    """
    conn = get_db_connection()
    clinics_list = []
    
    if not conn:
        return clinics_list

    try:
        with conn.cursor() as cursor:
            # We broaden the search to match 'Gynecolo', 'Obstetric', or 'Women'
            query = "SELECT * FROM clinics WHERE (specialization LIKE %s OR specialization LIKE %s OR specialization LIKE %s)"
            params = ['%Gynecol%', '%Obstetric%', '%Women%']
            
            if state:
                query += " AND LOWER(state) = LOWER(%s)"
                params.append(state)
                
            if city:
                query += " AND LOWER(city) = LOWER(%s)"
                params.append(city)
            
            cursor.execute(query, params)
            clinics_list = cursor.fetchall()
            
    except Exception as e:
        print(f"Error fetching nearby clinics: {e}")
    finally:
        conn.close()
        
    return clinics_list
