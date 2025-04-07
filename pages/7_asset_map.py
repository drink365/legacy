# --- pages/7_asset_map.py ---

import streamlit as st
import matplotlib.pyplot as plt
from matplotlib import font_manager
from io import BytesIO
from modules.pdf_generator import generate_asset_map_pdf
from modules.config import setup_page  # 共用頁面設定

# 設定頁面基本資訊
setup_page("傳承風險圖與建議摘要")

# 設定中文字型給 matplotlib 使用
font_path = "NotoSansTC-Regular.ttf"
font_prop = font_manager.FontProperties(fname=font_path)
plt.rcParams["font.family"] = font_prop.get_name()

# Logo 與頁面標題
st.image("logo.png", width=300)
st.markdown("## 傳承風險圖與建議摘要")

# 用戶輸入資產金額
st.markdown("請輸入各類資產的金額（單位：萬元）")
company = st.number_input("公司股權", min_value=0, value=1000, step=100)
real_estate = st.number_input("不動產", min_value=0, value=800, step=100)
financial = st.number_input("金融資產（存款、股票、基金等）", min_value=0, value=500, step=100)
insurance = st.number_input("保單", min_value=0, value=300, step=100)
offshore = st.number_input("海外資產", min_value=0, value=200, step=100)
others = st.number_input("其他資產", min_value=0, value=100, step=100)

labels = ["公司股權", "不動產", "金融資產", "保單", "海外資產", "其他"]
values = [company, real_estate, financial, insurance, offshore, others]

# 圓餅圖顯示
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

# 資產總覽
total_assets = sum(values)
percentages = [v / total_assets * 100 if total_assets else 0 for v in values]

st.markdown("### 💰 資產總覽")
st.write(f"📊 資產總額：**{total_assets:,.0f} 萬元**")

cols = st.columns(2)
for i, (label, val, pct) in enumerate(zip(labels, values, percentages)):
    with cols[i % 2]:
        st.markdown(f"◾ **{label}**：{val:,} 萬元（{pct:.1f}%）")

# 建議摘要
st.markdown("---")
st.markdown("### 📝 規劃建議摘要")

suggestions = []
if total_assets > 0 and (insurance / total_assets) < 0.2:
    suggestions.append("📌 保單佔比偏低，建議補強稅源工具，以降低未來繳稅與資產分配風險。")
if (company / total_assets) > 0.3:
    suggestions.append("🏢 公司股權超過 30%，資產過度集中，應考慮股權信託或接班配置。")
if (real_estate / total_assets) > 0.3:
    suggestions.append("🏠 不動產比重高，變現難度高，建議預留現金資源或補強保單稅源。")
if (financial / total_assets) < 0.2:
    suggestions.append("💵 金融資產不足，流動性可能無法應付突發稅務或照護支出。")
if offshore > 0:
    suggestions.append("🌐 您有海外資產，請留意 CRS、FBAR 等申報義務與相關罰則風險。")
if total_assets >= 30000:
    suggestions.append("🔒 總資產已超過 3 億元，建議進行整體資產保全架構設計。")

if suggestions:
    for s in suggestions:
        st.info(s)
else:
    st.success("👍 目前資產結構整體平衡，仍建議定期檢視傳承架構與稅源預備狀況。")

# 匯出 PDF 報告
chart_buffer = BytesIO()
fig.savefig(chart_buffer, format="png")
chart_buffer.seek(0)

st.markdown("### 📥 產出報告")
# 預先產出 PDF
pdf_file = generate_asset_map_pdf(labels, values, suggestions, chart_buffer)

# 一鍵下載
st.download_button(
    label="📄 下載我的資產風險報告",
    data=pdf_file,
    file_name="asset_risk_report.pdf",
    mime="application/pdf"
)


# 跨頁行動導引
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
