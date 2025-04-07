from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import mm
import streamlit as st

# 載入字型
font_path = "NotoSansTC-Regular.ttf"
pdfmetrics.registerFont(TTFont('NotoSansTC', font_path))

# 預設樣式
styleN = ParagraphStyle(name='Normal', fontName='NotoSansTC', fontSize=12)
styleH = ParagraphStyle(name='Heading2', fontName='NotoSansTC', fontSize=14, spaceAfter=10)
styleC = ParagraphStyle(name='Center', fontName='NotoSansTC', fontSize=10, alignment=TA_CENTER)

def generate_asset_map_pdf(asset_data, total, risk_suggestions, summary_text):
    buffer = BytesIO()

    # 建立 PDF 內容
    story = []
    story.append(Spacer(1, 6))
    story.append(Paragraph("傳承風險圖與建議摘要", styleH))
    story.append(Spacer(1, 24))
    story.append(Paragraph(f"總資產：約 {total:,.0f} 萬元", styleN))
    story.append(Spacer(1, 12))

    story.append(Paragraph("資產類別分佈圖", styleH))
    story.append(Spacer(1, 12))

    for asset_type, value in asset_data.items():
        story.append(Paragraph(f"• {asset_type}: {value:,.0f} 萬元", styleN))

    story.append(Spacer(1, 12))

    # 風險提示
    story.append(Paragraph("📌 傳承風險提示與建議", styleH))
    for suggestion in risk_suggestions:
        story.append(Paragraph(f"- {suggestion}", styleN))

    # 總體風險評估
    story.append(Spacer(1, 12))
    story.append(Paragraph("📊 總體風險評估", styleH))
    story.append(Paragraph(summary_text, styleN))

    # 行動清單
    story.append(Spacer(1, 12))
    story.append(Paragraph("🛠️ 建議行動清單", styleH))
    for action in risk_suggestions:
        story.append(Paragraph(f"- {action}", styleN))

    # 生成 PDF
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    doc.build(story)
    buffer.seek(0)
    return buffer

def generate_legacy_pdf(legacy_style_result, key_issues, directions, summary_text):
    buffer = BytesIO()

    # 建立 PDF 內容
    story = []
    story.append(Spacer(1, 6))
    story.append(Paragraph("傳承風險圖與建議摘要", styleH))
    story.append(Spacer(1, 24))

    # 傳承風格
    story.append(Paragraph("您的傳承風格", styleH))
    story.append(Paragraph(legacy_style_result, styleN))
    story.append(Spacer(1, 12))

    # 模組二：最在意的重點
    story.append(Paragraph("模組二：您最在意的重點", styleH))
    for issue in key_issues:
        story.append(Paragraph(f"• {issue}", styleN))
    story.append(Spacer(1, 12))

    # 模組三：期望的未來方向
    story.append(Paragraph("模組三：您期望的未來方向", styleH))
    for direction in directions:
        story.append(Paragraph(f"• {direction}", styleN))
    story.append(Spacer(1, 12))

    # 總體風險評估
    story.append(Paragraph("📊 總體風險評估", styleH))
    story.append(Paragraph(summary_text, styleN))

    # 生成 PDF
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    doc.build(story)
    buffer.seek(0)
    return buffer
