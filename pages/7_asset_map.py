import streamlit as st
import matplotlib.pyplot as plt
from matplotlib import font_manager
from io import BytesIO
from modules.pdf_generator import generate_asset_map_pdf
from modules.config import setup_page  # 共用頁面設定

# 頁面設定
setup_page("《影響力》資產結構圖與風險建議")

# 中文字型
font_path = "NotoSansTC-Regular.ttf"
font_prop = font_manager.FontProperties(fname=font_path)
plt.rcParams["font.family"] = font_prop.get_name()

# 標題
st.markdown("""
<div style='text-align: center;'>
    <h2>《影響力》資產結構圖與風險建議</h2>
</div>
""", unsafe_allow_html=True)

# 輸入資產金額
st.markdown("請輸入各類資產的金額（單位：萬元）")
company = st.number_input("公司股權", min_value=0, value=0, step=100)
real_estate = st.number_input("不動產", min_value=0, value=0, step=100)
financial = st.number_input("金融資產（存款、股票、基金等）", min_value=0, value=0, step=100)
insurance = st.number_input("保單", min_value=0, value=0, step=100)
offshore = st.number_input("海外資產", min_value=0, value=0, step=100)
others = st.number_input("其他資產", min_value=0, value=0, step=100)

labels = ["公司股權", "不動產", "金融資產", "保單", "海外資產", "其他"]
values = [company, real_estate, financial, insurance, offshore, others]
total_assets = sum(values)

# 過濾非零資產
filtered = [(lbl, val) for lbl, val in zip(labels, values) if val > 0]
filtered_labels = [lbl for lbl, _ in filtered]
filtered_values = [val for _, val in filtered]

# 風險評估基準
risk_scores_map = {
    "公司股權": 0.7,
    "不動產": 0.6,
    "金融資產": 0.5,
    "保單": 0.3,
    "海外資產": 0.6,
    "其他": 0.5,
}

# 計算風險等級與對應顏色
risk_levels = []
colors = []
for lbl in filtered_labels:
    score = risk_scores_map.get(lbl, 0.5)
    if score >= 0.7:
        level = "高風險"
        color = "#FF4C4C"
    elif score >= 0.5:
        level = "中風險"
        color = "#FFA500"
    else:
        level = "低風險"
        color = "#8BC34A"
    risk_levels.append(level)
    colors.append(color)

# 畫圖
if filtered_values:
    fig1, ax1 = plt.subplots(figsize=(6, 6))
    wedges, texts, autotexts = ax1.pie(
        filtered_values,
        labels=filtered_labels,
        colors=colors,
        autopct="%1.1f%%",
        startangle=140,
        textprops={"fontsize": 12, "fontproperties": font_prop}
    )
    ax1.set_title("資產結構與風險熱度", fontproperties=font_prop, fontsize=14)
    ax1.axis('equal')
    st.pyplot(fig1)

    # 市場情境模擬
    st.markdown("---")
    st.markdown("### 🔄 市場情境模擬")
    drop_pct = st.slider("模擬市場跌幅 (%)：", -50, 0, -10)
    scenario_values = [v * (1 + drop_pct / 100) for v in filtered_values]
    fig2, ax2 = plt.subplots(figsize=(6, 6))
    wedges2, texts2, autotexts2 = ax2.pie(
        scenario_values,
        labels=filtered_labels,
        colors=colors,
        autopct="%1.1f%%",
        startangle=140,
        textprops={"fontsize": 12, "fontproperties": font_prop}
    )
    ax2.set_title(f"大盤跌 {abs(drop_pct)}% 情境下的資產分布", fontproperties=font_prop, fontsize=14)
    ax2.axis('equal')
    st.pyplot(fig2)
else:
    st.info("尚未輸入任何資產，無法顯示圖表")

# 資產總覽
percentages = [v / total_assets * 100 if total_assets else 0 for v in values]
st.markdown("### 💰 資產總覽")
st.write(f"📊 資產總額：**{total_assets:,.0f} 萬元**")
cols = st.columns(2)
for i, (label, val, pct) in enumerate(zip(labels, values, percentages)):
    with cols[i % 2]:
        st.markdown(f"◾ **{label}**：{val:,} 萬元（{pct:.1f}%）")

# 規劃建議
if total_assets > 0:
    st.markdown("---")
    st.markdown("### 📝 規劃建議摘要")
    suggestions = []
    if (insurance / total_assets) < 0.2:
        suggestions.append("保單佔比偏低，建議補強稅源工具，以降低未來繳稅與資產分配風險。")
    if (company / total_assets) > 0.3:
        suggestions.append("公司股權超過 30%，資產過度集中，應考慮股權信託或接班配置。")
    if (real_estate / total_assets) > 0.3:
        suggestions.append("不動產比重高，變現難度高，建議預留現金資源或補強保單稅源。")
    if (financial / total_assets) < 0.2:
        suggestions.append("金融資產不足，流動性可能無法應付突發稅務或照護支出。")
    if offshore > 0:
        suggestions.append("您有海外資產，請留意 CRS、FBAR 等申報義務與相關罰則風險。")
    if total_assets >= 30000:
        suggestions.append("總資產已超過 3 億元，建議進行整體資產保全架構設計。")
    if suggestions:
        for s in suggestions:
            st.info(s)
    else:
        st.success("目前資產結構整體平衡，仍建議定期檢視傳承架構與稅源預備狀況。")

    # 匯出 PDF 報告
    st.markdown("### 📥 產出報告")
    chart_buffer = BytesIO()
    fig1.savefig(chart_buffer, format="png")
    chart_buffer.seek(0)
    pdf_file = generate_asset_map_pdf(labels, values, suggestions, chart_buffer)
    st.download_button(
        label="📄 下載我的資產風險報告",
        data=pdf_file,
        file_name="asset_risk_report.pdf",
        mime="application/pdf"
    )

    # 行動導引
    st.markdown("---")
    st.markdown("📊 想知道這些資產會產生多少遺產稅？")
    if st.button("🧮 立即前往 AI秒算遺產稅"):
        st.switch_page("pages/5_estate_tax.py")

# 聯絡資訊
st.markdown("---")
st.markdown("""
<div style='display: flex; justify-content: center; align-items: center; gap: 1.5em; font-size: 14px; color: gray;'>
  <a href='/' style='color:#006666; text-decoration: underline;'>《影響力》傳承策略平台</a>
  <a href='https://gracefo.com' target='_blank'>永傳家族辦公室</a>
  <a href='mailto:123@gracefo.com'>123@gracefo.com</a>
</div>
""", unsafe_allow_html=True)
