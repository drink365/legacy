from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.lib.units import mm

def generate_asset_map_pdf(asset_data, total, suggestions, summary_text):
    buffer = BytesIO()
    logo_path = "logo.png"
    font_path = "NotoSansTC-Regular.ttf"

    # 字型註冊
    pdfmetrics.registerFont(TTFont('NotoSansTC', font_path))
    styleN = ParagraphStyle(name='Normal', fontName='NotoSansTC', fontSize=12)
    styleH = ParagraphStyle(name='Heading2', fontName='NotoSansTC', fontSize=14, spaceAfter=10)
    styleC = ParagraphStyle(name='Center', fontName='NotoSansTC', fontSize=10, alignment=TA_CENTER)

    story = []

    # Logo 與標語
    try:
        logo = Image(logo_path, width=80 * mm, height=20 * mm)
        logo.hAlign = 'CENTER'
        story.append(logo)
    except:
        pass
    story.append(Spacer(1, 6))
    story.append(Paragraph("傳承您的影響力", styleC))
    story.append(Paragraph("每一位家族的掌舵者，都是家族傳承的種子。", styleC))
    story.append(Paragraph("我們陪您，讓這份影響力持續茁壯。", styleC))
    story.append(Spacer(1, 20))

    story.append(Paragraph("📊 傳承風險圖與建議摘要", styleH))
    story.append(Spacer(1, 6))

    # 資產總覽
    story.append(Paragraph("資產總額：約 {:,.0f} 萬元".format(total), styleN))
    story.append(Spacer(1, 6))

    table_data = [["資產類別", "金額（萬元）"]]
    for k, v in asset_data.items():
        table_data.append([k, "{:,.0f}".format(v)])
    table = Table(table_data, hAlign='LEFT', colWidths=[100, 100])
    table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'NotoSansTC'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ALIGN', (1, 1), (-1, -1), 'RIGHT')
    ]))
    story.append(table)
    story.append(Spacer(1, 12))

    # 風險建議
    if suggestions:
        story.append(Paragraph("🔍 傳承風險提示與建議", styleH))
        for item in suggestions:
            story.append(Paragraph(f"• {item}", styleN))
        story.append(Spacer(1, 12))

    # 總體風險評語
    story.append(Paragraph("📈 總體風險評估", styleH))
    story.append(Paragraph(summary_text, styleN))
    story.append(Spacer(1, 20))

    # 頁尾
    story.append(Paragraph("永傳家族辦公室｜https://gracefo.com/", styleC))
    story.append(Paragraph("聯絡我們：123@gracefo.com", styleC))

    # 輸出 PDF
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    doc.build(story)
    buffer.seek(0)
    return buffer
