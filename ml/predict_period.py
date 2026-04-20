import os
import pymysql
import joblib
import pandas as pd
from datetime import timedelta, datetime


# Load trained model
_ml_dir = os.path.dirname(os.path.abspath(__file__))
model = joblib.load(os.path.join(_ml_dir, "period_cycle_model.pkl"))


def predict_from_inputs(last_period_date_str):
    """
    Predict next period using form inputs (no DB lookup).
    Uses ML model with last_period_date ordinal to predict cycle length.
    Returns dict with next_period_date (YYYY-MM-DD) or None on error.
    """
    try:
        last_start = pd.to_datetime(last_period_date_str)
        last_start_ordinal = last_start.toordinal()
        predicted_cycle = model.predict([[last_start_ordinal]])[0]
        predicted_cycle = round(float(predicted_cycle))
        predicted_cycle = max(24, min(35, predicted_cycle))  # Clamp to valid range
        next_period_date = last_start + timedelta(days=predicted_cycle)
        return {
            "last_period": last_start.date(),
            "predicted_cycle_length": predicted_cycle,
            "next_period_date": next_period_date.date(),
        }
    except Exception as e:
        print("predict_from_inputs error:", e)
        return None


def predict_next_period(user_id):
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="Vaidy@2005",
        database="aarohi_ai"
    )

    query = """
    SELECT period_start_date
    FROM menstrual_cycles
    WHERE user_id = %s
    ORDER BY period_start_date DESC
    LIMIT 1
    """

    df = pd.read_sql(query, conn, params=[user_id])

    if df.empty:
        return None

    last_start = pd.to_datetime(df.iloc[0]["period_start_date"])
    last_start_ordinal = last_start.toordinal()

    predicted_cycle = model.predict([[last_start_ordinal]])[0]
    predicted_cycle = round(predicted_cycle)

    next_period_date = last_start + timedelta(days=predicted_cycle)

    return {
        "last_period": last_start.date(),
        "predicted_cycle_length": predicted_cycle,
        "next_period_date": next_period_date.date()
    }
