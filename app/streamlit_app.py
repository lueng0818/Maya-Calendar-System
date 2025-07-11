import streamlit as st
# app/streamlit_app.py

import streamlit as st

# 相對 import
from .utils import load_all, kin_lookup, date_to_maya_birthday

def main():
    st.title("瑪雅印記查詢系統")
    # 載入所有資料
    data = load_all()
    # 介面：輸入日期 → 查 KIN → 顯示結果
    date = st.date_input("請選擇公曆日期")
    maya_bday = date_to_maya_birthday(date)
    kin = kin_lookup(maya_bday, data)
    st.write(f"對應 KIN：{kin}")
    # （依你的 utils.py 實作再顯示更多欄位）
    # ...

if __name__ == "__main__":
    main()

st.set_page_config(page_title="瑪雅印記查詢系統", layout="wide")
st.title("🌟 瑪雅印記查詢系統")

tables = load_all()
query = st.sidebar.selectbox("選擇查詢類型", ["KIN 查詢", "日期→瑪雅生日"])

if query == "KIN 查詢":
    kin = st.sidebar.number_input("輸入 KIN 編號", min_value=1, max_value=260, value=1)
    if st.sidebar.button("查詢"):
        result = kin_lookup(tables, kin)
        st.write(f"### KIN {kin} 資料：")
        st.json(result)

elif query == "日期→瑪雅生日":
    month = st.sidebar.selectbox("月", list(range(1,13)))
    day = st.sidebar.selectbox("日", list(range(1,32)))
    if st.sidebar.button("查詢"):
        result = date_to_maya_birthday(tables, month, day)
        st.write(f"### {month:02d}/{day:02d} → 瑪雅生日：")
        st.json(result)

st.sidebar.markdown("---")
st.sidebar.write("© 2025 瑪雅印記查詢系統")
