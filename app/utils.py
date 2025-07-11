import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"

def load_all():
    tables = {}
    # Excel files
    excel_files = [
        "52流年計算.xlsx","流年印記.xlsx","個人流日印記.xlsx","矩陣表.xlsx",
        "國王預言棋盤.xlsx","對等印記.xlsx","PSI印記.xlsx","八個光點計算.xlsx",
        "女神印記.xlsx","內在小孩計算.xlsx","主印記查詢表.xlsx","全腦調頻.xlsx",
        "合盤印記.xlsx"
    ]
    for fname in excel_files:
        path = DATA_DIR / fname
n        if path.exists():
            tables[fname] = pd.read_excel(path, sheet_name=None)
    # CSV files
    csv_files = [
        "對應瑪雅生日.csv","瑪雅圖騰對照表.csv","銀河易經編碼.csv",
        "光點對照表.csv","卓爾金曆KIN對照表.csv"
    ]
    for fname in csv_files:
        path = DATA_DIR / fname
        if path.exists():
            tables[fname] = pd.read_csv(path)
    return tables

def kin_lookup(tables, kin):
    df = tables.get("卓爾金曆KIN對照表.csv")
    if df is None:
        return []
    row = df[df["KIN"] == kin]
    return row.to_dict(orient="records")

def date_to_maya_birthday(tables, month, day):
    df = tables.get("對應瑪雅生日.csv")
    if df is None:
        return []
    code = f"{month:02d}/{day:02d}"
    row = df[df["國曆月日"] == code]
    return row.to_dict(orient="records")
