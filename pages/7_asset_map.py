import streamlit as st
import matplotlib.pyplot as plt
from matplotlib import font_manager
import pandas as pd
import numpy as np
from io import BytesIO
from modules.pdf_generator import generate_asset_map_pdf
from modules.config import setup_page

# 頁面設定
setup_page("《影響力》資產結構與風險及現金流模擬")

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

# 輸入資產金額與現金流率
st.markdown("請輸入各類資產金額（萬元）及年化現金流率 (%)：")
col1, col2 = st.columns(2)
with col1:
    company = st.number_input("公司股權", 0, 1_000_000, 0, 100)
    real_estate = st.number_input("不動產", 0, 1_000_000, 0, 100)
    financial = st.number_input("金融資產", 0, 1_000_000, 0, 100)
    insurance = st.number_input("保單", 0, 1_000_000, 0, 100)
    offshore = st.number_input("海外資產", 0, 1_000_000, 0, 100)
    others = st.number_input("其他資產", 0, 1_000_000, 0, 100)
with col2:
    y_company = st.slider("公司股權 現金流率", 0.0, 20.0, 5.0, 0.1)
    y_real = st.slider("不動產 現金流率", 0.0, 20.0, 4.0, 0.1)
    y_fin = st.slider("金融資產 現金流率", 0.0, 20.0, 3.0, 0.1)
    y_ins = st.slider("保單 現金流率", 0.0, 20.0, 2.0, 0.1)
    y_off = st.slider("海外資產 現金流率", 0.0, 20.0, 3.5, 0.1)
    y_oth = st.slider("其他資產 現金流率", 0.0, 20.0, 1.0, 0.1)

# 計算與過濾數據
labels = ["公司股權","不動產","金融資產","保單","海外資產","其他"]
values = [company, real_estate, financial, insurance, offshore, others]
yields = [y_company, y_real, y_fin, y_ins, y_off, y_oth]
total_assets = sum(values)
filtered = [(lbl,val,yld) for lbl,val,yld in zip(labels,values,yields) if val>0]
filtered_labels = [f[0] for f in filtered]
filtered_values = [f[1] for f in filtered]
filtered_yields = [f[2] for f in filtered]

# 預先生成「當前資產結構」圖
if filtered_values:
    fig_current, ax_current = plt.subplots(figsize=(5,5))
    ax_current.pie(
        filtered_values,
        labels=filtered_labels,
        autopct="%1.1f%%",
        startangle=140,
        textprops={"fontproperties":font_prop}
    )
    ax_current.set_title("當前資產結構", fontproperties=font_prop)
    ax_current.axis('equal')
else:
    fig_current = None

# 預先計算現金流 DataFrame
df_cash = pd.DataFrame({
    "資產類別": labels,
    "金額(萬)": values,
    "現金流率(%)": yields
})
df_cash["年現金流(萬)"] = df_cash["金額(萬)"] * df_cash["現金流率(%)"] / 100

total_flow = df_cash["年現金流(萬)"].sum()

# 預先計算建議
suggestions = []
if total_assets>0:
    # 保單
    if df_cash.loc[3, "年現金流(萬)"] < 0.02 * total_assets:
        suggestions.append("保單現金流率偏低，建議增加高收益產品以提升固定現金流。")
    # 金融資產
    if df_cash.loc[2, "年現金流(萬)"] < 0.03 * total_assets:
        suggestions.append("金融資產現金流不足，建議調整至更高收益工具。")
    # 不動產
    if df_cash.loc[1, "金額(萬)"] > 0.4 * total_assets:
        suggestions.append("不動產比例過高，租金波動可能影響現金流穩定性。")
    # 整體
    if total_flow/ total_assets < 0.03:
        suggestions.append("整體現金流率低於3%，建議優化組合提高現金流覆蓋率。")
    if not suggestions:
        suggestions.append("現金流結構良好，請持續監控並定期調整組合。")

# 分頁展示
tab1, tab2, tab3 = st.tabs(["📊 當前結構", "💰 現金流分析", "📄 報告與行動"])

with tab1:
    st.header("1. 當前資產分佈")
    if fig_current:
        st.pyplot(fig_current)
        st.markdown(f"**資產總額：{total_assets:,.0f} 萬元**")
    else:
        st.info("尚未輸入資產數值，請先於左側輸入後檢視。")

with tab2:
    st.header("2. 年現金流分析")
    st.dataframe(df_cash.style.format({"金額(萬)":"{:,}","現金流率(%)":"{:.1f}","年現金流(萬)":"{:.1f}"}), use_container_width=True)
    if total_assets>0:
        st.markdown(f"**總年現金流：約 {total_flow:,.1f} 萬元**")
    st.subheader("分析建議")
    for s in suggestions:
        st.info(s)

with tab3:
    st.header("3. 報告與下一步")
    if fig_current:
        buf = BytesIO()
        fig_current.savefig(buf, format='png')
        buf.seek(0)
        report = generate_asset_map_pdf(labels, values, suggestions, buf)
        st.download_button("📄 下載 PDF 報告", report, "asset_cashflow_report.pdf", "application/pdf")
    else:
        st.info("請先輸入資產並進行分析後，才能下載報告。")
    st.markdown("---")
    st.markdown("若想更深入了解遺產稅影響，請前往：")
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
