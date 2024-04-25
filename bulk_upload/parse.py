from typing import List

import pandas as pd


def parse(url: str, columns: List[str] = None):
    df = pd.read_excel(url)
    df = df.astype(object).where(pd.notnull(df), None)
    if columns:
        if set(columns) - set(df.columns):
            raise Exception(f"Invalid file. {', '.join(set(columns) - set(df.columns))} column(s) not found.")
    return df.to_dict(orient="records")
