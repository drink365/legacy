import streamlit as st

st.set_page_config(page_title="不動產稅負評估 | 永傳家族傳承教練")
st.markdown("# 不動產稅負評估 💼🏠")

st.markdown("---")

st.markdown("### 📌 房屋基本資訊輸入")
col1, col2 = st.columns(2)
with col1:
    land_current_value = st.number_input("土地公告現值（萬元）", value=1000)
    building_value = st.number_input("房屋評定現值（萬元）", value=200)
with col2:
    market_price = st.number_input("房屋市價（萬元）", value=3000)

st.markdown("---")

st.markdown("### 🏠 房產登記與資金來源選項")
registration_target = st.radio("房屋登記於誰名下？", ["父母", "子女"], index=0)

if registration_target == "父母":
    transfer_plan = st.radio("未來規劃為何？", ["留待繼承", "未來贈與給子女"], index=0)
    parent_hold_years = st.number_input("父母持有年數", value=10)
    transfer_announcement_value = st.number_input("移轉當時土地公告現值（萬元）", value=1100)
    transfer_market_value = st.number_input("移轉當時房屋市價（萬元）", value=3200)
    transfer_building_value = st.number_input("移轉當時房屋評定現值（萬元）", value=220)
    if transfer_plan == "留待繼承":
        child_hold_years = st.number_input("繼承後子女持有年數", value=2)
    else:
        child_hold_years = st.number_input("贈與後子女持有年數", value=2)
elif registration_target == "子女":
    transfer_plan = st.radio("資金來源為何？", ["子女自備購屋款", "父母贈與現金購屋"], index=0)
    child_hold_years = st.number_input("子女持有年數", value=2)
    transfer_announcement_value = st.number_input("當時土地公告現值（萬元）", value=1000)
    transfer_market_value = st.number_input("當時房屋市價（萬元）", value=3000)
    transfer_building_value = st.number_input("當時房屋評定現值（萬元）", value=200)

st.markdown("---")

st.markdown("### 💰 未來出售預估")
sale_price = st.number_input("未來出售價格（萬元）", value=3800)
sale_announcement_value = st.number_input("未來土地公告現值（萬元）", value=1300)
future_building_value = st.number_input("未來房屋評定現值（萬元）", value=250)
multiplier = st.number_input("政府公告調整倍率", value=3.0, step=0.1)
is_self_use = st.radio("是否為自用住宅？", ["是", "否"], index=0)

# 土地增值額
if registration_target == "父母" and transfer_plan == "留待繼承":
    increment_amount = (sale_announcement_value - transfer_announcement_value) * multiplier
    hold_years = child_hold_years
    land_note = f"子女繼承後重新起算，持有 {hold_years} 年"
else:
    increment_amount = (sale_announcement_value - land_current_value) * multiplier
    if registration_target == "父母" and transfer_plan == "未來贈與給子女":
        hold_years = child_hold_years
        land_note = f"贈與後起算，子女持有 {hold_years} 年"
    elif registration_target == "子女":
        hold_years = child_hold_years
        land_note = f"子女持有 {hold_years} 年"
    else:
        hold_years = 0
        land_note = "無法判斷持有年數"

# 土增稅
if is_self_use == "是" and hold_years >= 6:
    land_tax = increment_amount * 0.10
    land_tax_formula = f"{increment_amount:.1f} × 10%"
    land_note += "，自用住宅，適用10%稅率"
else:
    if increment_amount <= 400:
        land_tax = increment_amount * 0.20
        land_tax_formula = f"{increment_amount:.1f} × 20%"
    elif increment_amount <= 800:
        land_tax = 400 * 0.20 + (increment_amount - 400) * 0.30
        land_tax_formula = f"400 × 20% + ({increment_amount:.1f} - 400) × 30%"
    else:
        land_tax = 400 * 0.20 + 400 * 0.30 + (increment_amount - 800) * 0.40
        land_tax_formula = f"400 × 20% + 400 × 30% + ({increment_amount:.1f} - 800) × 40%"
    land_note += "，一般用地累進稅率20~40%"

