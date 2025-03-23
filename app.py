import streamlit as st
import base64
import os
from modules.strategy_module import get_strategy_suggestions
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import mm

# --- 基本設定 ---
st.set_page_config(
    page_title="永傳 AI 傳承教練",
    page_icon="🌿",
    layout="centered"
)

# --- LOGO 顯示 ---
def load_logo_base64(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def generate_pdf():
    pdf_path = "/mnt/data/永傳AI探索報告.pdf"
    logo_path = "logo.png"
    font_path = "NotoSansTC-VariableFont_wght.ttf"  # 確保此檔已上傳

    pdfmetrics.registerFont(TTFont('NotoSansTC', font_path))

    styleN = ParagraphStyle(name='Normal', fontName='NotoSansTC', fontSize=12)
    styleH = ParagraphStyle(name='Heading2', fontName='NotoSansTC', fontSize=14, spaceAfter=10)
    styleC = ParagraphStyle(name='Center', fontName='NotoSansTC', fontSize=10, alignment=TA_CENTER)

    story = []

    logo = Image(logo_path, width=80 * mm, height=20 * mm)
    logo.hAlign = 'CENTER'
    story.append(logo)
    story.append(Spacer(1, 6))
    story.append(Paragraph("傳承您的影響力", styleC))
    story.append(Paragraph("每一位家族的掌舵者，都是家族傳承的種子。", styleC))
    story.append(Paragraph("我們陪您，讓這份影響力持續茁壯。", styleC))
    story.append(Spacer(1, 24))

    story.append(Paragraph("永傳 AI 傳承教練探索紀錄", styleH))
    story.append(Spacer(1, 20))

    story.append(Paragraph("模組一：您最近在思考的事情", styleH))
    story.append(Paragraph("• 公司的未來要怎麼安排？", styleN))
    story.append(Paragraph("• 家族成員之間的關係", styleN))
    story.append(Paragraph("• 希望未來能和子女有良好溝通", styleN))
    story.append(Spacer(1, 12))

    story.append(Paragraph("模組二：您最在意的重點", styleH))
    story.append(Paragraph("• 孩子是否適合承接家業", styleN))
    story.append(Paragraph("原因：我擔心交給他，他會壓力太大，反而破壞了我們的親子關係。", styleN))
    story.append(Spacer(1, 12))

    story.append(Paragraph("模組三：您期望的未來方向", styleH))
    story.append(Paragraph("• 希望有人能逐步接手", styleN))
    story.append(Paragraph("• 希望我退休後，也能保有影響力與參與感", styleN))
    story.append(Spacer(1, 12))

    story.append(Paragraph("模組四：建議的行動策略", styleH))
    story.append(Paragraph("• 逐步交接機制", styleN))
    story.append(Paragraph("設計一個循序漸進的參與計畫，從共同討論、旁聽會議到實際決策參與。", styleN))
    story.append(Spacer(1, 6))
    story.append(Paragraph("• 退休後參與角色", styleN))
    story.append(Paragraph("規劃一個具象的非營運角色，如品牌大使或顧問，持續保有參與感。", styleN))
    story.append(Spacer(1, 12))

    story.append(Paragraph("對談前的思考引導", styleH))
    story.append(Paragraph("這三個問題，邀請您在心中停留片刻，也許未來的答案，就藏在這裡：", styleN))
    story.append(Paragraph("1. 如果我今天退休，最擔心的事情是什麼？", styleN))
    story.append(Paragraph("2. 我希望未來家人如何記得我？", styleN))
    story.append(Paragraph("3. 有沒有什麼，是我現在就可以決定、啟動的？", styleN))
    story.append(Spacer(1, 20))

    story.append(Paragraph("下一步，我們可以一起完成", styleH))
    story.append(Paragraph(
        "如果這份紀錄讓您心中浮現了某些畫面或願景，我們誠摯邀請您走得更近一步。"
        "永傳家族辦公室專注協助高資產家庭進行退休與傳承規劃，將未來的不確定轉化為可安排的節奏，"
        "讓您的影響力持續為家族鋪路。",
        styleN
    ))
    story.append(Spacer(1, 6))
    story.append(Paragraph("歡迎與我們預約 30 分鐘深度對談", styleN))
    story.append(Spacer(1, 10))
    story.append(Paragraph("永傳家族辦公室｜https://gracefo.com/", styleC))
    story.append(Paragraph("聯絡我們：123@gracefo.com", styleC))

    doc = SimpleDocTemplate(pdf_path, pagesize=A4,
                            rightMargin=30, leftMargin=30,
                            topMargin=30, bottomMargin=30)
    doc.build(story)
    return pdf_path

# --- LOGO 顯示 ---
logo_base64 = load_logo_base64("logo.png")
st.markdown(f"""
<div style='text-align: center;'>
    <img src='data:image/png;base64,{logo_base64}' width='200'><br>
    <div style='font-size: 18px; font-weight: bold; margin-top: 0.5em;'>傳承您的影響力</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<br>
<div style='text-align: center; font-size: 20px; font-weight: bold;'>
🌱 每一位家族的掌舵者，都是家族傳承的種子。<br>
我們陪您，讓這份影響力持續茁壯。
</div>
<br>
""", unsafe_allow_html=True)

# --- 下載報告按鈕 ---
if st.button("📄 下載探索報告 PDF"):
    pdf = generate_pdf()
    with open(pdf, "rb") as f:
        st.download_button(
            label="下載報告",
            data=f,
            file_name="永傳AI探索報告.pdf",
            mime="application/pdf"
        )
