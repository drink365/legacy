from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import mm
import re
import os
import streamlit as st

font_path = "NotoSansTC-Regular.ttf"
logo_path = "logo.png"

def strip_emojis(text):
    emoji_pattern = re.compile("[\U00010000-\U0010ffff]", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

def generate_asset_map_pdf(asset_data, total, risk_suggestions, summary_text, remove_emojis=False):
    buffer = BytesIO()
    pdfmetrics.registerFont(TTFont('NotoSansTC', font_path))
    styleN = ParagraphStyle(name='Normal', fontName='NotoSansTC', fontSize=12)
    styleH = ParagraphStyle(name='Heading2', fontName='NotoSansTC', fontSize=14, spaceAfter=10)
    styleC = ParagraphStyle(name='Center', fontName='NotoSansTC', fontSize=10, alignment=TA_CENTER)

    story = []
    if os.path.exists(logo_path):
        logo = Image(logo_path, width=80 * mm, height=20 * mm)
        logo.hAlign = 'CENTER'
        story.append(logo)
        story.append(Spacer(1, 6))

    story.append(Paragraph("傳承您的影響力", styleC))
    story.append(Paragraph("每一位家族的掌舵者，都是家族傳承的種子。", styleC))
    story.append(Paragraph("我們陪您，讓這份影響力持續茁壯。", styleC))
    story.append(Spacer(1, 24))

    story.append(Paragraph("永傳 AI 傳承教練 - 傳承風險圖與建議摘要", styleH))
    story.append(Spacer(1, 12))

    story.append(Paragraph("【資產總覽】", styleH))
    for key, value in asset_data.items():
        text = f"{key}：{value:,.0f} 萬元"
        if remove_emojis:
            text = strip_emojis(text)
        story.append(Paragraph(text, styleN))
    story.append(Paragraph(f"總資產：約 {total:,.0f} 萬元", styleN))
    story.append(Spacer(1, 12))

    story.append(Paragraph("【傳承風險提示】", styleH))
    if risk_suggestions:
        for r in risk_suggestions:
            text = strip_emojis(r) if remove_emojis else r
            story.append(Paragraph(f"- {text}", styleN))
    else:
        story.append(Paragraph("目前未偵測到顯著風險。", styleN))
    story.append(Spacer(1, 12))

    story.append(Paragraph("【總體評估】", styleH))
    summary = strip_emojis(summary_text) if remove_emojis else summary_text
    story.append(Paragraph(summary, styleN))
    story.append(Spacer(1, 12))

    story.append(Paragraph("【建議行動清單】", styleH))
    actions = [
        "若股權占比高：請洽顧問討論股權信託與公司治理設計。",
        "若不動產占比高：可考慮不動產信託、換屋或出售部分資產。",
        "若未配置保單：可初步評估保額、稅源與家族成員的保障需求。",
        "若有海外資產：請確保已做 FBAR/CRS 合規申報，並評估海外信託規劃。",
        "若有其他資產：請逐項盤點其價值與流動性，規劃適當移轉方式。"
    ]
    for action in actions:
        story.append(Paragraph(action, styleN))

    story.append(Spacer(1, 20))
    story.append(Paragraph("永傳家族辦公室｜https://gracefo.com/", styleC))
    story.append(Paragraph("聯絡我們：123@gracefo.com", styleC))

    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    doc.build(story)
    buffer.seek(0)
    return buffer

def generate_legacy_pdf(remove_emojis=False):
    buffer = BytesIO()
    pdfmetrics.registerFont(TTFont('NotoSansTC', font_path))
    styleN = ParagraphStyle(name='Normal', fontName='NotoSansTC', fontSize=12)
    styleH = ParagraphStyle(name='Heading2', fontName='NotoSansTC', fontSize=14, spaceAfter=10)
    styleC = ParagraphStyle(name='Center', fontName='NotoSansTC', fontSize=10, alignment=TA_CENTER)

    story = []
    if os.path.exists(logo_path):
        logo = Image(logo_path, width=80 * mm, height=20 * mm)
        logo.hAlign = 'CENTER'
        story.append(logo)
        story.append(Spacer(1, 6))

    story.append(Paragraph("傳承您的影響力", styleC))
    story.append(Paragraph("每一位家族的掌舵者，都是家族傳承的種子。", styleC))
    story.append(Paragraph("我們陪您，讓這份影響力持續茁壯。", styleC))
    story.append(Spacer(1, 24))

    story.append(Paragraph("永傳 AI 傳承教練探索紀錄", styleH))
    story.append(Spacer(1, 12))

    if "legacy_style_result" in st.session_state:
        story.append(Paragraph("【您的傳承風格】", styleH))
        story.append(Paragraph(strip_emojis(st.session_state.legacy_style_result) if remove_emojis else st.session_state.legacy_style_result, styleN))
        story.append(Spacer(1, 12))

    if "key_issues" in st.session_state:
        story.append(Paragraph("【模組二：您最在意的重點】", styleH))
        for issue in st.session_state.key_issues:
            story.append(Paragraph(f"• {issue}", styleN))
        if st.session_state.get("reason"):
            story.append(Paragraph(f"原因：{st.session_state.reason}", styleN))
        story.append(Spacer(1, 12))

    if "directions" in st.session_state:
        story.append(Paragraph("【模組三：您期望的未來方向】", styleH))
        for d in st.session_state.directions:
            story.append(Paragraph(f"• {d}", styleN))
        if st.session_state.get("custom_direction"):
            story.append(Paragraph(f"補充：{st.session_state.custom_direction}", styleN))
        story.append(Spacer(1, 12))

    story.append(Paragraph("【對談前的思考引導】", styleH))
    for q in [
        "1. 如果我今天退休，最擔心的事情是什麼？",
        "2. 我希望未來家人如何記得我？",
        "3. 有沒有什麼，是我現在就可以決定、啟動的？"
    ]:
        story.append(Paragraph(q, styleN))

    story.append(Spacer(1, 20))
    story.append(Paragraph("永傳家族辦公室｜https://gracefo.com/", styleC))
    story.append(Paragraph("聯絡我們：123@gracefo.com", styleC))

    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    doc.build(story)
    buffer.seek(0)
    return buffer
