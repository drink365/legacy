import streamlit as st
import base64
import os
from modules.strategy_module import get_strategy_suggestions
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import mm

# 頁面設定
st.set_page_config(
    page_title="永傳 AI 傳承教練",
    page_icon="🌿",
    layout="centered"
)

# LOGO base64 顯示

def load_logo_base64(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# PDF 報告產出

def generate_pdf():
    pdf_path = "/mnt/data/永傳AI探索報告.pdf"
    logo_path = "logo.png"
    font_path = "NotoSansTC-Regular.ttf"  # 已確認存在的字型檔名

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

    if "key_issues" in st.session_state:
        story.append(Paragraph("模組二：您最在意的重點", styleH))
        for issue in st.session_state.key_issues:
            story.append(Paragraph(f"• {issue}", styleN))
        if st.session_state.get("reason"):
            story.append(Paragraph(f"原因：{st.session_state.reason}", styleN))
        story.append(Spacer(1, 12))

    if "directions" in st.session_state:
        story.append(Paragraph("模組三：您期望的未來方向", styleH))
        for d in st.session_state.directions:
            story.append(Paragraph(f"• {d}", styleN))
        if st.session_state.get("custom_direction"):
            story.append(Paragraph(f"補充：{st.session_state.custom_direction}", styleN))
        story.append(Spacer(1, 12))

    story.append(Paragraph("對談前的思考引導", styleH))
    story.append(Paragraph("這三個問題，邀請您在心中停留片刻：", styleN))
    story.append(Paragraph("1. 如果我今天退休，最擔心的事情是什麼？", styleN))
    story.append(Paragraph("2. 我希望未來家人如何記得我？", styleN))
    story.append(Paragraph("3. 有沒有什麼，是我現在就可以決定、啟動的？", styleN))
    story.append(Spacer(1, 20))

    story.append(Paragraph("下一步，我們可以一起完成", styleH))
    story.append(Paragraph("如果這份紀錄讓您浮現了願景，我們誠摯邀請您預約對談，一起為未來鋪路。", styleN))
    story.append(Spacer(1, 6))
    story.append(Paragraph("永傳家族辦公室｜https://gracefo.com/", styleC))
    story.append(Paragraph("聯絡我們：123@gracefo.com", styleC))

    doc = SimpleDocTemplate(pdf_path, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    doc.build(story)
    return pdf_path
