# app/utils.py
import os
import pandas as pd
from datetime import datetime
from typing import Dict

def load_all() -> Dict[str, pd.DataFrame]:
    """
    自動掃描 data/ 資料夾，讀取所有 .csv 和 .xlsx 檔案，
    依檔名（去副檔名）當成 key，回傳 DataFrame dict。
    """
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    files = os.listdir(data_dir)
    dfs: Dict[str, pd.DataFrame] = {}

    for fn in files:
        path = os.path.join(data_dir, fn)
        name, ext = os.path.splitext(fn)
        try:
            if ext.lower() == '.csv':
                dfs[name] = pd.read_csv(path, dtype=str)
            elif ext.lower() in ('.xls', '.xlsx'):
                dfs[name] = pd.read_excel(path, engine='openpyxl', dtype=str)
            # 若需要處理其他格式，再加條件即可
        except Exception as e:
            # 讀檔失敗時，印出警告，但不中斷
            print(f"⚠️ 無法讀取 {fn}：{e}")

    return dfs


def kin_lookup(kin_number: int, data: Dict[str, pd.DataFrame]) -> Dict:
    """
    根據 KIN 編號回傳對應矩陣表中的一筆記錄。
    假設矩陣表檔名包含「矩陣」或精確為 matrix、matrix表…，
    你可在這邊調整 key 值以配你的檔名，例如 data['矩陣表']。
    """
    # 請確認你的矩陣表檔名
    df = None
    for key in data:
        if '矩陣' in key or 'matrix' in key.lower():
            df = data[key]
            break
    if df is None:
        raise FileNotFoundError("找不到包含「矩陣」的 DataFrame，請檢查 data/ 中的檔名。")

    df = df.copy()
    # 假設欄位叫 'KIN'
    df['KIN'] = pd.to_numeric(df['KIN'], errors='coerce')
    row = df[df['KIN'] == kin_number]
    if row.empty:
        raise ValueError(f"KIN {kin_number} 不存在於矩陣表")
    return row.iloc[0].to_dict()


def date_to_maya_birthday(date: datetime, data: Dict[str, pd.DataFrame]) -> str:
    """
    輸入 datetime 或 date，回傳對應的瑪雅生日字串，
    假設對應表檔名含有「瑪雅生日」或 'maya_birthday'。
    """
    key_df = None
    for key in data:
        if '瑪雅生日' in key or 'maya' in key.lower():
            key_df = data[key]
            break
    if key_df is None:
        return "找不到瑪雅生日對照表"

    key_df = key_df.copy()
    # 假設有欄位 '國曆月日' 與 '瑪雅生日'
    key_df['國曆月日'] = key_df['國曆月日'].astype(str)
    lookup = date.strftime('%m/%d').lstrip('0').replace('/0','/')
    row = key_df[key_df['國曆月日'] == lookup]
    return row['瑪雅生日'].values[0] if not row.empty else "無對應瑪雅生日"

# utils.py 中新增

# 1) 年度 → 流年印記對照表（示例只列 2000～2005，可擴充到完整區間）
YEAR_TO_NUM = {
    2000: 152, 2001: 257, 2002: 102, 2003: 207,
    2004: 52,  2005: 157, # … 其他年份 …
}

# 2) 月份累計天數（非閏年）
MONTH_OFFSET = {
    1:   0,
    2:  31,
    3:  59,
    4:  90,
    5: 120,
    6: 151,
    7: 181,
    8: 212,
    9: 243,
    10: 273,  # 注意：因為 9 月 30 天→243+30=273，之前示例表格末尾用了 13 for October but那是跨年用
    11: 304,  # 273+31
    12: 334,  # 304+30
}

# 3) 日 → 偏移（1→1, …, 29上→28, 29下→1）
def day_offset(day: int, is_leap_29_low: bool=False) -> int:
    # 如果需要處理農曆閏二月（29上、29下），這裡用 is_leap_29_low 標記下層29
    if day == 29 and is_leap_29_low:
        return 1
    return day

def birthdate_to_kin(year: int, month: int, day: int, is_leap_29_low: bool=False) -> int:
    """
    將西元年、月、日轉成瑪雅 KIN (1~260)：

    - year: 4 位數西元年
    - month: 1~12
    - day: 1~31
    - is_leap_29_low: 若輸入「29 下」請傳 True，否則傳 False
    """
    # 1) 取得年度數字
    if year not in YEAR_TO_NUM:
        raise ValueError(f"年份 {year} 不在可查範圍內")
    y_num = YEAR_TO_NUM[year]

    # 2) 取得月份偏移
    if month not in MONTH_OFFSET:
        raise ValueError(f"月份 {month} 不可接受")
    m_off = MONTH_OFFSET[month]

    # 3) 取得日期偏移
    d_off = day_offset(day, is_leap_29_low)

    # 4) 加總並對 260 取餘
    kin = (y_num + m_off + d_off) % 260
    return kin or 260

