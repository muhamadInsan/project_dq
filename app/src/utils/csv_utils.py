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