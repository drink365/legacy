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

# 生成資產圖和建議摘要的 PDF
def generate_asset_map_pdf(asset_data, total, risk_suggestions, summary_text):
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

    story.append(Paragraph("資產分佈與建議摘要", styleH))
    story.append(Spacer(1, 20))

    # 生成資產資料
    story.append(Paragraph(f"總資產：約 {total:,.0f} 萬元", styleN))
    story.append(Spacer(1, 12))

    # 處理資產與風險提示
    for asset, amount in asset_data.items():
        if amount > 0:
            line = f"{asset}: {amount} 萬元"
            story.append(Paragraph(line, styleN))

    story.append(Spacer(1, 12))

    # 風險建議
    if risk_suggestions:
        story.append(Paragraph("風險提示與建議:", styleH))
        for suggestion in risk_suggestions:
            story.append(Paragraph(f"- {suggestion}", styleN))
        story.append(Spacer(1, 12))

    # 總體評估
    story.append(Paragraph(f"總體風險評估：{summary_text}", styleN))
    story.append(Spacer(1, 20))

    # 生成 PDF 文件
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    doc.build(story)
    buffer.seek(0)
    return buffer

# 生成傳承風格 PDF
def generate_legacy_pdf(legacy_style_result, key_issues, directions, summary_text):
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

    # 傳承風格
    story.append(Paragraph("傳承風格", styleH))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"您的傳承風格：{legacy_style_result}", styleN))
    story.append(Spacer(1, 12))

    # 風險評估
    story.append(Paragraph("模組二：您最在意的重點", styleH))
    for issue in key_issues:
        story.append(Paragraph(f"• {issue}", styleN))
    story.append(Spacer(1, 12))

    # 未來方向
    story.append(Paragraph("模組三：您期望的未來方向", styleH))
    for direction in directions:
        story.append(Paragraph(f"• {direction}", styleN))
    story.append(Spacer(1, 12))

    # 總體評估
    story.append(Paragraph(f"總體風險評估：{summary_text}", styleN))
    story.append(Spacer(1, 20))

    # 生成 PDF 文件
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    doc.build(story)
    buffer.seek(0)
    return buffer
