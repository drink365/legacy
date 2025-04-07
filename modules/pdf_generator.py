from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import mm
import streamlit as st
import re

# 字型與樣式設定
font_path = "NotoSansTC-Regular.ttf"
pdfmetrics.registerFont(TTFont('NotoSansTC', font_path))

styleN = ParagraphStyle(name='Normal', fontName='NotoSansTC', fontSize=12, spaceAfter=4)
styleH = ParagraphStyle(name='Heading2', fontName='NotoSansTC', fontSize=14, spaceAfter=10)
styleC = ParagraphStyle(name='Center', fontName='NotoSansTC', fontSize=10, alignment=TA_CENTER)


# ✅ 表情符號清除器（僅 PDF 用）
def remove_emojis(text):
    return re.sub(r"[^\u0000-\uFFFF]", "", text)


# ✅ 產生傳承教練模組 PDF
def generate_legacy_pdf():
    buffer = BytesIO()
    logo_path = "logo.png"

    story = []
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)

    # Logo & 標語
    logo = Image(logo_path, width=80 * mm, height=20 * mm)
    logo.hAlign = 'CENTER'
    story.append(logo)
    story.append(Spacer(1, 6))
    story.append(Paragraph("傳承您的影響力", styleC))
    story.append(Paragraph("每一位家族的掌舵者，都是家族傳承的種子。", styleC))
    story.append(Paragraph("我們陪您，讓這份影響力持續茁壯。", styleC))
    story.append(Spacer(1, 24))
    story.append(Paragraph("永傳 AI 傳承教練探索紀錄", styleH))

    # 傳承風格
    if "legacy_style_result" in st.session_state:
        text = remove_emojis(st.session_state.legacy_style_result)
        story.append(Spacer(1, 12))
        story.append(Paragraph("您的傳承風格：", styleH))
        story.append(Paragraph(text, styleN))

    # 模組二
    if "key_issues" in st.session_state:
        story.append(Spacer(1, 12))
        story.append(Paragraph("模組二：您最在意的重點", styleH))
        for issue in st.session_state.key_issues:
            story.append(Paragraph(f"• {issue}", styleN))
        if st.session_state.get("reason"):
            story.append(Paragraph(f"原因：{st.session_state.reason}", styleN))

    # 模組三
    if "directions" in st.session_state:
        story.append(Spacer(1, 12))
        story.append(Paragraph("模組三：您期望的未來方向", styleH))
        for d in st.session_state.directions:
            story.append(Paragraph(f"• {d}", styleN))
        if st.session_state.get("custom_direction"):
            story.append(Paragraph(f"補充：{st.session_state.custom_direction}", styleN))

    # 思考引導
    story.append(Spacer(1, 16))
    story.append(Paragraph("對談前的思考引導", styleH))
    story.append(Paragraph("1. 如果我今天退休，最擔心的事情是什麼？", styleN))
    story.append(Paragraph("2. 我希望未來家人如何記得我？", styleN))
    story.append(Paragraph("3. 有沒有什麼，是我現在就可以決定、啟動的？", styleN))

    # 結尾
    story.append(Spacer(1, 24))
    story.append(Paragraph("永傳家族辦公室｜https://gracefo.com/", styleC))
    story.append(Paragraph("聯絡我們：123@gracefo.com", styleC))

    doc.build(story)
    buffer.seek(0)
    return buffer


# ✅ 產生資產風險圖 PDF
def generate_asset_map_pdf(asset_data, total, risk_suggestions, summary_text, remove_emojis=False):
    buffer = BytesIO()
    logo_path = "logo.png"

    story = []
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)

    # Logo & 標題
    logo = Image(logo_path, width=80 * mm, height=20 * mm)
    logo.hAlign = 'CENTER'
    story.append(logo)
    story.append(Spacer(1, 10))
    story.append(Paragraph("傳承風險圖與建議摘要", styleH))
    story.append(Spacer(1, 10))
    story.append(Paragraph(f"總資產：約 {total:,.0f} 萬元", styleN))

    # 資產細項
    story.append(Spacer(1, 10))
    for k, v in asset_data.items():
        story.append(Paragraph(f"• {k}：{v:,.0f} 萬元", styleN))

    # 風險提醒
    story.append(Spacer(1, 12))
    story.append(Paragraph("風險提示與建議", styleH))
    for line in risk_suggestions:
        cleaned = remove_emojis(line) if remove_emojis else line
        story.append(Paragraph(f"• {cleaned}", styleN))

    # 總體摘要
    story.append(Spacer(1, 12))
    story.append(Paragraph("總體風險評估", styleH))
    story.append(Paragraph(summary_text, styleN))

    # 行動清單
    story.append(Spacer(1, 12))
    story.append(Paragraph("建議行動清單", styleH))
    for a in get_action_suggestions():
        cleaned = remove_emojis(a) if remove_emojis else a
        story.append(Paragraph(f"• {cleaned}", styleN))

    # 結尾資訊
    story.append(Spacer(1, 20))
    story.append(Paragraph("永傳家族辦公室｜https://gracefo.com/", styleC))
    story.append(Paragraph("聯絡我們：123@gracefo.com", styleC))

    doc.build(story)
    buffer.seek(0)
    return buffer


# ✅ 行動建議清單
def get_action_suggestions():
    return [
        "📌 重新檢視資產結構，確認是否已涵蓋流動性、稅源與保障需求。",
        "📌 檢查壽險與信託設計是否能對應潛在風險。",
        "📌 評估家族內部共識與接班安排是否已明確。",
        "📌 若擁有海外資產，應尋求專業稅務建議。",
        "📌 安排一次家族會議，開啟世代間傳承的對話。"
    ]
