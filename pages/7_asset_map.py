import streamlit as st
from PIL import Image

# 頁面設定
st.set_page_config(
    page_title="傳承風險圖與建議摘要",
    page_icon="📊",
    layout="wide"
)

# 載入 logo
try:
    logo = Image.open("logo.png")
    st.image(logo, width=220)
except:
    st.warning("⚠️ 找不到 logo.png，請確認檔案存在")

# 標題區
st.markdown("""
# 📊 傳承風險圖與建議摘要
請輸入您的主要資產類型，我們將自動對應可能風險並給出建議摘要。
""")

# 使用者輸入六大類資產估值
st.markdown("## 📥 資產類型輸入（單位：萬元）")
col1, col2 = st.columns(2)

with col1:
    equity = st.number_input("公司股權", min_value=0, step=100)
    real_estate = st.number_input("不動產", min_value=0, step=100)
    financial = st.number_input("金融資產（存款、股票、基金等）", min_value=0, step=100)
with col2:
    insurance = st.number_input("保單", min_value=0, step=100)
    overseas = st.number_input("海外資產", min_value=0, step=100)
    others = st.number_input("其他資產", min_value=0, step=100)

total = equity + real_estate + financial + insurance + overseas + others

# 顯示總資產
st.markdown(f"### 💰 總資產估值：約 **{total:,} 萬元**")

# 風險圖＋建議區
st.markdown("---")
st.markdown("## 🧭 傳承風險圖")

risk_items = []

if equity > 0:
    risk_items.append("📌 公司股權：建議盤點股東結構，預防繼承後經營權爭議")
if real_estate > 0:
    risk_items.append("📌 不動產：注意分割困難與稅務問題，可規劃信託或代持")
if financial > 0:
    risk_items.append("📌 金融資產：可提前安排贈與節稅，搭配保單建立現金流")
if insurance > 0:
    risk_items.append("📌 保單：檢查受益人與信託安排，避免分配糾紛")
if overseas > 0:
    risk_items.append("📌 海外資產：注意當地稅制與繼承法律，建議先行申報")
if others > 0:
    risk_items.append("📌 其他資產：盤點所有名下財產，建立完整資產清單")

# 顯示風險提醒
if risk_items:
    for item in risk_items:
        st.markdown(f"- {item}")
else:
    st.info("請輸入資產估值以生成風險圖")

# 備註與提醒
st.markdown("---")
st.markdown("""
📌 本工具為初步盤點，實際傳承建議仍須搭配顧問輔導。  
💬 若您希望進一步診斷與設計專屬架構，歡迎預約諮詢。
""")

# CTA
if st.button("📩 預約傳承規劃顧問"):
    st.markdown(
        "<meta http-equiv='refresh' content='0; url=mailto:123@gracefo.com?subject=預約傳承風險診斷&body=您好，我使用了傳承風險圖工具，想進一步了解家族資產配置與傳承建議。'>",
        unsafe_allow_html=True
    )
