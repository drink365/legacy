import streamlit as st
from modules.estate_tax_calculator import TaxConstants, EstateTaxCalculator
from modules.estate_tax_ui import render_estate_tax_ui

st.set_page_config(
    page_title="AI秒算遺產稅",
    page_icon="🧮",
    layout="wide"
)

st.markdown("# 🧮 AI秒算遺產稅")
st.markdown("""
這是一個提供給高資產人士的簡易稅務試算工具，
幫助您快速了解是否需要進一步預留稅源或規劃保險。

👉 試算結果僅供參考，實際稅務請洽專業顧問。
---
""")

constants = TaxConstants()
calculator = EstateTaxCalculator(constants)
render_estate_tax_ui(calculator)
