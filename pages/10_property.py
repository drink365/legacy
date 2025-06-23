import streamlit as st

# 頁面設定
st.set_page_config(page_title="不動產稅負評估工具", layout="wide")
st.title("🏠 不動產稅負評估工具")
st.markdown("請依序輸入以下資訊，系統將試算不動產贈與、繼承與出售的稅負。")

# 房屋與土地資訊輸入
st.header("📌 房屋與土地資訊")
market_price = st.number_input("市價（萬元）", min_value=0.0, value=3000.0)
land_value = st.number_input("土地公告現值（萬元）", min_value=0.0, value=1000.0)
house_value = st.number_input("房屋評定現值（萬元）", min_value=0.0, value=200.0)

# 資產登記與資金來源
st.header("🏷️ 資產登記與資金來源")
owner = st.radio("目前登記在誰名下？", ["父母", "子女"])

if owner == "父母":
    transfer_type = st.radio("未來預計如何移轉？", ["贈與", "留待繼承"])
else:
    fund_source = st.radio("子女購屋資金來源為？", ["自行購屋", "父母贈與現金"])

# 未來出售資訊
st.header("📈 預估未來出售資訊")
future_price = st.number_input("預估未來出售價格（萬元）", min_value=0.0, value=3600.0)
future_land_value = st.number_input("預估未來土地公告現值（萬元）", min_value=0.0, value=1300.0)

# 房屋折舊邏輯
depreciated_house_value = house_value * 0.9 if owner == "子女" else house_value * 0.8
future_house_value = st.number_input("預估未來房屋評定現值（萬元）", min_value=0.0, value=depreciated_house_value)

holding_years = st.number_input("子女持有年數", min_value=0, value=3)
is_self_use = st.checkbox("是否為自用住宅（本人或直系親屬設籍滿6年）", value=False)

# 契稅與印花稅
contract_tax = 0
stamp_tax = 0
if owner == "子女" or (owner == "父母" and transfer_type == "贈與"):
    contract_tax = house_value * 0.06
    stamp_tax = market_price * 0.001

# 贈與稅與遺產稅
def gift_tax_calc(amount):
    exempt = 244
    taxable = max(0, amount - exempt)
    if taxable <= 2811:
        return taxable * 0.1
    elif taxable <= 5621:
        return taxable * 0.15 - 140.55
    else:
        return taxable * 0.2 - 421.6

def estate_tax_calc(amount):
    exempt = 1333
    taxable = max(0, amount - exempt)
    if taxable <= 5621:
        return taxable * 0.1
    elif taxable <= 11242:
        return taxable * 0.15 - 281.05
    else:
        return taxable * 0.2 - 842.3

gift_tax = 0
estate_tax = 0
if owner == "父母":
    if transfer_type == "贈與":
        gift_tax = gift_tax_calc(land_value + house_value)
    else:
        estate_tax = estate_tax_calc(land_value + house_value)

# 土增稅
land_base = land_value
if owner == "父母" and transfer_type == "留待繼承":
    land_base = future_land_value
land_gain = future_land_value - land_base
if is_self_use:
    land_tax = land_gain * 0.1
else:
    first = min(land_gain, 400)
    second = min(max(land_gain - 400, 0), 400)
    third = max(land_gain - 800, 0)
    land_tax = first * 0.2 + second * 0.3 + third * 0.4

# 房地合一稅
deduction = 0
if owner == "子女":
    cost = market_price
elif owner == "父母" and transfer_type == "贈與":
    cost = land_value + house_value
else:
    cost = future_land_value + future_house_value
tax_base = future_price - cost
rate = 0.35
if holding_years <= 2:
    rate = 0.45
elif holding_years <= 5:
    rate = 0.35
elif is_self_use and holding_years > 6:
    deduction = 400
    tax_base = max(0, tax_base - deduction)
    rate = 0.1
elif holding_years <= 10:
    rate = 0.2
else:
    rate = 0.15
real_estate_tax = tax_base * rate

# 顯示結果
st.header("📊 稅負試算總表")
st.markdown(f"""
### ➤ 資產登記與資金來源：
- 登記人：**{owner}**
{"- 移轉方式：**" + transfer_type + "**" if owner == "父母" else "- 資金來源：**" + fund_source + "**"}

---

📄 **契稅**：{contract_tax:.1f} 萬元  
📄 **印花稅**：{stamp_tax:.1f} 萬元  
🎁 **贈與稅**：{gift_tax:.1f} 萬元  
🪦 **遺產稅**：{estate_tax:.1f} 萬元  
🌱 **土地增值稅**：{land_tax:.1f} 萬元  
🏠 **房地合一稅**：{real_estate_tax:.1f} 萬元（稅率：{rate*100:.0f}%，扣除額：{deduction:.1f} 萬）

---

💰 **總稅負**：{(contract_tax + stamp_tax + gift_tax + estate_tax + land_tax + real_estate_tax):.1f} 萬元
""")

# 頁尾
st.markdown("---")
st.markdown("""
<div style='text-align:center; font-size: 14px; color: gray;'>
《影響力》傳承策略平台｜永傳家族辦公室  
<a href='https://gracefo.com' target='_blank'>gracefo.com</a> ｜ 聯絡信箱：123@gracefo.com
</div>
""", unsafe_allow_html=True)
