# -*- coding: utf-8 -*-
import streamlit as st
from ui_shared import ensure_page_config, render_header, render_footer

# 統一樣式與 favicon（/assets/favicon.png）
ensure_page_config(title="數位工具｜永傳家族辦公室")

# 共用頁首（此頁不在導覽列，但可直接訪問）
render_header()

st.subheader("🧰 工具入口")
st.markdown(
    "永傳數位家族辦公室將複雜的傳承規劃，拆解為可視化、可試算的獨立模組。您可以從這裡進入各項工具。"
)

# 主要工具
st.page_link("pages/9_risk_check.py", label="👉 傳承風險初診（1分鐘快篩）", icon="✅", use_container_width=True)
st.page_link("pages/5_estate_tax.py", label="👉 遺產/贈與稅敏感度（稅務壓縮模擬）", icon="💡", use_container_width=True)
st.page_link("pages/8_insurance_strategy.py", label="👉 保單策略模組（現金流與稅負協作）", icon="📦", use_container_width=True)

st.markdown("---")

# 進階模組（深度諮詢後使用）
st.markdown("### 更多進階模組")
st.page_link("pages/7_asset_map.py", label="🗺️ 資產地圖｜家族視覺化", use_container_width=True)
st.page_link("pages/6_retirement.py", label="💼 退休與永續金流", use_container_width=True)
st.page_link("pages/10_property.py", label="🏛️ 資產與不動產配置", use_container_width=True)

# 共用頁尾
render_footer()