# 契稅、贈與稅、遺產稅、印花稅
gift_tax = 0
gift_tax_formula = ""
inherit_tax = 0
inherit_tax_formula = ""
stamp_tax = sale_price * 0.001
stamp_tax_formula = f"{sale_price:.1f} × 0.1%"
deed_tax = sale_price * 0.06
deed_tax_formula = f"{sale_price:.1f} × 6%"

if registration_target == "父母" and transfer_plan == "未來贈與給子女":
    gift_base = transfer_announcement_value + transfer_building_value
    tax_exempt = 2444
    taxable_amount = max(0, gift_base - tax_exempt)
    if taxable_amount <= 256:
        gift_tax = taxable_amount * 0.10
    elif taxable_amount <= 512:
        gift_tax = 256 * 0.10 + (taxable_amount - 256) * 0.15
    else:
        gift_tax = 256 * 0.10 + 256 * 0.15 + (taxable_amount - 512) * 0.20
    gift_tax_formula = f"(公告值：{gift_base:.1f} - 免稅額：{tax_exempt}) → 應稅：{taxable_amount:.1f} 萬元"
elif registration_target == "父母" and transfer_plan == "留待繼承":
    estate_base = transfer_announcement_value + transfer_building_value
    basic_deduction = 1333 + 56 * 1 + 138 * 2
    taxable_amount = max(0, estate_base - basic_deduction)
    if taxable_amount <= 5000:
        inherit_tax = taxable_amount * 0.10
    elif taxable_amount <= 10000:
        inherit_tax = 5000 * 0.10 + (taxable_amount - 5000) * 0.15
    else:
        inherit_tax = 5000 * 0.10 + 5000 * 0.15 + (taxable_amount - 10000) * 0.20
    inherit_tax_formula = f"(公告值：{estate_base:.1f} - 扣除額：{basic_deduction}) → 應稅：{taxable_amount:.1f} 萬元"

# 房地合一稅計算邏輯
cost_basis = transfer_market_value
capital_gain = sale_price - cost_basis
if hold_years < 2:
    income_tax = capital_gain * 0.45
    income_tax_formula = f"({sale_price} - {cost_basis}) × 45%"
elif hold_years < 5:
    income_tax = capital_gain * 0.35
    income_tax_formula = f"({sale_price} - {cost_basis}) × 35%"
elif hold_years < 10:
    income_tax = capital_gain * 0.20
    income_tax_formula = f"({sale_price} - {cost_basis}) × 20%"
else:
    income_tax = capital_gain * 0.15
    income_tax_formula = f"({sale_price} - {cost_basis}) × 15%"

st.markdown("---")
st.markdown("### 📊 稅負試算總表")
st.write(f"📌 土地增值稅：約 **{land_tax:.1f} 萬元**（{land_note}）")
st.write(f"  計算式：{land_tax_formula}")
if gift_tax > 0:
    st.write(f"🎁 贈與稅：約 **{gift_tax:.1f} 萬元**（以公告值計算）")
    st.write(f"  計算式：{gift_tax_formula}")
if inherit_tax > 0:
    st.write(f"👪 遺產稅：約 **{inherit_tax:.1f} 萬元**（含法定扣除額）")
    st.write(f"  計算式：{inherit_tax_formula}")
st.write(f"📑 印花稅：約 **{stamp_tax:.1f} 萬元**（0.1%）")
st.write(f"  計算式：{stamp_tax_formula}")
st.write(f"📃 契稅：約 **{deed_tax:.1f} 萬元**（6%）")
st.write(f"  計算式：{deed_tax_formula}")
st.write(f"💼 房地合一稅：約 **{income_tax:.1f} 萬元**")
st.write(f"  計算式：{income_tax_formula}")

st.markdown("---")

# --- 聯絡資訊 ---
st.markdown("""
<div style='display: flex; justify-content: center; align-items: center; gap: 1.5em; font-size: 14px; color: gray;'>
  <a href='/' style='color:#006666; text-decoration: underline;'>《影響力》傳承策略平台</a>
  <a href='https://gracefo.com' target='_blank'>永傳家族辦公室</a>
  <a href='mailto:123@gracefo.com'>123@gracefo.com</a>
</div>
""", unsafe_allow_html=True)
