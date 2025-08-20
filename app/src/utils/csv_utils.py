import pandas as pd

def read_csv(file):
    try:
        file.seek(0)
        return pd.read_csv(file)
    except pd.errors.ParserError:
        file.seek(0)
        return pd.read_csv(file, delimiter=';')
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

def check_timeliness(df, date_columns, threshold_days=3000):
    """
    Assess timeliness for given date columns.
    Returns DataFrame with columns: ['column', 'timeliness_percent']
    Timeliness is the percent of rows where the date is within threshold_days from today.
    """
    results = []
    today = pd.Timestamp.today()
    for col in date_columns:
        try:
            dates = pd.to_datetime(df[col], errors='coerce')
            timely = ((today - dates).dt.days <= threshold_days).sum()
            percent = timely / len(df) * 100 if len(df) > 0 else 0
        except Exception:
            percent = 0
        results.append({'column': col, 'timeliness_percent': percent})
    return pd.DataFrame(results)