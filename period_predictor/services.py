"""
Period Predictor services for Aarohi AI.

Validates inputs, calls ML prediction, saves to period_prediction table.
"""

from datetime import datetime
from typing import Optional, Tuple

from database import get_db_connection
from ml.predict_period import predict_from_inputs


def validate_inputs(data: dict) -> Tuple[bool, str]:
    """
    Validate form inputs.
    Returns (is_valid, error_message).
    """
    last_period = data.get("last_period_start_date")
    cycle_length = data.get("cycle_length")
    period_duration = data.get("period_duration")

    if not last_period or not isinstance(last_period, str):
        return False, "Last period start date is required"

    try:
        dt = datetime.strptime(last_period, "%Y-%m-%d")
    except ValueError:
        return False, "Invalid date format for last period"

    if cycle_length is not None and cycle_length != "":
        try:
            cl = int(cycle_length)
            if cl < 24 or cl > 35:
                return False, "Cycle length must be between 24 and 35 days"
        except (ValueError, TypeError):
            return False, "Invalid cycle length"

    if period_duration is not None and period_duration != "":
        try:
            pd_val = int(period_duration)
            if pd_val < 1 or pd_val > 10:
                return False, "Period duration must be between 1 and 10 days"
        except (ValueError, TypeError):
            pass  # Optional field

    return True, ""


def save_prediction(
    user_id: int,
    last_period_start_date: str,
    cycle_length: int,
    period_duration: int,
    cramps: int,
    mood_swings: int,
    headache: int,
    fatigue: int,
    bloating: int,
    predicted_next_start_date,
) -> bool:
    """Insert prediction into period_prediction table."""
    conn = get_db_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO period_prediction (
                user_id, last_period_start_date, cycle_length, period_duration,
                cramps, mood_swings, headache, fatigue, bloating,
                predicted_next_start_date
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (
                user_id,
                last_period_start_date,
                cycle_length,
                period_duration,
                cramps,
                mood_swings,
                headache,
                fatigue,
                bloating,
                predicted_next_start_date,
            ),
        )
        cursor.close()
        return True
    except Exception as e:
        print("period_prediction insert error:", e)
        return False
    finally:
        if conn:
            conn.close()


def run_prediction(user_id: int, data: dict) -> Tuple[Optional[dict], Optional[str]]:
    """
    Run full prediction flow: validate, predict, save, return result.
    Returns (result_dict, error_message).
    """
    is_valid, err = validate_inputs(data)
    if not is_valid:
        return None, err

    last_period = data.get("last_period_start_date")
    cycle_length = int(data.get("cycle_length", 28))
    period_duration = int(data.get("period_duration", 5))
    cramps = int(data.get("cramps", 0))
    mood_swings = int(data.get("mood_swings", 0))
    headache = int(data.get("headache", 0))
    fatigue = int(data.get("fatigue", 0))
    bloating = int(data.get("bloating", 0))

    result = predict_from_inputs(last_period)
    if not result:
        return None, "Prediction failed"

    predicted_date = result.get("next_period_date")
    if not predicted_date:
        return None, "Could not compute predicted date"

    save_prediction(
        user_id=user_id,
        last_period_start_date=last_period,
        cycle_length=cycle_length,
        period_duration=period_duration,
        cramps=cramps,
        mood_swings=mood_swings,
        headache=headache,
        fatigue=fatigue,
        bloating=bloating,
        predicted_next_start_date=predicted_date,
    )

    result["predicted_next_start_date"] = str(predicted_date)
    return result, None
