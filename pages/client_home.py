
import streamlit as st

st.set_page_config(page_title="客戶專屬服務", layout="centered")
st.title("客戶專屬服務")

options = {
    "遺產稅規劃": "5_estate_tax.py",
    "退休規劃": "6_retirement.py",
    "資產地圖": "7_asset_map.py"
}

cols = st.columns(len(options), gap="medium")
for idx, (label, page) in enumerate(options.items()):
    with cols[idx]:
        if st.button(label, use_container_width=True):
            st.switch_page(f"{page}")
