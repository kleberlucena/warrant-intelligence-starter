import pandas as pd
from unidecode import unidecode

def normalize_name(s: str) -> str:
    if not s:
        return ""
    s = unidecode(str(s)).strip()
    return " ".join(part.capitalize() for part in s.split())

def transform(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for col in ["name", "mother_name"]:
        if col in df.columns:
            df[col] = df[col].map(normalize_name)
    if "birth_date" in df.columns:
        df["birth_date"] = pd.to_datetime(df["birth_date"], errors="coerce").dt.date
    df = df.drop_duplicates(subset=["national_id", "name", "mother_name"], keep="first")
    return df
