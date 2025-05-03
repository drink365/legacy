import streamlit as st
import matplotlib.pyplot as plt
from matplotlib import font_manager
import pandas as pd
import numpy as np
from io import BytesIO
from modules.pdf_generator import generate_asset_map_pdf
from modules.config import setup_page

# 頁面設定
setup_page("《影響力》資產結構、風險與現金流模擬")

# 字型設定
font_path = "NotoSansTC-Regular.ttf"
font_prop = font_manager.FontProperties(fname=font_path)
plt.rcParams["font.family"] = font_prop.get_name()

# 標題
st.markdown(
    "<div style='text-align:center;'>"
    "<h2>《影響力》資產結構、風險與現金流模擬</h2>"
    "</div>", unsafe_allow_html=True
)

# 1. 輸入區放在側邊欄
st.sidebar.header("🔧 輸入參數")
st.sidebar.markdown("請輸入資產金額（萬元）與現金流率 (%)：")
labels = ["公司股權","不動產","金融資產","保單","海外資產","其他"]
values = []
yields = []
for asset in labels:
    val = st.sidebar.number_input(f"{asset} 金額", min_value=0, value=0, step=100)
    rate = st.sidebar.slider(f"{asset} 年化現金流率(%)", 0.0, 20.0, 3.0, 0.1)
    values.append(val)
    yields.append(rate)

total_assets = sum(values)
# 計算年現金流
df = pd.DataFrame({"資產類別": labels, "金額(萬)": values, "現金流率(%)": yields})
df["年現金流(萬)"] = df["金額(萬)"] * df["現金流率(%)"] / 100
total_flow = df["年現金流(萬)"].sum()

# 2. 首屏 Metric 卡片
col1, col2, col3 = st.columns(3)
col1.metric("總資產(萬)", f"{total_assets:,.0f}")
col2.metric("總年現金流(萬)", f"{total_flow:,.1f}")
avg_yield = (total_flow / total_assets * 100) if total_assets else 0
col3.metric("平均現金流率(%)", f"{avg_yield:.2f}")

# 3. 主要圖表區：左圓餅圖、右長條圖
if total_assets>0:
    fig, axes = plt.subplots(1, 2, figsize=(10,4))
    # 圓餅圖
    vals = [v for v in values if v>0]
    labs = [l for l,v in zip(labels, values) if v>0]
    axes[0].pie(vals, labels=labs, autopct="%1.1f%%", startangle=140,
               textprops={"fontproperties":font_prop, "fontsize":10})
    axes[0].set_title("資產結構分佈", fontproperties=font_prop)
    axes[0].axis('equal')
    # 長條圖
    axes[1].bar(df["資產類別"], df["年現金流(萬)"], color='#8BC34A')
    axes[1].set_title("年現金流(萬) 比對", fontproperties=font_prop)
    axes[1].set_ylabel("年現金流(萬)")
    plt.setp(axes[1].get_xticklabels(), rotation=45, ha='right')
    st.pyplot(fig)
else:
    st.info("尚未輸入任何資產，請於側邊欄輸入後查看圖表。")

# 4. 展開細節區
with st.expander("🔍 查看現金流明細與建議"):
    if total_assets>0:
        st.subheader("資產與現金流明細表")
        st.dataframe(df.style.format({"金額(萬)":"{:,}", "現金流率(%)":"{:.1f}", "年現金流(萬)":"{:.1f}"}), use_container_width=True)
        st.markdown(f"- **總年現金流(萬)：{total_flow:,.1f}**")
        # 建議摘要
        st.subheader("建議摘要")
        suggestions = []
        if df.loc[labels.index("保單"), "年現金流(萬)"] < 0.02 * total_assets:
            suggestions.append("保單現金流率偏低，建議增加高收益產品以提升固定現金流。")
        if df.loc[labels.index("金融資產"), "年現金流(萬)"] < 0.03 * total_assets:
            suggestions.append("金融資產現金流不足，建議調整至更高收益工具。")
        if df.loc[labels.index("不動產"), "金額(萬)"] > 0.4 * total_assets:
            suggestions.append("不動產比例過高，租金波動可能影響現金流穩定性。")
        if total_flow / total_assets < 0.03:
            suggestions.append("整體現金流率低於3%，建議優化組合提高現金流覆蓋率。")
        if not suggestions:
            suggestions.append("現金流結構良好，請持續監控並定期調整組合。")
        for s in suggestions:
            st.info(s)
    else:
        st.info("請先輸入資產並設定現金流率後，才能查看明細與建議。")

# 5. 報告下載與進一步規劃
with st.expander("📄 下載報告與下一步"):
    if total_assets>0:
        buf = BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        report = generate_asset_map_pdf(labels, values, suggestions, buf)
        st.download_button("📄 下載資產及現金流報告", report, "asset_cashflow_report.pdf", "application/pdf")
    else:
        st.info("報告需先輸入資產並完成分析。")
    st.markdown("---")
    st.markdown("如需深入遺產稅影響分析：")
    if st.button("🧮 AI 秒算遺產稅"):
        st.switch_page("pages/5_estate_tax.py")

# 聯絡資訊
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:gray; font-size:14px;'>"
    "<a href='/' style='color:#006666; text-decoration:underline;'>《影響力》傳承策略平台</a> | "
    "<a href='https://gracefo.com' target='_blank'>永傳家族辦公室</a> | "
    "<a href='mailto:123@gracefo.com'>123@gracefo.com</a>"
    "</div>", unsafe_allow_html=True
)
