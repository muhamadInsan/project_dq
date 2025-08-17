import pandas as pd

def read_csv(file):
    try:
        file.seek(0)  # Reset file pointer
        # Try to auto-detect delimiter
        return pd.read_csv(file)
    except pd.errors.ParserError:
        file.seek(0)
        return pd.read_csv(file, delimiter=';')  # Try semicolon as fallback
    except Exception as e:
        raise ValueError(f"Failed to read CSV: {e}")

def validate_csv(file):
    if not file.name.endswith('.csv'):
        raise ValueError("The uploaded file is not a CSV file.")
    file.seek(0, 2)  # Move to end of file
    if file.tell() == 0:
        raise ValueError("The uploaded CSV file is empty.")
    file.seek(0)  # Reset pointer