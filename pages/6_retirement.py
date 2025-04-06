import streamlit as st
from io import BytesIO
from datetime import date
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
import os

st.set_page_config(
    page_title="樂活退休試算｜永傳家族傳承教練",
    page_icon="💰",
    layout="centered"
)

# 註冊中文字體
pdfmetrics.registerFont(TTFont('NotoSansTC', 'NotoSansTC-Regular.ttf'))

st.markdown("""
<div style='text-align: center;'>
    <h1>💰 樂活退休試算</h1>
    <p style='font-size: 18px; margin-top: -10px;'>由永傳家族傳承教練陪您看見未來，預作準備</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
傳承教練陪您一起看清未來 30 年的生活輪廓：

✅ 預估退休期間的年支出（生活、醫療、長照）  
✅ 了解目前資產是否足以支撐退休生活  
✅ 預測可能出現的財務缺口，提早準備、安心退休

💬 「退休不是結束，而是另一段人生的開始。」  
傳承教練提醒您，提早預備的每一步，都是為自己與家人創造安心與選擇的自由。

> 📌 本工具為初步估算，實際規劃仍需搭配個人財務諮詢
---
""")

# 基本輸入
st.markdown("### 👤 基本資料")
age = st.number_input("目前年齡", min_value=30, max_value=80, value=55)
retire_age = st.number_input("預計退休年齡", min_value=50, max_value=80, value=60)
life_expectancy = st.number_input("預估壽命（活多久）", min_value=70, max_value=110, value=90)

# 資產與報酬
st.markdown("### 💼 現有資產與報酬")
current_assets = st.number_input("目前可用於退休的總資產（萬元）", min_value=0, value=1000)
expected_return = st.slider("預期年報酬率（％）", 0.0, 10.0, 2.0, 0.1)

# 年支出預估
st.markdown("### 💸 預估年支出")
annual_expense = st.number_input("每年退休生活支出（萬元）", min_value=0, value=100)
annual_medical = st.number_input("每年醫療支出預估（萬元）", min_value=0, value=10)
annual_longterm = st.number_input("每年長照支出預估（萬元）", min_value=0, value=5)

# 試算
if st.button("📊 開始試算"):
    total_years = life_expectancy - retire_age
    total_expense = total_years * (annual_expense + annual_medical + annual_longterm)
    total_assets_future = current_assets * ((1 + expected_return / 100) ** (retire_age - age))
    shortage = total_expense - total_assets_future

    st.markdown("---")
    st.markdown("### 📈 試算結果")
    st.markdown(f"預估退休後需準備的總金額：約 **{total_expense:,.0f} 萬元**")
    st.markdown(f"您的資產在退休時預估將成長為：約 **{total_assets_future:,.0f} 萬元**")

    if shortage > 0:
        st.error(f"⚠️ 預估可能短缺：約 {shortage:,.0f} 萬元。建議及早進行資產配置與保障規劃。")
        st.markdown("""
💬 <i>傳承教練提醒：</i> 不用擔心，這正是開始規劃的好時機！  
- 您可以評估是否透過保險、年金或不動產現金流做補強  
- 建議進一步釐清資產配置與支出彈性，打造安心的退休現金流
""", unsafe_allow_html=True)
        suggested_insurance = round(shortage * 1.05)
        st.markdown(f"📌 建議預留壽險／年金保障金額：約 **{suggested_insurance:,.0f} 萬元**")
    else:
        st.success("✅ 恭喜！目前規劃的資產足以支應您的退休需求。")
        st.markdown("""
💬 <i>傳承教練建議：</i> 即使足夠，也建議定期檢視，調整投資策略與風險控管，讓退休後生活更有彈性與餘裕。
""", unsafe_allow_html=True)

    # PDF 下載區
    st.markdown("---")
    st.markdown("### 📥 下載試算摘要（PDF）")
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    logo_path = "logo-橫式彩色.png"
    if os.path.exists(logo_path):
        logo = ImageReader(logo_path)
        c.drawImage(logo, 50, height - 100, width=180, preserveAspectRatio=True, mask='auto')
        logo_offset = 110
    else:
        logo_offset = 60

    c.setFont("NotoSansTC", 16)
    c.drawString(50, height - logo_offset - 20, "樂活退休試算摘要")
    c.setFont("NotoSansTC", 12)
    c.drawString(50, height - logo_offset - 40, f"試算日期：{date.today()}")
    c.drawString(50, height - logo_offset - 70, f"退休年齡：{retire_age} 歲")
    c.drawString(50, height - logo_offset - 90, f"預估壽命：{life_expectancy} 歲")
    c.drawString(50, height - logo_offset - 110, f"預估退休年數：{total_years} 年")
    c.drawString(50, height - logo_offset - 140, f"退休總支出：約 {total_expense:,.0f} 萬元")
    c.drawString(50, height - logo_offset - 160, f"退休資產成長：約 {total_assets_future:,.0f} 萬元")
    c.drawString(50, height - logo_offset - 180, f"退休資金缺口：約 {shortage:,.0f} 萬元")
    if shortage > 0:
        c.drawString(50, height - logo_offset - 200, f"建議補強金額：約 {round(shortage * 1.05):,.0f} 萬元")

    c.setFont("NotoSansTC", 10)
    c.drawString(50, 60, "永傳家族辦公室｜https://gracefo.com    聯絡信箱：123@gracefo.com")

    c.save()
    buffer.seek(0)

    st.download_button(
        label="下載我的退休試算報告（PDF）",
        data=buffer,
        file_name="retirement_summary.pdf",
        mime="application/pdf"
    )

    # 回首頁按鈕
    st.markdown("---")
    if st.button("🏡 回到首頁"):
        st.switch_page("app.py")

# 導引與聯絡
st.markdown("---")
st.markdown("### 📬 想更完整安排退休與傳承？")
st.markdown("""
💡 歡迎預約 1 對 1 對談，由傳承教練陪您規劃樂活退休的藍圖。  
👉 <a href=\"mailto:123@gracefo.com?subject=退休試算後想深入諮詢\" target=\"_blank\">點我寄信預約對談</a>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
<div style='text-align: center; font-size: 14px; color: gray;'>
永傳家族辦公室｜<a href=\"https://gracefo.com\" target=\"_blank\">https://gracefo.com</a><br>
聯絡信箱：<a href=\"mailto:123@gracefo.com\">123@gracefo.com</a>
</div>
""", unsafe_allow_html=True)
