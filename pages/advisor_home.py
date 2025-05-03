
import streamlit as st

st.set_page_config(page_title="顧問專屬服務", layout="centered")
st.title("顧問專屬服務")

options = {
    "保險策略規劃": "8_insurance_strategy.py",
    "風險檢核": "9_risk_check.py",
    "客戶案例": "2_cases.py"
}

cols = st.columns(len(options), gap="medium")
for idx, (label, page) in enumerate(options.items()):
    with cols[idx]:
        if st.button(label, use_container_width=True):
            st.switch_page(f"{page}")
