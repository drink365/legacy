import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
from io import BytesIO
from modules.pdf_generator import generate_asset_map_pdf

# 設定中文字型
font_path = "NotoSansTC-Regular.ttf"
prop = fm.FontProperties(fname=font_path)
plt.rcParams["font.family"] = prop.get_name()

st.set_page_config(page_title="傳承風險圖與建議摘要", page_icon="📊", layout="wide")
st.markdown("# 📊 傳承風險圖與建議摘要")
st.markdown("透過簡單輸入，盤點您的資產分布，預見風險、提前準備。")
st.markdown("---")

# 六大類資產輸入表單
with st.form("asset_form"):
    col1, col2 = st.columns(2)
    with col1:
        equity = st.number_input("公司股權 (萬元)", min_value=0, value=0, step=100)
        real_estate = st.number_input("不動產 (萬元)", min_value=0, value=0, step=100)
        financial = st.number_input("金融資產（存款、股票、基金等）(萬元)", min_value=0, value=0, step=100)
    with col2:
        insurance = st.number_input("保單 (萬元)", min_value=0, value=0, step=100)
        overseas = st.number_input("海外資產 (萬元)", min_value=0, value=0, step=100)
        others = st.number_input("其他資產 (萬元)", min_value=0, value=0, step=100)

    submitted = st.form_submit_button("產生風險圖")

# 若按下按鈕，顯示風險圖與總覽
if submitted:
    asset_data = {
        "公司股權": equity,
        "不動產": real_estate,
        "金融資產": financial,
        "保單": insurance,
        "海外資產": overseas,
        "其他資產": others
    }

    total = sum(asset_data.values())
    st.markdown("### ✅ 資產總覽")
    st.markdown(f"總資產：約 **{total:,.0f} 萬元**")

    if total == 0:
        st.info("請輸入資產資料以產生圖表與分析建議。")
    else:
        # 長條圖
        fig, ax = plt.subplots(figsize=(5, 2.5))
        categories = list(asset_data.keys())
        values = list(asset_data.values())
        bars = ax.bar(categories, values, color="#C62828")
        ax.set_ylabel("金額 (萬元)", fontsize=10)
        ax.set_title("資產分布圖", fontsize=12)
        ax.tick_params(axis='x', labelrotation=30, labelsize=8)
        ax.tick_params(axis='y', labelsize=8)
        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2.0, yval + total*0.01, f"{int(yval):,}",
                    ha='center', va='bottom', fontsize=8)
        st.pyplot(fig)

        # 傳承風險提示
        st.markdown("---")
        st.markdown("### 🔍 傳承風險提示")
        shown = False
        if equity > total * 0.5:
            st.warning("您的資產過度集中於『公司股權』，建議考慮股權信託或保險來分散風險與稅負。")
            shown = True
        if real_estate > total * 0.4:
            st.info("您持有較多不動產，可事先規劃移轉方式，避免未來繼承時產生糾紛或變現困難。")
            shown = True
        if financial > total * 0.5:
            st.success("金融資產具流動性，有助於預留稅源與安排傳承，但仍需搭配整體架構設計。")
            shown = True
        if not shown:
            st.markdown("目前您的資產分布相對平均，請持續關注未來的變化與傳承安排。")

        # PDF 下載
        st.markdown("---")
        st.markdown("### 📎 下載 PDF 總結報告")
        pdf_bytes = generate_asset_map_pdf(asset_data, total)
        st.download_button(
            label="📄 下載傳承風險圖報告 (PDF)",
            data=pdf_bytes,
            file_name="asset_map_summary.pdf",
            mime="application/pdf"
        )

        # 補充導引按鈕
        st.markdown("---")
        st.markdown("### 📌 想進一步了解遺產稅試算？")
        st.page_link("pages/5_estate_tax.py", label="🔗 前往 AI秒算遺產稅 模組", icon="🧮")

        st.markdown("---")
        st.markdown("### 🗂️ 需要專人協助擬定傳承策略？")
        st.page_link("pages/4_contact.py", label="📞 預約 1 對 1 諮詢", icon="📌")
