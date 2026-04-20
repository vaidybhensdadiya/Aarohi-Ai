"""
Database seeder for additional Government Schemes focused on women's health and empowerment.
"""

import os
from database import get_db_connection

def seed_more_schemes():
    conn = get_db_connection()
    if not conn:
        print("Failed to connect to the database.")
        return

    try:
        cursor = conn.cursor()

        # Check existing to prevent full duplication (a simple check)
        cursor.execute("SELECT COUNT(*) as count FROM government_schemes")
        result = cursor.fetchone()
        
        # New comprehensive schemes for seeding
        additional_schemes = [
            (
                "Maternity Benefit Programme (MBP)",
                "Provides partial compensation for wage loss so that the woman can take adequate rest before and after delivery of the first child.",
                19, 45, 800000, None, "All", True,
                "Cash benefit of Rs. 6000 directly transferred to the bank account.",
                "https://wcd.nic.in/schemes/maternity-benefit-programme"
            ),
            (
                "Working Women Hostel Scheme",
                "Promotes the availability of safe and conveniently located accommodation for working women, with day care facility for their children.",
                18, 60, None, None, "All", False,
                "Safe, affordable hostel accommodation and day-care for children.",
                "https://wcd.nic.in/schemes/working-women-hostel"
            ),
            (
                "STEP (Support to Training and Employment Programme for Women)",
                "Provides skills that give employability to women and to provide competencies and skill that enable women to become self-employed.",
                16, 50, None, None, "All", False,
                "Skill development and employment provision.",
                "https://wcd.nic.in/schemes/support-training-and-employment-programme-women-step"
            ),
            (
                "Swadhar Greh Scheme",
                "Targets women victims of difficult circumstances who are in need of institutional support for rehabilitation so that they could lead their life with dignity.",
                18, 60, None, None, "All", False,
                "Shelter, food, clothing, medical treatment and care.",
                "https://wcd.nic.in/schemes/swadhar-greh-scheme-women-difficult-circumstances"
            ),
            (
                "Ujjawala Scheme",
                "A comprehensive scheme for prevention of trafficking and rescue, rehabilitation, re-integration and repatriation of victims of trafficking.",
                0, 60, None, None, "All", False,
                "Rehabilitation centers, medical care, legal aid, and vocational training.",
                "https://wcd.nic.in/schemes/ujjawala-comprehensive-scheme-prevention-trafficking-and-rescue-rehabilitation-re"
            ),
            (
                "Rajiv Gandhi Scheme for Empowerment of Adolescent Girls (SABLA)",
                "Empowers adolescent girls by improving their nutritional and health status, and upgrading various skills like home skills, life skills and vocational skills.",
                11, 18, None, None, "All", False,
                "Nutrition provision, iron/folic acid supplementation, health check-up, and family welfare education.",
                "https://wcd.nic.in/schemes/rajiv-gandhi-scheme-empowerment-adolescent-girls-sabla"
            ),
            (
                "Indira Gandhi Matritva Sahyog Yojana (IGMSY)",
                "Conditional Maternity Benefit scheme for pregnant and lactating women to improve health and nutrition status.",
                19, 45, None, None, "All", True,
                "Cash incentive paid in installments directly into bank accounts.",
                "https://wcd.nic.in/schemes/indira-gandhi-matritva-sahyog-yojana-igmsy"
            ),
            (
                "Nari Shakti Puraskar",
                "National award to recognize women and institutions that have made significant contributions towards the empowerment of women.",
                25, 100, None, None, "All", False,
                "Recognition, certificate, and cash award.",
                "https://wcd.nic.in/schemes/nari-shakti-puraskar"
            ),
            (
                "Mahila E-Haat",
                "Online marketing platform for women entrepreneurs / SHGs / NGOs.",
                18, 60, None, None, "All", False,
                "Free digital platform to showcase products and services.",
                "http://mahilaehaat-rmk.gov.in"
            ),
            (
                "One Stop Centre Scheme",
                "Provides integrated support and assistance to women affected by violence, both in private and public spaces under one roof.",
                0, 100, None, None, "All", False,
                "Medical aid, police assistance, legal counseling, and temporary shelter.",
                "https://wcd.nic.in/schemes/one-stop-centre-scheme-1"
            )
        ]

        insert_query = """
        INSERT INTO government_schemes 
        (scheme_name, description, min_age, max_age, max_income, state, category, pregnancy_required, benefits, official_link)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        # Insert them individually to avoid crashing if one matches a unique key constraint
        # (though there isn't one, it's safer)
        count = 0
        for scheme in additional_schemes:
            cursor.execute(insert_query, scheme)
            count += 1
            
        conn.commit()
        print(f"✅ Successfully seeded {count} additional government schemes into the database!")

    except Exception as e:
        print(f"❌ Error seeding schemes: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    seed_more_schemes()
