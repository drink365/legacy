import streamlit as st

st.set_page_config(page_title="不動產稅負評估 | 永傳家族傳承教練")
st.markdown("# 不動產稅負評估 💼🏠")

st.markdown("---")

st.markdown("### 📌 房屋基本資訊輸入")
col1, col2 = st.columns(2)
with col1:
    market_price = st.number_input("市價（萬元）", value=3000)
    building_value = st.number_input("房屋評定現值（萬元）", value=200)
with col2:
    land_current_value = st.number_input("土地公告現值（萬元）", value=1000)

st.markdown("---")

st.markdown("### 🏠 房產登記與資金來源選項")
registration_target = st.radio("房屋登記於誰名下？", ["父母", "子女"], index=0)

if registration_target == "父母":
    transfer_plan = st.radio("未來規劃為何？", ["留待繼承", "未來贈與給子女"], index=0)
    parent_hold_years = st.number_input("父母持有年數", value=10)
    if transfer_plan == "留待繼承":
        child_hold_years = st.number_input("繼承後子女持有年數", value=2)
    else:
        child_hold_years = st.number_input("贈與後子女持有年數", value=2)
elif registration_target == "子女":
    transfer_plan = st.radio("資金來源為何？", ["子女自備購屋款", "父母贈與現金購屋"], index=0)
    child_hold_years = st.number_input("子女持有年數", value=2)

st.markdown("---")

# 土增稅模組區塊
st.markdown("### 🧮 土地增值稅試算")

st.info("說明：依是否符合自用住宅稅率（10%）或一般用地累進稅率（20%～40%）計算稅負。")

col3, col4 = st.columns(2)
with col3:
    original_land_value = st.number_input("原始公告現值（萬元）", value=500)
    adjusted_land_value = st.number_input("未來公告現值（萬元）", value=1200)
with col4:
    multiplier = st.number_input("政府調整倍率", value=3.0, step=0.1)
    is_self_use = st.radio("是否符合自用住宅條件？", ["是", "否"], index=0)

# 決定實際持有年數
if registration_target == "父母" and transfer_plan == "留待繼承":
    hold_years = parent_hold_years + child_hold_years
elif registration_target == "父母" and transfer_plan == "未來贈與給子女":
    hold_years = child_hold_years
elif registration_target == "子女":
    hold_years = child_hold_years
else:
    hold_years = 0

increment_amount = (adjusted_land_value - original_land_value) * multiplier

# 土增稅邏輯
land_tax = 0
if is_self_use == "是" and hold_years >= 6:
    land_tax = increment_amount * 0.10
    tax_note = f"符合自用條件，實際持有 {hold_years} 年，適用稅率10%"
else:
    if increment_amount <= 400:
        land_tax = increment_amount * 0.20
    elif increment_amount <= 800:
        land_tax = 400 * 0.20 + (increment_amount - 400) * 0.30
    else:
        land_tax = 400 * 0.20 + 400 * 0.30 + (increment_amount - 800) * 0.40
    tax_note = f"一般用地，持有 {hold_years} 年，依增值級距套用20~40%累進稅率"

st.success(f"土地漲價總數額：約 {increment_amount:.1f} 萬元\n\n{tax_note} → 土地增值稅：約 {land_tax:.1f} 萬元")

st.markdown("---")

# --- 聯絡資訊 ---
st.markdown("""
<div style='display: flex; justify-content: center; align-items: center; gap: 1.5em; font-size: 14px; color: gray;'>
  <a href='/' style='color:#006666; text-decoration: underline;'>《影響力》傳承策略平台</a>
  <a href='https://gracefo.com' target='_blank'>永傳家族辦公室</a>
  <a href='mailto:123@gracefo.com'>123@gracefo.com</a>
</div>
""", unsafe_allow_html=True)
