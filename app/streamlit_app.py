import streamlit as st
from app.utils import load_all, kin_lookup, date_to_maya_birthday

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
