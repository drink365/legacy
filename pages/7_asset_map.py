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

# 標籤分頁
tab1, tab2, tab3 = st.tabs(["📊 當前結構", "💰 現金流分析", "📄 報告與行動"])

# 輸入與當前結構
with tab1:
    st.header("1. 當前資產分佈")
    st.markdown("請於下方輸入各類資產金額（單位：萬元）：")
    cols = st.columns(2)
    with cols[0]:
        company = st.number_input("公司股權", 0, 1_000_000, 0, 100)
        real_estate = st.number_input("不動產", 0, 1_000_000, 0, 100)
        financial = st.number_input("金融資產", 0, 1_000_000, 0, 100)
    with cols[1]:
        insurance = st.number_input("保單", 0, 1_000_000, 0, 100)
        offshore = st.number_input("海外資產", 0, 1_000_000, 0, 100)
        others = st.number_input("其他資產", 0, 1_000_000, 0, 100)

    labels = ["公司股權", "不動產", "金融資產", "保單", "海外資產", "其他"]
    values = [company, real_estate, financial, insurance, offshore, others]
    total = sum(values)

    if total > 0:
        filtered = [(l, v) for l, v in zip(labels, values) if v>0]
        names, vals = zip(*filtered)
        fig, ax = plt.subplots(figsize=(5,5))
        ax.pie(vals, labels=names, autopct="%1.1f%%", startangle=140,
               textprops={"fontproperties":font_prop})
        ax.set_title("當前資產結構", fontproperties=font_prop)
        ax.axis('equal')
        st.pyplot(fig)
        st.markdown(f"**資產總額：{total:,.0f} 萬元**")
    else:
        st.info("尚未輸入資產數值，請輸入後檢視結構圖。")

# 現金流率與年現金流
with tab2:
    st.header("2. 年現金流分析")
    st.markdown("設定各類資產的預期年化現金流率 (%)，系統將計算年現金收入：")
    cols = st.columns(2)
    with cols[0]:
        y_company = st.slider("公司股權 現金流率", 0.0, 20.0, 5.0, 0.1)
        y_real = st.slider("不動產 現金流率", 0.0, 20.0, 4.0, 0.1)
        y_fin = st.slider("金融資產 現金流率", 0.0, 20.0, 3.0, 0.1)
    with cols[1]:
        y_ins = st.slider("保單 現金流率", 0.0, 20.0, 2.0, 0.1)
        y_off = st.slider("海外資產 現金流率", 0.0, 20.0, 3.5, 0.1)
        y_oth = st.slider("其他資產 現金流率", 0.0, 20.0, 1.0, 0.1)

    yields = [y_company, y_real, y_fin, y_ins, y_off, y_oth]
    df = pd.DataFrame({"資產類別": labels, "金額(萬)": values, "現金流率(%)": yields})
    df["年現金流(萬)"] = df["金額(萬)"] * df["現金流率(%)"] / 100
    st.dataframe(df.style.format({"金額(萬)":"{:,}", "現金流率(%)":"{:.1f}", "年現金流(萬)":"{:.1f}"}))

    total_flow = df["年現金流(萬)"].sum()
    if total > 0:
        st.markdown(f"**總年現金流：約 {total_flow:,.1f} 萬元**")

    st.subheader("建議摘要")
    suggestions = []
    if df.loc[3, "年現金流(萬)"] < 0.02 * total:
        suggestions.append("保單現金流率偏低，建議增加高收益產品以提升固定現金流。")
    if df.loc[2, "年現金流(萬)"] < 0.03 * total:
        suggestions.append("金融資產現金流不足，建議調整至更高收益工具。")
    if df.loc[1, "金額(萬)"] > 0.4 * total:
        suggestions.append("不動產比例過高，租金波動可能影響現金流穩定性。")
    if total_flow/total < 0.03:
        suggestions.append("整體現金流率低於3%，建議優化組合提高現金流覆蓋率。 ")
    if suggestions:
        for s in suggestions:
            st.info(s)
    else:
        st.success("現金流結構良好，請持續監控並定期調整組合。")

# 報告與行動
with tab3:
    st.header("3. 報告與下一步")
    buf = BytesIO()
    # 使用當前第一張圖保存為示例
    fig.savefig(buf, format='png')
    buf.seek(0)
    report = generate_asset_map_pdf(labels, values, suggestions, buf)
    st.download_button("📄 下載 PDF 報告", report, "asset_cashflow_report.pdf", "application/pdf")
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
