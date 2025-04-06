from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import mm
import streamlit as st


def generate_exploration_pdf():
    buffer = BytesIO()
    logo_path = "logo.png"
    font_path = "NotoSansTC-Regular.ttf"

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

    if "legacy_style_result" in st.session_state:
        story.append(Paragraph("您的傳承風格：", styleH))
        story.append(Paragraph(
            st.session_state.legacy_style_result.replace("❤️", "").replace("💼", "").replace("🧭", ""),
            styleN
        ))
        story.append(Spacer(1, 12))

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
    story.append(Spacer(1, 12))
    story.append(Spacer(1, 6))
    story.append(Paragraph("永傳家族辦公室｜https://gracefo.com/", styleC))
    story.append(Paragraph("聯絡我們：123@gracefo.com", styleC))

    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    doc.build(story)
    buffer.seek(0)
    return buffer


def generate_asset_map_pdf(asset_data, total_value):
    buffer = BytesIO()
    font_path = "NotoSansTC-Regular.ttf"

    pdfmetrics.registerFont(TTFont("NotoSansTC", font_path))
    style_title = ParagraphStyle(name='Title', fontName='NotoSansTC', fontSize=18, alignment=TA_CENTER, spaceAfter=12)
    style_header = ParagraphStyle(name='Header', fontName='NotoSansTC', fontSize=14, spaceAfter=10)
    style_text = ParagraphStyle(name='Normal', fontName='NotoSansTC', fontSize=12)
    style_center = ParagraphStyle(name='Center', fontName='NotoSansTC', fontSize=10, alignment=TA_CENTER)

    story = []

    logo = Image("logo.png", width=80 * mm, height=20 * mm)
    logo.hAlign = 'CENTER'
    story.append(logo)
    story.append(Spacer(1, 12))
    story.append(Paragraph("傳承風險圖與建議摘要", style_title))
    story.append(Spacer(1, 12))

    for category, amount in asset_data.items():
        story.append(Paragraph(f"{category}：{amount:,.0f} 萬元", style_text))
    story.append(Spacer(1, 12))

    story.append(Paragraph(f"總資產：{total_value:,.0f} 萬元", style_header))
    story.append(Spacer(1, 24))

    story.append(Paragraph("永傳家族辦公室｜https://gracefo.com/", style_center))
    story.append(Paragraph("聯絡信箱：123@gracefo.com", style_center))

    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    doc.build(story)
    buffer.seek(0)
    return buffer
