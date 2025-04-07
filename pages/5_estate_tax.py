import streamlit as st
from modules.tax_constants import TaxConstants
from modules.tax_calculator import EstateTaxCalculator
from modules.estate_tax_ui import render_estate_tax_ui
from modules.cta_section import render_cta

# 頁面設定
st.set_page_config(
    page_title="AI秒算遺產稅｜《影響力》傳承策略平台",
    page_icon="🧮",
    layout="wide"
)

# 標題與說明
st.markdown("""
<div style='text-align: center; margin-top: 1em;'>
    <h1 style='font-size: 36px;'>🧮 AI秒算遺產稅</h1>
    <p style='font-size: 20px; color: #555;'>快速預估潛在稅負，為資產傳承提前預留稅源</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
這是一個為高資產家庭設計的簡易稅務試算工具，協助您掌握未來遺產稅額與現金需求，進一步思考保險與信託等安排。  
<br>
👉 試算結果僅供初步參考，實際稅務依各國法令與申報內容而定，建議與專業顧問討論。
""", unsafe_allow_html=True)

st.markdown("---")

# 啟用試算模組
constants = TaxConstants()
calculator = EstateTaxCalculator(constants)
render_estate_tax_ui(calculator)

# 行動導引 CTA
render_cta()

# 頁尾資訊
st.markdown("---")
st.markdown("""
<div style='text-align: center; font-size: 14px; color: gray;'>
《影響力》傳承策略平台｜永傳家族辦公室  
<a href="https://gracefo.com" target="_blank">https://gracefo.com</a><br>
聯絡信箱：<a href="mailto:123@gracefo.com">123@gracefo.com</a>
</div>
""", unsafe_allow_html=True)
