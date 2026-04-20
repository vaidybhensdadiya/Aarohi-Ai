import random
from datetime import datetime, timedelta
import pymysql

# -----------------------------
# DB CONFIG (same as your app)
# -----------------------------
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Vaidy@2005",
    "database": "aarohi_ai",
    "port": 3306,
    "cursorclass": pymysql.cursors.DictCursor,
    "autocommit": True,
}

TOTAL_ROWS = 500
USER_ID = 1  # can be same user for ML training


def generate_record(base_date):
    cycle_length = random.randint(24, 35)
    period_duration = random.randint(3, 7)

    period_start = base_date
    period_end = period_start + timedelta(days=period_duration)

    # Symptoms
    cramps = random.choice([0, 1])
    mood_swings = random.choice([0, 1])
    headache = random.choice([0, 1])
    fatigue = random.choice([0, 1])
    bloating = random.choice([0, 1])

    # Add small realistic variation for next cycle
    variation = random.randint(-2, 2)

    symptom_impact = (
        (cramps * -1)
        + (fatigue * 1)
        + (mood_swings * 0)
    )

    next_cycle_length = cycle_length + variation + symptom_impact
    next_cycle_length = max(24, min(35, next_cycle_length))

    predicted_next_start = period_start + timedelta(days=next_cycle_length)

    return (
        USER_ID,
        period_start.date(),
        period_end.date(),
        cycle_length,
        period_duration,
        cramps,
        mood_swings,
        headache,
        fatigue,
        bloating,
        next_cycle_length,
        predicted_next_start.date(),
    )


def main():
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()

    start_date = datetime.today() - timedelta(days=TOTAL_ROWS * 30)

    insert_query = """
        INSERT INTO period_records (
            user_id,
            period_start_date,
            period_end_date,
            cycle_length,
            period_duration,
            cramps,
            mood_swings,
            headache,
            fatigue,
            bloating,
            next_cycle_length,
            predicted_next_start_date
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    current_date = start_date

    for _ in range(TOTAL_ROWS):
        record = generate_record(current_date)
        cursor.execute(insert_query, record)

        # move forward by cycle length
        current_date += timedelta(days=record[3])

    cursor.close()
    conn.close()

    print(f"✅ {TOTAL_ROWS} period records inserted successfully")


if __name__ == "__main__":
    main()
