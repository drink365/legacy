# 以下是整合後完整、可執行的 Streamlit 程式碼，包含三種情境稅負計算：
# 1. 子女自行購屋
# 2. 父母贈與房產
# 3. 父母留待繼承
# 請將本程式貼上於 Streamlit 環境中執行

import streamlit as st

st.set_page_config(page_title="不動產稅負分析", layout="wide")
st.title("📊 不動產情境稅負分析工具")

# --- 基本資訊輸入 ---
scenario_label = st.selectbox("選擇情境", ["子女自行購屋", "父母贈與房產", "父母留待繼承"])

st.header("🏠 房屋與土地價格設定")
market_price = st.number_input("市價（萬元）", min_value=0.0, value=3000.0)
land_value = st.number_input("原始土地公告現值（萬元）", min_value=0.0, value=600.0)
house_value = st.number_input("原始房屋評定現值（萬元）", min_value=0.0, value=300.0)

if scenario_label == "父母贈與房產":
    gift_land_value = st.number_input("贈與時土地公告現值（萬元）", min_value=0.0, value=700.0)
    gift_house_value = st.number_input("贈與時房屋評定現值（萬元）", min_value=0.0, value=280.0)
elif scenario_label == "父母留待繼承":
    inherit_land_value = st.number_input("繼承時土地公告現值（萬元）", min_value=0.0, value=750.0)
    inherit_house_value = st.number_input("繼承時房屋評定現值（萬元）", min_value=0.0, value=250.0)

future_price = st.number_input("未來出售價格（萬元）", min_value=0.0, value=3600.0)
holding_years = st.number_input("持有年數", min_value=0, value=5)
is_self_use = st.checkbox("是否為自用住宅", value=True)

# --- 稅率與計算函數 ---
def calc_gift_tax(amount):
    deduction = 244
    taxable = max(amount - deduction, 0)
    if taxable <= 2811:
        return taxable * 0.10, f"({amount} - 244) × 10%"
    elif taxable <= 5621:
        return taxable * 0.15 - 140.55, f"({amount} - 244) × 15% - 140.55"
    else:
        return taxable * 0.20 - 421.6, f"({amount} - 244) × 20% - 421.6"

def calc_estate_tax(amount):
    deduction = 1333
    taxable = max(amount - deduction, 0)
    if taxable <= 5621:
        return taxable * 0.10, f"({amount} - 1333) × 10%"
    elif taxable <= 11242:
        return taxable * 0.15 - 281.05, f"({amount} - 1333) × 15% - 281.05"
    else:
        return taxable * 0.20 - 842.3, f"({amount} - 1333) × 20% - 842.3"

def calc_real_estate_tax(acquired_price, sell_price, holding_years, is_self_use):
    gain = sell_price - acquired_price
    if holding_years <= 2:
        return gain * 0.45, f"({sell_price} - {acquired_price}) × 45%"
    elif holding_years <= 5:
        return gain * 0.35, f"({sell_price} - {acquired_price}) × 35%"
    elif holding_years <= 10 and not is_self_use:
        return gain * 0.20, f"({sell_price} - {acquired_price}) × 20%"
    elif holding_years > 10 and not is_self_use:
        return gain * 0.15, f"({sell_price} - {acquired_price}) × 15%"
    elif holding_years > 6 and is_self_use:
        gain = max(gain - 400, 0)
        return gain * 0.10, f"({sell_price} - {acquired_price} - 400) × 10%"
    return gain * 0.35, f"({sell_price} - {acquired_price}) × 35%"

# --- 各稅試算 ---
st.header("📘 稅負彙整明細")

if scenario_label == "子女自行購屋":
    stamp_tax = market_price * 0.001
    contract_tax = house_value * 0.06
    land_tax = (future_price - land_value) * 0.2
    real_tax, real_formula = calc_real_estate_tax(market_price, future_price, holding_years, is_self_use)
    st.markdown("**🔹 子女自行購屋情境**")
    st.markdown(f"- 契稅：{contract_tax:.1f} 萬元\n- 印花稅：{stamp_tax:.1f} 萬元\n- 土地增值稅：{land_tax:.1f} 萬元\n- 房地合一稅：{real_tax:.1f} 萬元（{real_formula}）")

elif scenario_label == "父母贈與房產":
    parent_stamp = market_price * 0.001
    parent_contract = house_value * 0.06
    gift_val = gift_land_value + gift_house_value
    gift_tax, gift_formula = calc_gift_tax(gift_val)
    gift_stamp = gift_val * 0.001
    gift_contract = gift_house_value * 0.06
    gift_land_tax = (gift_land_value - land_value) * 0.2
    real_tax, real_formula = calc_real_estate_tax(gift_land_value + gift_house_value, future_price, holding_years, is_self_use)
    st.markdown("**🔹 父母贈與房產情境**")
    st.markdown(f"""
- 父母購屋：契稅 {parent_contract:.1f} 萬元、印花稅 {parent_stamp:.1f} 萬元
- 贈與階段：贈與稅 {gift_tax:.1f} 萬元（{gift_formula}）、印花稅 {gift_stamp:.1f} 萬元、契稅 {gift_contract:.1f} 萬元、土增稅 {gift_land_tax:.1f} 萬元
- 子女出售：房地合一稅 {real_tax:.1f} 萬元（{real_formula}）
    """)

elif scenario_label == "父母留待繼承":
    parent_stamp = market_price * 0.001
    parent_contract = house_value * 0.06
    estate_val = inherit_land_value + inherit_house_value
    estate_tax, estate_formula = calc_estate_tax(estate_val)
    real_tax, real_formula = calc_real_estate_tax(estate_val, future_price, holding_years, is_self_use)
    land_tax = (future_price - inherit_land_value) * 0.2
    st.markdown("**🔹 父母留待繼承情境**")
    st.markdown(f"""
- 父母購屋：契稅 {parent_contract:.1f} 萬元、印花稅 {parent_stamp:.1f} 萬元
- 繼承階段：遺產稅 {estate_tax:.1f} 萬元（{estate_formula}）
- 子女出售：土地增值稅 {land_tax:.1f} 萬元、房地合一稅 {real_tax:.1f} 萬元（{real_formula}）
    """)

st.markdown("---")
st.caption("《影響力》傳承策略平台｜永傳家族辦公室")
