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
    font_path = "NotoSansTC-VariableFont_wght.ttf"

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

# LOGO 顯示
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

# 初始化狀態
for key in ["started", "submitted", "next_step", "module_two_done", "module_three_done", "module_four_done"]:
    if key not in st.session_state:
        st.session_state[key] = False

# 起始按鈕
if not st.session_state.started:
    if st.button("開始整理我的傳承藍圖"):
        st.session_state.started = True
        st.rerun()
    st.stop()

# 模組一
if not st.session_state.submitted:
    st.markdown("## 模組一：經營的是事業，留下的是故事")
    st.markdown("我們陪您一起梳理這段歷程，為後人留下的不只是成果，更是一種精神。")
    options = st.multiselect("您最近比較常想的是：", [
        "公司的未來要怎麼安排？",
        "孩子適不適合承接家業？",
        "退休後的生活要怎麼過？",
        "怎麼分配資產才公平？",
        "家族成員之間的關係",
        "萬一健康出現變化怎麼辦？",
        "我想慢慢退下來，但不知道從哪開始",
    ])
    custom_input = st.text_area("還有什麼最近常出現在您心裡的？（可以不填）")
    if st.button("繼續"):
        st.session_state.options = options
        st.session_state.custom_input = custom_input
        st.session_state.submitted = True
        st.rerun()

# 模組二
if st.session_state.submitted and not st.session_state.module_two_done:
    st.markdown("## 模組二：釐清內心的優先順序")
    combined = list(st.session_state.options)
    if st.session_state.custom_input.strip():
        combined.append(st.session_state.custom_input.strip())
    key_issues = st.multiselect("哪一兩件對您來說最重要？", combined, max_selections=2)
    reason = st.text_area("為什麼這件事對您來說特別重要？")
    if st.button("完成這一段思考"):
        st.session_state.key_issues = key_issues
        st.session_state.reason = reason
        st.session_state.module_two_done = True
        st.rerun()

# 模組三
if st.session_state.module_two_done and not st.session_state.module_three_done:
    st.markdown("## 模組三：從想法，到方向")
    direction_choices = st.multiselect(
        "您希望事情未來可以朝哪些方向走？",
        [
            "希望有人能逐步接手，讓我放心退下來",
            "希望我退休後，也能保有影響力與參與感",
            "希望家人之間能建立共識與溝通模式",
            "希望財務安排穩妥清楚，避免未來爭議",
            "希望即使我不在，公司與資產仍能穩定運作",
        ]
    )
    custom_dir = st.text_area("其他想補充的方向？（可以不填）")
    if st.button("完成方向探索"):
        st.session_state.directions = direction_choices
        st.session_state.custom_direction = custom_dir
        st.session_state.module_three_done = True
        st.rerun()

# 模組四
if st.session_state.module_three_done and not st.session_state.module_four_done:
    st.markdown("## 模組四：行動策略，從這裡慢慢展開")
    st.markdown("釐清了想法之後，這一步我們陪您看看有哪些小步驟可以開始安排，慢慢走、也走得穩。")
    strategies = get_strategy_suggestions()
    for s in strategies:
        with st.expander(s["title"]):
            st.write(s["details"])
    if st.button("完成策略探索"):
        st.session_state.module_four_done = True
        st.rerun()

# 模組五＋報告下載
if st.session_state.module_four_done:
    st.markdown("## 模組五：預約諮詢")
    st.markdown("🌿 恭喜您，這些思考將是未來傳承藍圖的起點。")
    st.markdown("📩 如果您想更具體地展開行動，我們誠摯邀請您預約 30 分鐘專屬對談。")
    if st.button("📆 我想預約聊聊我的想法"):
        st.info("請來信至 123@gracefo.com，我們會親自為您安排。")

    with st.expander("📄 點此下載探索紀錄 PDF"):
        pdf = generate_pdf()
        with open(pdf, "rb") as f:
            st.download_button(
                label="下載我的探索紀錄",
                data=f,
                file_name="永傳AI探索報告.pdf",
                mime="application/pdf"
            )

    st.markdown("""
📌 永傳家族辦公室｜[https://gracefo.com/](https://gracefo.com/)  
📧 Email｜[123@gracefo.com](mailto:123@gracefo.com)
""")
