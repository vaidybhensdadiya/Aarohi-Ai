"""
Schemes services for Aarohi AI.

Business logic for reading schemes from the database and applying
simple eligibility rules based on age and state.
"""

from typing import List, Tuple, Optional

from database import get_db_connection


def get_eligible_schemes(age: int, state: Optional[str] = None) -> List[dict]:
    """
    Return schemes the user is eligible for, based on:
    - age: between min_age and max_age (when present)
    - state: either matching user's state or pan-India (NULL / 'All India')

    Data is read from `government_schemes` table defined in schema_features.sql.
    """
    conn = get_db_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor()

        sql = """
            SELECT
                id,
                scheme_name,
                description,
                category,
                state,
                official_link
            FROM government_schemes
            WHERE 1 = 1
              AND (min_age IS NULL OR %s >= min_age)
              AND (max_age IS NULL OR %s <= max_age)
        """
        params: List = [age, age]

        if state and state != 'All India':
            sql += " AND (state = %s OR state = 'All India' OR state IS NULL OR state = '')"
            params.append(state)

        sql += " ORDER BY scheme_name ASC"

        cursor.execute(sql, params)
        rows = cursor.fetchall()
        cursor.close()
        return rows or []
    except Exception as e:
        print("❌ Error fetching eligible schemes:", e)
        return []
    finally:
        if conn:
            conn.close()


def get_states() -> List[str]:
    """
    Return distinct states from government_schemes table
    for the state filter dropdown.
    """
    conn = get_db_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT DISTINCT state FROM government_schemes "
            "WHERE state IS NOT NULL AND state <> '' ORDER BY state"
        )
        state_rows = cursor.fetchall()
        cursor.close()
        return [row["state"] for row in state_rows if row.get("state")]
    except Exception as e:
        print("❌ Error fetching scheme states:", e)
        return []
    finally:
        if conn:
            conn.close()


