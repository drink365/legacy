import streamlit as st

st.set_page_config(page_title="不動產稅負評估工具", layout="wide")
st.title("🏠 不動產稅負評估工具")

# 房屋與土地資訊
st.header("📌 房屋與土地資訊")
current_price = st.number_input("市價（萬元）", min_value=0.0, value=3000.0)
current_land_value = st.number_input("土地公告現值（萬元）", min_value=0.0, value=1000.0)
current_house_value = st.number_input("房屋評定現值（萬元）", min_value=0.0, value=200.0)

# 登記與移轉
st.header("🏷️ 資產登記與資金來源")
owner = st.radio("目前登記在誰名下？", ["父母", "子女"])
transfer_type, fund_source = "", ""
if owner == "父母":
    transfer_type = st.radio("將來打算如何移轉給子女？", ["留待繼承", "贈與房產"])
else:
    fund_source = st.radio("子女購屋資金來源為？", ["自行購屋", "父母贈與現金"])

# 出售資訊
st.header("📈 預估未來出售資訊")
future_price = st.number_input("預估未來出售價格（萬元）", value=3800.0)
future_land_value = st.number_input("未來土地公告現值（萬元）", value=1200.0)
future_house_value = st.number_input("未來房屋評定現值（萬元）", value=180.0)

# 基本條件
st.header("⏳ 基本條件")
holding_years = st.number_input("子女持有年數", min_value=0, value=2)
is_self_use = st.checkbox("是否為自用住宅（滿6年）", value=False)

# 贈與／繼承時的價格
gift_land_value = st.number_input("贈與或繼承時土地公告現值（萬元）", value=1100.0)
gift_house_value = st.number_input("贈與或繼承時房屋評定現值（萬元）", value=190.0)

# 計算稅負
def calc_gift_tax(total):
    taxable = max(total - 244, 0)
    if taxable <= 2811:
        return taxable * 0.10
    elif taxable <= 5621:
        return taxable * 0.15 - 140.55
    else:
        return taxable * 0.20 - 421.6

def calc_estate_tax(total):
    taxable = max(total - 1333, 0)
    if taxable <= 5621:
        return taxable * 0.10
    elif taxable <= 11242:
        return taxable * 0.15 - 281.05
    else:
        return taxable * 0.20 - 842.3

def calc_land_tax(start, end, self_use):
    diff = end - start
    if diff <= 0:
        return 0
    if self_use:
        return diff * 0.10
    first = min(diff, 400)
    second = min(max(diff - 400, 0), 400)
    third = max(diff - 800, 0)
    return first * 0.2 + second * 0.3 + third * 0.4

def calc_real_estate_tax(cost, self_use, years):
    gain = future_price - cost
    if years <= 2:
        return gain * 0.45
    elif years <= 5:
        return gain * 0.35
    elif years > 6 and self_use:
        return max((gain - 400), 0) * 0.10
    elif years <= 10:
        return gain * 0.20
    else:
        return gain * 0.15

# 預設取得成本
if owner == "子女" and fund_source == "自行購屋":
    acquisition_cost = current_price
elif owner == "父母" and transfer_type in ["贈與房產", "留待繼承"]:
    acquisition_cost = gift_land_value + gift_house_value
else:
    acquisition_cost = current_land_value + current_house_value

# 稅試算
land_tax = calc_land_tax(current_land_value, future_land_value, is_self_use)
real_estate_tax = calc_real_estate_tax(acquisition_cost, is_self_use, holding_years)
contract_tax = gift_house_value * 0.06
stamp_tax = (gift_land_value + gift_house_value) * 0.001
gift_total = gift_land_value + gift_house_value
gift_tax = calc_gift_tax(gift_total)
estate_tax = calc_estate_tax(gift_total)

# 顯示明細
st.header("📊 稅負明細")

if owner == "子女":
    st.subheader("📘 原始取得稅負")
    st.markdown(f"- 印花稅：{stamp_tax:.1f} 萬元")
    st.markdown(f"- 契稅：{contract_tax:.1f} 萬元")

if owner == "父母" and transfer_type == "贈與房產":
    st.subheader("🎁 贈與稅負")
    st.markdown(f"- 贈與稅：{gift_tax:.1f} 萬元")
    st.markdown(f"- 土地增值稅（受贈人繳）：{land_tax:.1f} 萬元")
    st.markdown(f"- 印花稅（受贈人繳）：{stamp_tax:.1f} 萬元")
    st.markdown(f"- 契稅（受贈人繳）：{contract_tax:.1f} 萬元")

if owner == "父母" and transfer_type == "留待繼承":
    st.subheader("🪦 繼承稅負")
    st.markdown(f"- 遺產稅：{estate_tax:.1f} 萬元")
    st.markdown("- 土地增值稅：免稅")
    st.markdown("- 印花稅與契稅：免稅")

st.subheader("🏠 最終出售稅負")
st.markdown(f"- 房地合一稅：{real_estate_tax:.1f} 萬元")
if not (owner == "父母" and transfer_type == "留待繼承"):
    st.markdown(f"- 土地增值稅：{land_tax:.1f} 萬元")

# 總稅負
st.header("💰 稅負總結")
total = real_estate_tax
if owner == "父母" and transfer_type == "贈與房產":
    total += gift_tax + land_tax + contract_tax + stamp_tax
elif owner == "父母" and transfer_type == "留待繼承":
    total += estate_tax
elif owner == "子女":
    total += contract_tax + stamp_tax + land_tax

st.markdown(f"👉 總稅負約為：**{total:.1f} 萬元**")
