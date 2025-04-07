from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import mm
import re

# 註冊中文字型
pdfmetrics.registerFont(TTFont('NotoSansTC', 'NotoSansTC-Regular.ttf'))

def remove_emoji(text):
    return re.sub(r"[^\u0000-\uFFFF]", "", text)

def get_action_suggestions():
    return [
        "📌 重新檢視資產結構，確認是否已涵蓋流動性、稅源與保障需求。",
        "📌 檢查壽險與信託設計是否能對應潛在風險。",
        "📌 評估家族內部共識與接班安排是否已明確。",
        "📌 若擁有海外資產，應尋求專業稅務建議。",
        "📌 安排一次家族會議，開啟世代間傳承的對話。"
    ]

def generate_asset_map_pdf(asset_data, total, risk_suggestions, summary_text, remove_emojis=False):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)

    styleN = ParagraphStyle(name='Normal', fontName='NotoSansTC', fontSize=12)
    styleH = ParagraphStyle(name='Heading2', fontName='NotoSansTC', fontSize=14, spaceAfter=10)
    styleC = ParagraphStyle(name='Center', fontName='NotoSansTC', fontSize=10, alignment=TA_CENTER)

    def clean(text):
        return remove_emoji(text) if remove_emojis else text

    story = []

    # Logo
    try:
        logo = Image("logo.png", width=80 * mm, height=20 * mm)
        logo.hAlign = 'CENTER'
        story.append(logo)
    except:
        pass

    story.append(Spacer(1, 6))
    story.append(Paragraph(clean("傳承您的影響力"), styleC))
    story.append(Paragraph(clean("每一位家族的掌舵者，都是家族傳承的種子。"), styleC))
    story.append(Paragraph(clean("我們陪您，讓這份影響力持續茁壯。"), styleC))
    story.append(Spacer(1, 24))

    story.append(Paragraph("📊 傳承風險圖與建議摘要", styleH))
    story.append(Spacer(1, 12))

    story.append(Paragraph("一、資產總覽", styleH))
    for k, v in asset_data.items():
        story.append(Paragraph(f"{clean(k)}：{v:,.0f} 萬元", styleN))
    story.append(Paragraph(f"總資產：約 {total:,.0f} 萬元", styleN))
    story.append(Spacer(1, 12))

    if total > 0:
        story.append(Paragraph("二、傳承風險提示", styleH))
        for tip in risk_suggestions:
            story.append(Paragraph(f"- {clean(tip)}", styleN))
        story.append(Spacer(1, 12))

        story.append(Paragraph("三、總體風險評估", styleH))
        story.append(Paragraph(clean(summary_text), styleN))
        story.append(Spacer(1, 12))

        story.append(Paragraph("四、建議行動清單", styleH))
        for act in get_action_suggestions():
            story.append(Paragraph(f"- {clean(act)}", styleN))
        story.append(Spacer(1, 12))

    story.append(Spacer(1, 20))
    story.append(Paragraph("永傳家族辦公室｜https://gracefo.com/", styleC))
    story.append(Paragraph("聯絡我們：123@gracefo.com", styleC))

    doc.build(story)
    buffer.seek(0)
    return buffer
