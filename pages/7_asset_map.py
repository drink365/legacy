import streamlit as st
import matplotlib.pyplot as plt
from matplotlib import font_manager
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from io import BytesIO

# 註冊字型給 matplotlib 使用
font_path = "NotoSansTC-Regular.ttf"
font_prop = font_manager.FontProperties(fname=font_path)
plt.rcParams["font.family"] = font_prop.get_name()

# 頁面設定
st.set_page_config(
    page_title="傳承風險圖與建議摘要",
    page_icon="📊",
    layout="centered"
)

# Logo與標題
st.image("logo.png", width=300)
st.markdown("## 傳承風險圖與建議摘要")

# 用戶輸入資產金額
st.markdown("請輸入各類資產的金額（單位：萬元）")
company = st.number_input("公司股權", min_value=0, value=10000, step=100)
real_estate = st.number_input("不動產", min_value=0, value=8000, step=100)
financial = st.number_input("金融資產（存款、股票、基金等）", min_value=0, value=5000, step=100)
insurance = st.number_input("保單", min_value=0, value=3000, step=100)
offshore = st.number_input("海外資產", min_value=0, value=2000, step=100)
others = st.number_input("其他資產", min_value=0, value=1000, step=100)

# 總覽與風險提示
labels = ["公司股權", "不動產", "金融資產", "保單", "海外資產", "其他"]
values = [company, real_estate, financial, insurance, offshore, others]

# 圖表呈現
fig, ax = plt.subplots(figsize=(6, 6))
wedges, texts, autotexts = ax.pie(
    values,
    labels=labels,
    autopct="%1.1f%%",
    startangle=140,
    textprops={"fontsize": 12, "fontproperties": font_prop}
)
ax.axis("equal")
st.pyplot(fig)

# 建議摘要
st.markdown("---")
st.markdown("### 📝 規劃建議摘要")

if insurance < (company + financial + real_estate) * 0.2:
    st.warning("📌 建議保單比重可再強化，以利稅源預留與資產傳承。")

if offshore > 0:
    st.info("🌐 您有海外資產，請留意申報義務與稅務風險。")

if company > financial:
    st.info("🏢 公司股權佔比較高，建議思考股權配置與接班安排。")

# 行動導引 CTA
st.markdown("---")
st.markdown("📊 想知道這些資產會產生多少遺產稅？")
if st.button("🧮 立即前往 AI秒算遺產稅"):
    st.switch_page("pages/5_estate_tax.py")

# 頁尾資訊
st.markdown("---")
st.markdown("""
<div style='text-align: center; font-size: 14px; color: gray;'>
永傳家族辦公室｜<a href="https://gracefo.com" target="_blank">https://gracefo.com</a><br>
聯絡信箱：<a href="mailto:123@gracefo.com">123@gracefo.com</a>
</div>
""", unsafe_allow_html=True)
