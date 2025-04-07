import streamlit as st
from modules.pdf_generator import generate_asset_map_pdf, get_action_suggestions
from io import BytesIO
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.family'] = 'Noto Sans TC'

st.set_page_config(page_title="傳承風險圖與建議摘要", page_icon="📊", layout="centered")

st.title("📊 傳承風險圖與建議摘要")
st.caption("透過簡單輸入，盤點您的資產分佈，預見風險，提前準備。")
st.markdown("---")

# 使用 session_state 儲存使用者輸入
if 'asset_data' not in st.session_state:
    st.session_state.asset_data = {
        "公司股權": 0,
        "不動產": 0,
        "金融資產": 0,
        "保單": 0,
        "海外資產": 0,
        "其他資產": 0
    }

st.header("✅ 資產總覽")
st.caption("請輸入每項資產的預估金額（萬元）")

cols = st.columns(3)
keys = list(st.session_state.asset_data.keys())
for i, key in enumerate(keys):
    with cols[i % 3]:
        st.session_state.asset_data[key] = st.number_input(
            f"{key}", min_value=0, step=100, value=st.session_state.asset_data[key], key=key
        )

# 資產總額
asset_data = st.session_state.asset_data
total = sum(asset_data.values())
st.write(f"總資產：約 {total:,.0f} 萬元")

# 顯示表格
st.table({"資產類別": asset_data.keys(), "金額（萬元）": asset_data.values()})

# 風險提示
st.subheader("📌 傳承風險提示與建議")
risk_suggestions = []
if asset_data["公司股權"] > 0:
    risk_suggestions.append("📌 公司股權應留意接班設計與股權流動性，建議結合信託與治理規劃。")
if asset_data["不動產"] > 0:
    risk_suggestions.append("📌 不動產具價值穩定性但流動性較差，建議搭配保單以補足稅源。")
if asset_data["金融資產"] > 0:
    risk_suggestions.append("📌 金融資產雖流動性較好，但仍會在繼承發生時被凍結，建議搭配壽險安排。")
if asset_data["保單"] == 0:
    risk_suggestions.append("📌 尚未配置保單，建議初步評估稅源缺口與家族成員的保障需求。")
else:
    risk_suggestions.append("📌 已有壽險，請確認受益人設計與規劃目的，同時確認整體稅源是否足夠。")

if total == 0:
    st.info("尚未輸入資產，無法提供風險提示。")
else:
    for suggestion in risk_suggestions:
        st.write(f"- {suggestion}")

# PDF 下載按鈕
st.markdown("---")
st.subheader("📄 下載風險摘要報告")
pdf_bytes = generate_asset_map_pdf(asset_data, total, risk_suggestions, "資產分佈風險穩定")
st.download_button(
    label="📥 下載 PDF 報告",
    data=pdf_bytes,
    file_name="傳承風險圖與建議摘要.pdf",
    mime="application/pdf"
)

# 導引按鈕
st.markdown("---")
if st.button("🧮 前往 AI秒算遺產稅 模組"):
    st.switch_page("pages/5_estate_tax.py")

if st.button("🤝 預約 1 對 1 傳承諮詢"):
    st.switch_page("pages/4_contact.py")
