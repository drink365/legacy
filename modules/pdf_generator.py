from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import mm
import streamlit as st

# 註冊字型
def register_font():
    font_path = "NotoSansTC-Regular.ttf"  # 修改為你的字型檔案
    pdfmetrics.registerFont(TTFont('NotoSansTC', font_path))

# 生成資產風險圖 PDF
def generate_asset_map_pdf(asset_data, total, risk_suggestions, summary_text):
    buffer = BytesIO()

    # 註冊字型
    register_font()

    styleN = ParagraphStyle(name='Normal', fontName='NotoSansTC', fontSize=12)
    styleH = ParagraphStyle(name='Heading2', fontName='NotoSansTC', fontSize=14, spaceAfter=10)
    styleC = ParagraphStyle(name='Center', fontName='NotoSansTC', fontSize=10, alignment=TA_CENTER)

    story = []
    logo_path = "logo.png"
    logo = Image(logo_path, width=80 * mm, height=20 * mm)
    logo.hAlign = 'CENTER'
    story.append(logo)
    story.append(Spacer(1, 6))
    story.append(Paragraph("傳承風險圖與建議摘要", styleC))
    story.append(Spacer(1, 24))

    # 資產類別與金額
    story.append(Paragraph("資產總覽", styleH))
    story.append(Spacer(1, 6))
    for key, value in asset_data.items():
        story.append(Paragraph(f"{key}: {value:,} 萬元", styleN))

    story.append(Spacer(1, 24))

    # 風險提示
    story.append(Paragraph("📌 傳承風險提示與建議", styleH))
    for suggestion in risk_suggestions:
        story.append(Paragraph(f"- {suggestion}", styleN))
    
    story.append(Spacer(1, 24))

    # 總體評估
    story.append(Paragraph("📊 總體風險評估", styleH))
    story.append(Paragraph(summary_text, styleN))

    # 行動建議
    story.append(Spacer(1, 24))
    story.append(Paragraph("🛠️ 建議行動清單", styleH))
    for action in get_action_suggestions():
        story.append(Paragraph(f"- {action}", styleN))

    # PDF 設定
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    doc.build(story)
    buffer.seek(0)
    return buffer


# 生成傳承風格 PDF
def generate_legacy_pdf(legacy_style_result, key_issues, directions, summary_text):
    buffer = BytesIO()

    # 註冊字型
    register_font()

    styleN = ParagraphStyle(name='Normal', fontName='NotoSansTC', fontSize=12)
    styleH = ParagraphStyle(name='Heading2', fontName='NotoSansTC', fontSize=14, spaceAfter=10)
    styleC = ParagraphStyle(name='Center', fontName='NotoSansTC', fontSize=10, alignment=TA_CENTER)

    story = []
    logo_path = "logo.png"
    logo = Image(logo_path, width=80 * mm, height=20 * mm)
    logo.hAlign = 'CENTER'
    story.append(logo)
    story.append(Spacer(1, 6))
    story.append(Paragraph("傳承探索報告", styleC))
    story.append(Spacer(1, 24))

    # 傳承風格
    story.append(Paragraph("您的傳承風格", styleH))
    story.append(Paragraph(legacy_style_result, styleN))
    story.append(Spacer(1, 12))

    # 關鍵問題
    story.append(Paragraph("模組二：您最在意的重點", styleH))
    for issue in key_issues:
        story.append(Paragraph(f"• {issue}", styleN))

    story.append(Spacer(1, 12))

    # 期望未來方向
    story.append(Paragraph("模組三：您期望的未來方向", styleH))
    for d in directions:
        story.append(Paragraph(f"• {d}", styleN))

    story.append(Spacer(1, 12))

    # 總體評估
    story.append(Paragraph("📊 總體風險評估", styleH))
    story.append(Paragraph(summary_text, styleN))

    # PDF 設定
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    doc.build(story)
    buffer.seek(0)
    return buffer


# 取得建議行動清單
def get_action_suggestions():
    return [
        "✅ 規劃家族會議，討論家族價值觀與未來方向",
        "✅ 盤點目前所有資產，並檢視其流動性及稅務狀況",
        "✅ 開始設計企業接班計劃，確定接班人選",
        "✅ 與專業顧問協作，建立信託和保險計劃"
    ]
