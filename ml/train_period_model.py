import pandas as pd
import pymysql
from datetime import timedelta
from sklearn.linear_model import LinearRegression
import joblib

import sys
import os

# Allow importing config from parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import Config

# -----------------------------
# DATABASE CONNECTION
# -----------------------------
conn = pymysql.connect(
    host=Config.DB_HOST,
    user=Config.DB_USER,
    password=Config.DB_PASSWORD,
    database=Config.DB_NAME,
    port=Config.DB_PORT
)

query = "SELECT * FROM period_records"
df = pd.read_sql(query, conn)

print("[INFO] Raw rows:", len(df))

# -----------------------------
# REMOVE HEADER-LIKE ROWS
# -----------------------------
df = df[df["cycle_length"] != "cycle_length"]

# -----------------------------
# TYPE CONVERSION
# -----------------------------
df["cycle_length"] = pd.to_numeric(df["cycle_length"], errors="coerce")
df["period_duration"] = pd.to_numeric(df["period_duration"], errors="coerce")

df["period_start_date"] = pd.to_datetime(
    df["period_start_date"], errors="coerce"
)

# -----------------------------
# FILTER VALID DATA
# -----------------------------
df = df[
    (df["cycle_length"] >= 24) &
    (df["cycle_length"] <= 35)
]

df = df.dropna(subset=["cycle_length", "period_start_date"])

print("[INFO] Clean rows used for training:", len(df))

if len(df) < 10:
    print("[ERROR] Not enough clean data to train model")
    exit()

# -----------------------------
# FEATURE ENGINEERING
# -----------------------------
df["start_ordinal"] = df["period_start_date"].map(pd.Timestamp.toordinal)

X = df[["start_ordinal"]]
y = df["cycle_length"]

# -----------------------------
# TRAIN MODEL
# -----------------------------
model = LinearRegression()
model.fit(X, y)

# -----------------------------
# SAVE MODEL
# -----------------------------
joblib.dump(model, "ml/period_cycle_model.pkl")

print("[SUCCESS] Model trained and saved successfully!")
