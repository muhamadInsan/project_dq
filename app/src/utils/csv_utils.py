import pandas as pd
from datetime import time
import re

def read_csv(file):
    try:
        file.seek(0)
        return pd.read_csv(file)
    except pd.errors.ParserError:
        file.seek(0)
        return pd.read_csv(file, delimiter=';', keep_date_col=True, parse_dates=True)
    except Exception as e:
        raise ValueError(f"Failed to read CSV: {e}")

def validate_csv(file):
    if not file.name.endswith('.csv'):
        raise ValueError("The uploaded file is not a CSV file.")
    file.seek(0, 2)
    if file.tell() == 0:
        raise ValueError("The uploaded CSV file is empty.")
    file.seek(0)

def check_completeness(df):
    """
    Returns a DataFrame with columns: ['column', 'completeness_percent']
    """
    completeness = df.notnull().mean() * 100
    return pd.DataFrame({
        'column': completeness.index,
        'completeness_percent': completeness.values
    })

def check_uniqueness(df):
    """
    Returns a DataFrame with columns: ['column', 'uniqueness_percent']
    """
    uniqueness = df.nunique(dropna=False) / len(df) * 100 if len(df) > 0 else 0
    return pd.DataFrame({
        'column': uniqueness.index,
        'uniqueness_percent': uniqueness.values
    })

def check_timeliness(df, date_columns, time_column=None, frequency="Daily", cutoff_time=None):
    """
    Assess timeliness for given date columns and time column.
    For each row, timeliness is True if:
      - The date is within the latest 'cutoff_time' units (e.g., last 5 days for Daily, last 2 months for Monthly)
      - If time_column and cutoff_time (as time) are provided, the time is <= cutoff_time
    Returns DataFrame with columns: ['column', 'timeliness_percent']add
    """
    freq_days = {
        "Daily": 1,
        "Weekly": 7,
        "Monthly": 30,
        "Quarterly": 90,
        "Yearly": 365
    }
    results = []
    today = pd.Timestamp.today()
    # If cutoff_time is int, treat as number of frequency units
    if isinstance(cutoff_time, int):
        threshold_days = cutoff_time * freq_days.get(frequency, 1)
    else:
        threshold_days = freq_days.get(frequency, 1)  # fallback to 1 unit

    for col in date_columns:
        try:
            dates = pd.to_datetime(df[col], errors='coerce')
            # Timeliness by date: within threshold_days from today
            timely_date_mask = ((today - dates).dt.days < threshold_days)
            # Timeliness by time (if provided)
            if time_column and cutoff_time and isinstance(cutoff_time, time) and time_column in df.columns:
                times = pd.to_datetime(df[time_column], errors='coerce').dt.time
                timely_time_mask = times <= cutoff_time
                timely_mask = timely_date_mask & timely_time_mask
            else:
                timely_mask = timely_date_mask
            percent = timely_mask.sum() / len(df) * 100 if len(df) > 0 else 0
        except Exception:
            percent = 0
        results.append({'column': col, 'timeliness_percent': percent})
    return pd.DataFrame(results)

def check_validity(df, column, condition, value):
    """
    Check validity for a column based on a condition and value.
    Supported conditions: 'equal', 'min', 'max', 'in', 'between', 'regex'
    Returns percentage of valid rows.
    """
    valid_mask = pd.Series([False] * len(df))
    if condition == "equal":
        valid_mask = df[column] == value
    elif condition == "min":
        valid_mask = df[column] >= value
    elif condition == "max":
        valid_mask = df[column] <= value
    elif condition == "in":
        valid_mask = df[column].isin(value if isinstance(value, list) else [value])
    elif condition == "between":
        if isinstance(value, (list, tuple)) and len(value) == 2:
            valid_mask = df[column].between(value[0], value[1])
    elif condition == "regex":
        # Example: r"^[A-Za-z0-9]+$" for alphanumeric values only
        pattern = value if isinstance(value, str) else ""
        valid_mask = df[column].astype(str).str.match(pattern)
    percent = valid_mask.sum() / len(df) * 100 if len(df) > 0 else 0
    return percent