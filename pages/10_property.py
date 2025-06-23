import streamlit as st

st.set_page_config(page_title="不動產稅負評估工具", layout="wide")
st.title("🏠 不動產稅負評估工具")

st.markdown("請依序輸入以下資訊，系統將自動試算房地合一稅。")

# 房屋與土地資訊
st.header("📌 房屋與土地資訊")
current_price = st.number_input("目前市價（萬元）", min_value=0.0, value=3000.0)
current_land_value = st.number_input("目前土地公告現值（萬元）", min_value=0.0, value=1000.0)
current_house_value = st.number_input("目前房屋評定現值（萬元）", min_value=0.0, value=200.0)

# 登記與取得方式
st.header("🏷️ 資產登記與資金來源")
owner = st.radio("目前登記在誰名下？", ["父母", "子女"])

if owner == "父母":
    transfer_type = st.radio("未來將如何移轉？", ["留待繼承", "贈與房產"])
    if transfer_type == "贈與房產":
        gift_land_value = st.number_input("贈與時土地公告現值（萬元）", min_value=0.0, value=1000.0)
        gift_house_value = st.number_input("贈與時房屋評定現值（萬元）", min_value=0.0, value=200.0)
    elif transfer_type == "留待繼承":
        inherit_land_value = st.number_input("繼承時土地公告現值（萬元）", min_value=0.0, value=1000.0)
        inherit_house_value = st.number_input("繼承時房屋評定現值（萬元）", min_value=0.0, value=200.0)
else:
    fund_source = st.radio("子女購屋資金來源為？", ["自行購屋", "父母贈與現金"])

# 預估出售
st.header("📈 預估未來出售資訊")
future_price = st.number_input("預估未來出售價格（萬元）", min_value=0.0, value=3800.0)
future_land_value = st.number_input("預估未來土地公告現值（萬元）", min_value=0.0, value=1200.0)
years = st.number_input("持有年數", min_value=0, value=5)
is_self_use = st.checkbox("是否為自用住宅（符合條件）", value=False)

# 房屋折舊邏輯
depreciation_years = min(years, 10)
future_house_value = current_house_value * (1 - depreciation_years * 0.05)

# 計算成本基礎
if owner == "子女":
    cost_basis = current_price
elif transfer_type == "贈與房產":
    cost_basis = gift_land_value + gift_house_value
elif transfer_type == "留待繼承":
    cost_basis = inherit_land_value + inherit_house_value
else:
    cost_basis = 0

# 利潤與稅率邏輯
profit = future_price - cost_basis
deduction = 0
if years <= 2:
    tax_rate = 0.45
elif years <= 5:
    tax_rate = 0.35
elif years > 6 and is_self_use:
    tax_rate = 0.10
    deduction = 400
    profit = max(profit - deduction, 0)
elif years <= 10:
    tax_rate = 0.20
else:
    tax_rate = 0.15

real_estate_tax = profit * tax_rate

# 顯示試算
st.header("📊 房地合一稅試算結果")
st.markdown(f"""
- 成本基礎: {cost_basis:.1f} 萬元  
- 銷售價格: {future_price:.1f} 萬元  
- 獲利金額: {profit:.1f} 萬元  
- 稅率: {tax_rate * 100:.0f}%  
- 可扣除額: {deduction:.1f} 萬元  

💰 **預估房地合一稅：{real_estate_tax:.1f} 萬元**  
""")
