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

st.markdown("# 傳承風險圖與建議摘要")
st.markdown("透過簡單輸入，盤點您的資產分布，預見風險、提前準備。")
st.markdown("---")

# 六大類資產輸入表單
if "submitted_asset_map" not in st.session_state:
    st.session_state.submitted_asset_map = False

if not st.session_state.submitted_asset_map:
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
        st.session_state.asset_data = {
            "公司股權": equity,
            "不動產": real_estate,
            "金融資產": financial,
            "保單": insurance,
            "海外資產": overseas,
            "其他資產": others
        }
        st.session_state.submitted_asset_map = True
        st.rerun()

if st.session_state.submitted_asset_map:
    asset_data = st.session_state.asset_data
    total = sum(asset_data.values())

    st.markdown("## 資產總覽")
    st.markdown(f"總資產：約 **{total:,.0f} 萬元**")
    st.table(pd.DataFrame({"金額 (萬元)": asset_data}))

    st.markdown("---")
    st.markdown("## 傳承風險提示與建議")
    high_risk_count = 0
    risk_suggestions = []
    for category, value in asset_data.items():
        if total == 0:
            continue
        ratio = value / total
        if category == "公司股權" and ratio > 0.4:
            msg = "您的『公司股權』占比偏高，建議提前規劃股權信託與接班結構。"
            st.warning(msg)
            risk_suggestions.append(msg)
            high_risk_count += 1
        elif category == "不動產" and ratio > 0.4:
            msg = "『不動產』占比較大，可能影響繼承時分配彈性與流動性，建議規劃信託或分批移轉。"
            st.warning(msg)
            risk_suggestions.append(msg)
            high_risk_count += 1
        elif category == "金融資產" and ratio > 0.5:
            msg = "金融資產雖流動性較好，但仍會在繼承發生時被凍結，建議搭配壽險安排。"
            st.info(msg)
            risk_suggestions.append(msg)
        elif category == "保單":
            if value > 0:
                msg = "已配置保單，有助於現金補充與稅源預留，建議確認受益人與規劃目的，同時留意整體稅源是否足夠。"
                st.success(msg)
                risk_suggestions.append(msg)
            else:
                msg = "尚未配置保單，可能缺乏稅源預留與資金彈性，建議儘早評估保險規劃作為遺產稅源預備。"
                st.warning(msg)
                risk_suggestions.append(msg)
                high_risk_count += 1
        elif category == "海外資產" and value > 0:
            msg = "海外資產需留意境外稅務與申報合規，建議搭配信託與法遵規劃。"
            st.warning(msg)
            risk_suggestions.append(msg)
            high_risk_count += 1
        elif category == "其他資產" and value > 0:
            msg = "其他資產類型多元，建議進一步盤點細項（如藝術品、車輛、收藏等），以便評估其流動性與分配彈性。"
            st.info(msg)
            risk_suggestions.append(msg)

    st.markdown("---")
    st.markdown("## 總體風險評估")
    summary_text = ""
    if total == 0:
        summary_text = "尚未輸入資產，無法進行風險評估。"
        st.info(summary_text)
    elif high_risk_count == 0:
        summary_text = "您的資產分布風險相對穩定，建議持續觀察並定期盤點。"
        st.success(summary_text)
    elif high_risk_count <= 2:
        summary_text = "整體風險中等，建議針對特定項目進行優化，例如稅源預留、股權安排或資產結構。"
        st.warning(summary_text)
    else:
        summary_text = "資產結構風險偏高，建議盡快與專業顧問討論具體的傳承與稅務安排。"
        st.error(summary_text)

    st.markdown("---")
    st.markdown("## 建議行動清單")
    st.markdown("以下是針對風險提示，您可以採取的下一步行動：")
    st.markdown("""
    - 若股權占比高：請洽顧問討論股權信託與公司治理設計。
    - 若不動產占比高：可考慮不動產信託、換屋或出售部分資產。
    - 若未配置保單：可初步評估保額、稅源與家族成員的保障需求。
    - 若有海外資產：請確保已做 FBAR/CRS 合規申報，並評估海外信託規劃。
    - 若有其他資產：建議詳細盤點內容，考慮變現與分配的難易度。
    """)

    st.markdown("---")
    st.markdown("## 下載 PDF 建議報告")
    pdf_bytes = generate_asset_map_pdf(asset_data, total, risk_suggestions, summary_text)
    st.download_button(
        label="📄 下載傳承風險圖報告 (PDF)",
        data=pdf_bytes,
        file_name="asset_map_summary.pdf",
        mime="application/pdf",
        use_container_width=True
    )

    st.markdown("---")
    st.markdown("## 延伸工具")
    st.link_button("🧮 前往 AI秒算遺產稅 模組", url="/5_estate_tax", use_container_width=True)
    st.link_button("📞 預約 1 對 1 傳承諮詢", url="/4_contact", use_container_width=True)

    st.markdown("---")
    if st.button("🔄 修改資產資料"):
        st.session_state.submitted_asset_map = False
        st.rerun()
