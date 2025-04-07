import streamlit as st
from io import BytesIO
from datetime import date
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import mm
import os
from modules.cta_section import render_cta

st.set_page_config(
    page_title="樂活退休試算｜《影響力》傳承策略平台",
    page_icon="💰",
    layout="centered"
)

pdfmetrics.registerFont(TTFont('NotoSansTC', 'NotoSansTC-Regular.ttf'))

st.markdown("""
<div style='text-align: center;'>
    <h1>💰 樂活退休試算</h1>
    <p style='font-size: 18px; margin-top: -10px;'>由《影響力》傳承策略平台陪您看見未來，預作準備</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<br>
《影響力》陪您一起看清未來 30 年的生活輪廓：

✅ 預估退休期間的年支出（生活、醫療、長照）  
✅ 了解目前資產是否足以支撐退休生活  
✅ 預測可能出現的財務缺口，提早準備、安心退休

💬 「退休不是結束，而是另一段人生的開始。」  
傳承策略平台提醒您，提早預備的每一步，都是為自己與家人創造安心與選擇的自由。

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

# 試算按鈕
if st.button("📊 開始試算") or "calc_done" in st.session_state:
    st.session_state.calc_done = True
    total_years = life_expectancy - retire_age
    total_expense = total_years * (annual_expense + annual_medical + annual_longterm)
    total_assets_future = current_assets * ((1 + expected_return / 100) ** (retire_age - age))
    shortage = total_expense - total_assets_future
    buffer = None

    st.markdown("---")
    st.markdown("### 📈 試算結果")
    st.markdown(f"預估退休年數：**{total_years} 年**")
    st.markdown(f"退休總支出：約 **{total_expense:,.0f} 萬元**")
    st.markdown(f"退休資產成長：約 **{total_assets_future:,.0f} 萬元**")
    st.markdown(f"退休資金缺口：約 **{shortage:,.0f} 萬元**")

    if shortage > 0:
        suggested_insurance = round(shortage * 1.05)
        st.warning(f"⚠️ 建議預留補強金額（含 5% 安全係數）：約 **{suggested_insurance:,.0f} 萬元**")
        st.markdown("""
💬 <i>傳承策略平台提醒：</i> 不用擔心，這正是開始規劃的好時機！  
- 您可以評估是否透過保險、年金或不動產現金流做補強  
- 建議進一步釐清資產配置與支出彈性，打造安心的退休現金流
""", unsafe_allow_html=True)
    else:
        st.success("✅ 恭喜！目前規劃的資產足以支應您的退休需求。")
        st.markdown("""
💬 <i>傳承策略平台建議：</i> 即使足夠，也建議定期檢視，調整投資策略與風險控管，讓退休後生活更有彈性與餘裕。
""", unsafe_allow_html=True)

    # PDF 下載區
    st.markdown("---")
    st.markdown("### 📥 下載試算摘要（PDF）")

    def generate_pdf():
        pdf_buffer = BytesIO()
        logo_path = "logo.png"
        font_path = "NotoSansTC-Regular.ttf"

        pdfmetrics.registerFont(TTFont('NotoSansTC', font_path))
        styleN = ParagraphStyle(name='Normal', fontName='NotoSansTC', fontSize=12)
        styleH = ParagraphStyle(name='Heading2', fontName='NotoSansTC', fontSize=14, spaceAfter=10)
        styleC = ParagraphStyle(name='Center', fontName='NotoSansTC', fontSize=10, alignment=TA_CENTER)

        story = []
        if os.path.exists(logo_path):
            logo = Image(logo_path, width=80 * mm, height=20 * mm)
            logo.hAlign = 'CENTER'
            story.append(logo)
        story.append(Spacer(1, 12))
        story.append(Paragraph("樂活退休試算摘要", styleH))
        story.append(Spacer(1, 6))
        story.append(Paragraph(f"試算日期：{date.today()}", styleN))
        story.append(Paragraph(f"退休年齡：{retire_age} 歲", styleN))
        story.append(Paragraph(f"預估壽命：{life_expectancy} 歲", styleN))
        story.append(Paragraph(f"預估退休年數：{total_years} 年", styleN))
        story.append(Spacer(1, 6))
        story.append(Paragraph(f"退休總支出：約 {total_expense:,.0f} 萬元", styleN))
        story.append(Paragraph(f"退休資產成長：約 {total_assets_future:,.0f} 萬元", styleN))
        story.append(Paragraph(f"退休資金缺口：約 {shortage:,.0f} 萬元", styleN))
        if shortage > 0:
            story.append(Paragraph(f"建議補強金額（含 5% 安全係數）：約 {suggested_insurance:,.0f} 萬元", styleN))
        story.append(Spacer(1, 12))
        story.append(Paragraph("《影響力》傳承策略平台｜永傳家族辦公室 https://gracefo.com", styleC))
        story.append(Paragraph("聯絡信箱：123@gracefo.com", styleC))

        doc = SimpleDocTemplate(pdf_buffer, pagesize=A4)
        doc.build(story)
        pdf_buffer.seek(0)
        return pdf_buffer

    pdf = generate_pdf()
    st.download_button(
        label="📄 下載我的退休試算報告（PDF）",
        data=pdf,
        file_name="retirement_summary.pdf",
        mime="application/pdf"
    )

    render_cta()

# 頁尾資訊
st.markdown("---")
st.markdown("""
<div style='text-align: center; font-size: 14px; color: gray;'>
《影響力》傳承策略平台｜永傳家族辦公室 <a href=\"https://gracefo.com\" target=\"_blank\">https://gracefo.com</a><br>
聯絡信箱：<a href=\"mailto:123@gracefo.com\">123@gracefo.com</a>
</div>
""", unsafe_allow_html=True)
