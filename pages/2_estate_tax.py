import streamlit as st

st.set_page_config(page_title="遺產稅試算與壓縮", page_icon="📊", layout="wide")

st.markdown("### 📊 遺產稅試算與壓縮（展示版）")
st.caption("先看稅，再排解。用保單與節點設計，壓縮未來稅負與風險。")

c1, c2, c3 = st.columns(3)
with c1:
    estate_total = st.number_input("遺產總額（元）", min_value=0, step=1_000_000, value=300_000_000)
with c2:
    liabilities = st.number_input("可扣除負債（元）", min_value=0, step=500_000, value=20_000_000)
with c3:
    dependents = st.number_input("直系親屬人數（估）", min_value=0, value=3)

st.divider()

taxable = max(estate_total - liabilities - dependents * 4_000_000 - 13_000_000, 0)  # 示意
est_tax = int(taxable * 0.1) if taxable <= 50_000_000 else int(50_000_000*0.1 + (taxable-50_000_000)*0.2)

colx, coly = st.columns(2)
with colx:
    st.metric(label="可能課稅基（示意）", value=f"{taxable:,.0f} 元")
with coly:
    st.metric(label="可能遺產稅額（示意）", value=f"{est_tax:,.0f} 元")

st.warning("以上為教學示意，實務需依現行法規、扣除與免稅項目、資產性質與時點調整。")

st.markdown("#### 🧭 壓縮方向（摘要）")
st.success(
    "- **保單配置**：以壽險作為「指定受益」與「價值壓縮」工具，降低課稅基。\n"
    "- **贈與節點**：活用時點與金額分散，搭配變更要保人與受益人，提高效率。\n"
    "- **跨代設計**：指定第三代部分受益，維持資產秩序，避免爭議。\n"
    "- **現金流**：預留稅源與費用基金，避免被迫售資產。"
)
