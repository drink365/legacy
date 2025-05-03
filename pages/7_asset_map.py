import streamlit as st
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np
import pandas as pd
from io import BytesIO
from modules.pdf_generator import generate_asset_map_pdf
from modules.config import setup_page  # 共用頁面設定

# 頁面設定
setup_page("《影響力》資產結構圖與風險及現金流模擬")

# 中文字型設定
font_path = "NotoSansTC-Regular.ttf"
font_prop = font_manager.FontProperties(fname=font_path)
plt.rcParams["font.family"] = font_prop.get_name()

# 標題
st.markdown("""
<div style='text-align: center;'>
    <h2>《影響力》資產結構、風險與現金流模擬</h2>
</div>
""", unsafe_allow_html=True)

# 1. 輸入當前資產
st.markdown("## 1. 當前資產分佈（現在的情況）")
st.markdown("請輸入各類資產金額（萬元）及預期年化現金流率（%）")
col1, col2 = st.columns(2)
with col1:
    company = st.number_input("公司股權", min_value=0, value=0, step=100)
    real_estate = st.number_input("不動產", min_value=0, value=0, step=100)
    financial = st.number_input("金融資產", min_value=0, value=0, step=100)
    insurance = st.number_input("保單", min_value=0, value=0, step=100)
    offshore = st.number_input("海外資產", min_value=0, value=0, step=100)
    others = st.number_input("其他資產", min_value=0, value=0, step=100)
with col2:
    y_company = st.slider("公司股權 現金流率(%)", 0.0, 20.0, 5.0, step=0.1)
    y_real_estate = st.slider("不動產 現金流率(%)", 0.0, 20.0, 4.0, step=0.1)
    y_financial = st.slider("金融資產 現金流率(%)", 0.0, 20.0, 3.0, step=0.1)
    y_insurance = st.slider("保單 現金流率(%)", 0.0, 20.0, 2.0, step=0.1)
    y_offshore = st.slider("海外資產 現金流率(%)", 0.0, 20.0, 3.5, step=0.1)
    y_others = st.slider("其他資產 現金流率(%)", 0.0, 20.0, 1.0, step=0.1)

labels = ["公司股權", "不動產", "金融資產", "保單", "海外資產", "其他"]
values = [company, real_estate, financial, insurance, offshore, others]
yields = [y_company, y_real_estate, y_financial, y_insurance, y_offshore, y_others]
total_assets = sum(values)

# 過濾
filtered = [(lbl, val, yd) for lbl, val, yd in zip(labels, values, yields) if val>0]
filtered_labels = [f[0] for f in filtered]
filtered_values = [f[1] for f in filtered]
filtered_yields = [f[2] for f in filtered]

# 畫當前結構
if filtered_values:
    fig1, ax1 = plt.subplots(figsize=(5,5))
    ax1.pie(filtered_values, labels=filtered_labels, autopct="%1.1f%%", startangle=140,
            textprops={"fontproperties":font_prop})
    ax1.set_title("當前資產結構", fontproperties=font_prop)
    ax1.axis('equal')
    st.pyplot(fig1)
else:
    st.info("尚未輸入資產，無法顯示結構圖")

# 資產總覽數據
if total_assets>0:
    st.markdown("### 資產總覽與現金流率")
    df = pd.DataFrame({"資產類別": labels, "金額": values, "現金流率(%)": yields})
    df["現金流(年)"] = df["金額"] * df["現金流率(%)"] / 100
    st.table(df.style.format({"金額":"{:,}", "現金流率(%)":"{:.1f}", "現金流(年)":"{:.0f}"}))

# 2. 規劃建議摘要
if total_assets>0:
    st.markdown("---")
    st.markdown("## 2. 規劃建議摘要")
    suggestions=[]
    if insurance/total_assets<0.2:
        suggestions.append("保單現金流率較低，建議增加高收益保險產品或其他固定收益工具。")
    if financial/total_assets<0.2:
        suggestions.append("金融資產佔比低，流動現金流建議提高至至少20%。")
    if real_estate/total_assets>0.4:
        suggestions.append("不動產佔比過高，市況波動可能影響租金收入與整體流動性。")
    if sum(df["現金流(年)"])/total_assets<0.03*10000:
        suggestions.append("整體年化現金流率低於3%，建議優化資產組合以提高現金流覆蓋率。 ")
    if suggestions:
        for s in suggestions: st.info(s)
    else:
        st.success("現金流結構良好，建議持續監控市場機遇與風險動態。")

    # 3. 下載報告
    st.markdown("---")
    st.markdown("## 3. 下載資產及現金流報告")
    buf=BytesIO(); fig1.savefig(buf,format='png'); buf.seek(0)
    pdf=generate_asset_map_pdf(labels,values,suggestions,buf)
    st.download_button("📄 下載 PDF 報告", pdf, "asset_cashflow_report.pdf","application/pdf")

    # 4. 進一步規劃
    st.markdown("---")
    st.markdown("## 4. 進一步規劃")
    if st.button("🧮 前往 AI秒算遺產稅"):
        st.switch_page("pages/5_estate_tax.py")

# 聯絡資訊
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:gray; font-size:14px;'>
    <a href='/' style='color:#006666; text-decoration:underline;'>《影響力》傳承策略平台</a> |
    <a href='https://gracefo.com' target='_blank'>永傳家族辦公室</a> |
    <a href='mailto:123@gracefo.com'>123@gracefo.com</a>
</div>
""", unsafe_allow_html=True)
