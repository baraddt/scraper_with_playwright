import pandas as pd


def get_links_from_excel(filepath):
    df = pd.read_excel(filepath)

    for col in df.columns:
        if df[col].astype(str).str.contains(r"https?://", na=False).any():
            return df[col].dropna().astype(str).tolist()

    print("[WARNING] Tidak ditemukan kolom berisi URL di file Excel.")
    return []
