import streamlit as st
from utils.pdf import export_proposal_pdf

st.set_page_config(page_title="保單策略模擬器", page_icon="📦", layout="wide")

st.markdown("### 📦 保單策略模擬器（展示版）")
st.caption("以保單為核心，設計「保障 × 傳承 × 現金流」的最適結構。")

col1, col2, col3 = st.columns(3)
with col1:
    age = st.number_input("年齡", min_value=0, max_value=100, value=55)
    gender = st.selectbox("性別", ["女", "男"], index=0)
with col2:
    budget = st.number_input("年繳保費（元）", min_value=0, step=10000, value=3_000_000)
    years = st.selectbox("繳費年期", [1, 3, 5, 6, 7, 10], index=2)
with col3:
    currency = st.selectbox("幣別", ["TWD", "USD"], index=0)
    need = st.selectbox("需求類型", ["退休/現金流", "傳承/保額", "綜合平衡"], index=1)

st.divider()

direction = "提高保額結構，搭配變更要保人與指定受益人" if need == "傳承/保額" else             "重視現金價值與現金流，搭配保單貸款與分期給付機制" if need == "退休/現金流" else             "保額 × 現金價值平衡，保留彈性與資產隔離機制"

st.success(
    f"**策略摘要**：{direction}\n\n"
    "- 以保單為「資產載體」，隔離風險、指定受益、加速交棒。\n"
    "- 結合贈與節點與變更要保人，達到**稅負壓縮**與**分流**。\n"
    "- 規劃「分期給付」如同類信託，**降低管理成本**且保有彈性。"
)

colA, colB = st.columns([2,1])
with colA:
    st.markdown("#### 📋 建議配置（示意）")
    st.table({
        "項目": ["年繳保費", "繳費年期", "預估目標", "策略方向"],
        "內容": [f"{budget:,.0f} {currency}", f"{years} 年", need, direction]
    })
with colB:
    if st.button("⬇️ 匯出提案 PDF / TXT"):
        content = [
            {"heading":"條件摘要", "content": f"年齡：{age} 歲 / 性別：{gender} / 幣別：{currency}\n年繳保費：{budget:,.0f} / 繳費年期：{years}"},
            {"heading":"策略摘要", "content": direction},
            {"heading":"顧問說明", "content":"以保單作為資產載體，搭配贈與節點、變更要保人與指定受益機制，達到稅負壓縮與秩序化交棒。"}
        ]
        data, mime, filename = export_proposal_pdf("保單策略提案（展示版）", content)
        st.download_button("下載提案", data=data, file_name=filename, mime=mime)

st.info("**顧問版** 可接上商品參數（保額係數、現價曲線、IRR），自動生成對比表與 PDF。")
