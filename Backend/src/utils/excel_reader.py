from typing import List, Dict
import pandas as pd

def read_excel(file_path: str) -> List[Dict]:
    df = pd.read_excel(file_path)
    return df.to_dict(orient='records')