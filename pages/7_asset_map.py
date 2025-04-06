import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.patches as mpatches
from datetime import date

# 設定中文字型
font_path = "NotoSansTC-Regular.ttf"
prop = fm.FontProperties(fname=font_path)

# 頁面設定
st.set_page_config(
    page_title="傳承風險圖與建議摘要",
    page_icon="📊",
    layout="wide"
)

# Logo 與標題
col1, col2 = st.columns([1, 6])
with col1:
    st.image("logo.png", width=100)
with col2:
    st.markdown("### 傳承風險圖與建議摘要")
    st.markdown(f"<div style='color: gray; font-size: 14px;'>更新日期：{date.today()}</div>", unsafe_allow_html=True)

st.markdown("---")

# 輸入六大資產類型金額
st.markdown("#### 📋 請輸入您的資產金額（單位：萬元）")
company = st.number_input("公司股權", min_value=0, value=5000)
real_estate = st.number_input("不動產", min_value=0, value=3000)
financial = st.number_input("金融資產（存款、股票、基金等）", min_value=0, value=2000)
insurance = st.number_input("保單", min_value=0, value=1500)
offshore = st.number_input("海外資產", min_value=0, value=1000)
other = st.number_input("其他資產", min_value=0, value=500)

# 計算總資產與百分比
assets = {
    "公司股權": company,
    "不動產": real_estate,
    "金融資產": financial,
    "保單": insurance,
    "海外資產": offshore,
    "其他資產": other
}
total = sum(assets.values())
percentages = {k: (v / total * 100 if total > 0 else 0) for k, v in assets.items()}

# 繪製圓餅圖
fig, ax = plt.subplots(figsize=(6, 6))
ax.pie(assets.values(), labels=assets.keys(), autopct="%1.1f%%", textprops={"fontproperties": prop})
ax.set_title("資產分布圖", fontproperties=prop)
st.pyplot(fig)

# 顯示分析摘要
st.markdown("#### 🧭 風險分析與建議摘要")
st.markdown("""
- **公司股權**：占比較高時，應特別留意未來接班人選與股權轉移機制，避免糾紛與稅負集中。
- **不動產**：建議盤點持有型態（自用、出租、持分等），並提早規劃贈與或信託，以分散稅務風險。
- **金融資產**：流動性高，適合作為應急與長照準備金。建議進一步思考用途比例與配置策略。
- **保單**：屬於具稅務效率的傳承工具。若佔比偏低，建議可用於補足現金缺口或設計特定受益人分配。
- **海外資產**：需留意跨境申報與遺產稅規定，可考慮海外信託或保險作為工具。
- **其他資產**：例如收藏、虛擬貨幣、債權等，應逐一盤點並建立文件紀錄，便於傳承與管理。

📌 **提醒**：傳承規劃不只是資產的分配，更關乎價值的延續與家族的穩定。建議搭配完整傳承架構進行。
""")

# CTA 區塊
st.markdown("---")
st.markdown("### 📬 想針對資產進一步設計您的專屬傳承策略？")
if st.button("📩 點我預約 1 對 1 諮詢"):
    st.markdown(
        "<meta http-equiv='refresh' content='0; url=mailto:123@gracefo.com?subject=資產風險分析諮詢&body=您好，我剛剛使用了資產風險分析工具，想進一步了解如何規劃傳承策略。'>",
        unsafe_allow_html=True
    )

# 頁尾資訊
st.markdown("---")
st.markdown("""
<div style='text-align: center; font-size: 14px; color: gray;'>
永傳家族辦公室｜<a href="https://gracefo.com" target="_blank">https://gracefo.com</a>  
聯絡信箱：<a href="mailto:123@gracefo.com">123@gracefo.com</a>
</div>
""", unsafe_allow_html=True)
