# app/streamlit_app.py
import streamlit as st
from datetime import datetime
from utils import load_all, kin_lookup, date_to_maya_birthday

# -----------------------------------------------------------------------------
# 初始
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="瑪雅印記查詢系統",
    page_icon="🗿",
    layout="wide"
)

st.title("🗿 瑪雅印記查詢系統")
st.markdown(
    """
    這個應用會自動載入 `data/` 資料夾下所有 `.csv` 和 `.xlsx` 檔案，
    並提供以下功能：
    - **KIN 查詢**：輸入 KIN 編號，搜尋矩陣表中的對應資料。  
    - **日期轉瑪雅生日**：輸入西元日期，查詢對應的瑪雅生日。  
    """
)

# -----------------------------------------------------------------------------
# 載入所有資料表
# -----------------------------------------------------------------------------
with st.spinner("📥 正在讀取資料..."):
    data_dict = load_all()
st.success(f"✅ 已載入 {len(data_dict)} 張資料表")

# -----------------------------------------------------------------------------
# 側邊選單
# -----------------------------------------------------------------------------
mode = st.sidebar.radio("選擇功能", ["KIN 查詢", "日期轉瑪雅生日", "檢視已載入資料表"])

# -----------------------------------------------------------------------------
# 功能：檢視已載入資料表
# -----------------------------------------------------------------------------
if mode == "檢視已載入資料表":
    st.header("📑 已載入資料表列表")
    for key in sorted(data_dict.keys()):
        df = data_dict[key]
        st.subheader(f"- `{key}` （{df.shape[0]} 列 × {df.shape[1]} 欄）")
        st.dataframe(df.head(5), height=200)
    st.stop()

# -----------------------------------------------------------------------------
# 功能：KIN 查詢
# -----------------------------------------------------------------------------
if mode == "KIN 查詢":
    st.header("🔢 KIN 查詢")
    kin_input = st.number_input("請輸入 KIN 編號", min_value=1, max_value=260, value=1, step=1)
    if st.button("開始查詢"):
        try:
            result = kin_lookup(int(kin_input), data_dict)
            st.success(f"找到 KIN {kin_input} 的對應資料：")
            # 轉成 DataFrame 顯示
            import pandas as pd
            df = pd.DataFrame([result])
            st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error(f"❌ 查詢失敗：{e}")

# -----------------------------------------------------------------------------
# 功能：日期轉瑪雅生日
# -----------------------------------------------------------------------------
elif mode == "日期轉瑪雅生日":
    st.header("📅 日期轉瑪雅生日")
    col1, col2 = st.columns(2)
    with col1:
        date_input = st.date_input("請選擇西元日期", datetime.today())
    with col2:
        if st.button("轉換"):
            try:
                maya_bd = date_to_maya_birthday(date_input, data_dict)
                st.success(f"對應的瑪雅生日：**{maya_bd}**")
            except Exception as e:
                st.error(f"❌ 轉換失敗：{e}")
