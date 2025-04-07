import streamlit as st
st.set_page_config(page_title="傳承風險圖與建議摘要", page_icon="📊", layout="centered")

import matplotlib.font_manager as fm
import pandas as pd
from modules.pdf_generator import generate_asset_map_pdf

# 設定中文字型
font_path = "NotoSansTC-Regular.ttf"
prop = fm.FontProperties(fname=font_path)
st.markdown("""
    <style>
    * { font-family: 'NotoSansTC-Regular', sans-serif; }
    </style>
""", unsafe_allow_html=True)

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

    submitted = st.form_submit_button("產生建議摘要")

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
    st.table(pd.DataFrame({"金額 (萬元)": asset_data}))

    st.markdown("---")
    st.markdown("### 🔍 傳承風險提示與建議")
    high_risk_count = 0
    for category, value in asset_data.items():
        if total == 0:
            continue
        ratio = value / total
        if category == "公司股權" and ratio > 0.4:
            st.warning("💼 您的『公司股權』占比偏高，建議提前規劃股權信託與接班結構。")
            high_risk_count += 1
        elif category == "不動產" and ratio > 0.4:
            st.warning("🏠 『不動產』占比較大，可能影響繼承時分配彈性，建議規劃信託或分批移轉。")
            high_risk_count += 1
        elif category == "金融資產" and ratio > 0.5:
            st.info("💰 金融資產雖流動性較好，但仍會在繼承發生時被凍結，建議搭配壽險安排。")
        elif category == "保單":
            if value > 0:
                st.success("📄 已配置保單，有助於現金補充與稅源預留，建議確認受益人與規劃目的，同時留意整體稅源是否足夠。")
            else:
                st.warning("📄 尚未配置保單，可能缺乏稅源預留與資金彈性，建議儘早評估保險規劃作為遺產稅源預備。")
                high_risk_count += 1
        elif category == "海外資產" and value > 0:
            st.warning("🌍 海外資產需留意境外稅務與申報合規，建議搭配信託與法遵規劃。")
            high_risk_count += 1
        elif category == "其他資產" and value > 0:
            st.info("📦 其他資產類型多元，建議進一步盤點細項（如藝術品、車輛、收藏等），以便評估其流動性與分配彈性。")

    # 總體評估
    st.markdown("---")
    st.markdown("### 📈 總體風險評估")
    if total == 0:
        st.info("尚未輸入資產，無法進行風險評估。")
    elif high_risk_count == 0:
        st.success("✅ 您的資產分布風險相對穩定，建議持續觀察並定期盤點。")
    elif high_risk_count <= 2:
        st.warning("⚠️ 整體風險中等，建議針對特定項目進行優化，例如稅源預留、股權安排或資產結構。")
    else:
        st.error("🚨 資產結構風險偏高，建議盡快與專業顧問討論具體的傳承與稅務安排。")

    st.markdown("---")
    st.markdown("### 📎 下載 PDF 建議報告")
    pdf_bytes = generate_asset_map_pdf(asset_data, total)
    st.download_button(
        label="📄 下載傳承風險圖報告 (PDF)",
        data=pdf_bytes,
        file_name="asset_map_summary.pdf",
        mime="application/pdf",
        use_container_width=True
    )

    st.markdown("---")
    st.markdown("### 📌 延伸工具")
    col1, col2 = st.columns(2)
    with col1:
        st.link_button("🧮 前往 AI秒算遺產稅 模組", url="/5_estate_tax", use_container_width=True)
    with col2:
        st.link_button("📞 預約 1 對 1 傳承諮詢", url="/4_contact", use_container_width=True)
