import streamlit as st
from modules.tax_constants import TaxConstants
from modules.tax_calculator import EstateTaxCalculator
from modules.estate_tax_ui import render_estate_tax_ui

st.set_page_config(
    page_title="AI秒算遺產稅｜永傳家辦小工具",
    page_icon="🧮",
    layout="wide"
)

st.markdown("# 🧮 AI秒算遺產稅")
st.markdown("""
傳承教練在這裡，陪您快速了解資產與稅務之間的關聯。  
這個小工具特別為高資產家庭設計，幫助您：

✅ 初步估算潛在的遺產稅負擔  
✅ 看見可能出現的現金缺口  
✅ 提早思考如何透過保險或信託安排，預防風險

> 📌 試算結果僅供參考，實際稅務請與顧問討論。
---
""")

constants = TaxConstants()
calculator = EstateTaxCalculator(constants)
render_estate_tax_ui(calculator)

# 結語引導
st.markdown("---")
st.markdown("""
### 📬 下一步建議
傳承教練建議您可：
- 與顧問討論保單、信託、贈與等安排，建立稅源預備架構
- 評估現金流與繳稅時點的配合度，避免資產被迫處分
- 若您有海外資產，也可進一步進行跨境稅務整合規劃

💡 若需要，我們也可協助一對一診斷。
👉 <a href="mailto:123@gracefo.com?subject=遺產稅試算後想深入諮詢&body=您好，我剛完成永傳AI秒算遺產稅的試算，想了解我的稅源預備與保險配置。">點我寄信預約對談</a>
""", unsafe_allow_html=True)

# 頁尾資訊
st.markdown("---")
st.markdown("""
<div style='text-align: center; font-size: 14px; color: gray;'>
永傳家族辦公室｜<a href="https://gracefo.com" target="_blank">https://gracefo.com</a><br>
聯絡信箱：<a href="mailto:123@gracefo.com">123@gracefo.com</a>
</div>
""", unsafe_allow_html=True)
