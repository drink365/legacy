import streamlit as st

# 頁面設定
st.set_page_config(page_title="不動產稅負評估", layout="wide")

st.title("🏠 不動產稅負評估工具")
st.markdown("請依序輸入以下資訊，系統將自動試算買賣、贈與與繼承的各項稅負。")

# 房屋與土地資訊輸入
st.header("📌 房屋與土地資訊")
current_price = st.number_input("市價（萬元）", min_value=0.0, value=3000.0)
current_land_value = st.number_input("土地公告現值（萬元）", min_value=0.0, value=1000.0)
current_house_value = st.number_input("房屋評定現值（萬元）", min_value=0.0, value=200.0)

# 資產登記與資金來源
st.header("🏷️ 資產登記與資金來源")
owner = st.radio("目前登記在誰名下？", ["父母", "子女"])

transfer_type = ""
fund_source = ""
if owner == "父母":
    transfer_type = st.radio("將來打算如何移轉給子女？", ["留待繼承", "贈與房產"])
else:
    fund_source = st.radio("子女購屋資金來源為？", ["自行購屋", "父母贈與現金"])

# 繼承或贈與當時的價格（僅父母持有時顯示）
if owner == "父母":
    st.header("📂 贈與或繼承當時價格")
    transfer_market = st.number_input("移轉時市價（萬元）", min_value=0.0, value=3000.0)
    transfer_land_value = st.number_input("移轉時土地公告現值（萬元）", min_value=0.0, value=1000.0)
    transfer_house_value = st.number_input("移轉時房屋評定現值（萬元）", min_value=0.0, value=200.0)

# 預估未來出售資料
st.header("📈 預估未來出售資訊")
future_price = st.number_input("預估未來出售價格（萬元）", min_value=0.0, value=3800.0)
future_land_value = st.number_input("預估未來土地公告現值（萬元）", min_value=0.0, value=1200.0)
future_house_value = st.number_input("預估未來房屋評定現值（萬元）", min_value=0.0, value=250.0)

# 基本參數
st.header("⏳ 其他基本條件")
holding_years = st.number_input("子女持有年數", min_value=0, value=2)
is_self_use = st.checkbox("是否為自用住宅", value=False)

# 計算基礎設定
gift_exempt = 244  # 贈與免稅額
estate_exempt = 1333  # 遺產免稅額

# 土地增值稅
increased_value = future_land_value - current_land_value
if is_self_use:
    land_increment_tax = increased_value * 0.10
    formula_land_tax = f"{increased_value:.1f} × 10%"
else:
    first = min(increased_value, 400)
    second = min(max(increased_value - 400, 0), 400)
    third = max(increased_value - 800, 0)
    land_increment_tax = first * 0.2 + second * 0.3 + third * 0.4
    formula_land_tax = f"{first:.1f}×20% + {second:.1f}×30% + {third:.1f}×40%"

# 贈與稅與遺產稅
def calc_gift_tax(amount):
    net = max(amount - gift_exempt, 0)
    if net <= 2811:
        return net * 0.10, f"({amount:.1f} - 244) × 10%"
    elif net <= 5621:
        return net * 0.15 - 140.55, f"({amount:.1f} - 244) × 15% - 140.55"
    else:
        return net * 0.20 - 421.6, f"({amount:.1f} - 244) × 20% - 421.6"

def calc_estate_tax(amount):
    net = max(amount - estate_exempt, 0)
    if net <= 5621:
        return net * 0.10, f"({amount:.1f} - 1333) × 10%"
    elif net <= 11242:
        return net * 0.15 - 281.05, f"({amount:.1f} - 1333) × 15% - 281.05"
    else:
        return net * 0.20 - 842.3, f"({amount:.1f} - 1333) × 20% - 842.3"

gift_tax = estate_tax = 0
gift_formula = estate_formula = ""

if owner == "父母":
    transfer_value = transfer_land_value + transfer_house_value
    if transfer_type == "贈與房產":
        gift_tax, gift_formula = calc_gift_tax(transfer_value)
    elif transfer_type == "留待繼承":
        estate_tax, estate_formula = calc_estate_tax(transfer_value)

# 契稅與印花稅（繼承免除）
if owner == "父母" and transfer_type == "留待繼承":
    stamp_tax = 0.0
    contract_tax = 0.0
    stamp_formula = "繼承免印花稅"
    contract_formula = "繼承免契稅"
else:
    stamp_tax = future_price * 0.001
    stamp_formula = f"{future_price:.1f} × 0.1%"
    contract_tax = future_price * 0.06
    contract_formula = f"{future_price:.1f} × 6%"

# 房地合一稅計算
def calc_real_estate_tax(cost_basis):
    taxable_income = max(future_price - cost_basis, 0)
    if holding_years <= 2:
        rate = 0.45
        formula = f"({future_price:.1f} - {cost_basis:.1f}) × 45%"
    elif holding_years <= 5:
        rate = 0.35
        formula = f"({future_price:.1f} - {cost_basis:.1f}) × 35%"
    elif is_self_use and holding_years > 6:
        deduction = 400
        net = max(taxable_income - deduction, 0)
        tax = net * 0.10
        return tax, f"(({future_price:.1f} - {cost_basis:.1f}) - 400) × 10%"
    elif holding_years <= 10:
        rate = 0.20
        formula = f"({future_price:.1f} - {cost_basis:.1f}) × 20%"
    else:
        rate = 0.15
        formula = f"({future_price:.1f} - {cost_basis:.1f}) × 15%"
    return taxable_income * rate, formula

# 成本基礎計算邏輯
if owner == "子女":
    real_estate_cost = current_price  # 子女自購或受贈現金購屋，以市價為成本
elif owner == "父母" and transfer_type == "贈與房產":
    real_estate_cost = transfer_land_value + transfer_house_value
else:
    real_estate_cost = future_land_value + future_house_value  # 繼承視同從公告現值繼承

real_estate_tax, real_estate_formula = calc_real_estate_tax(real_estate_cost)

# 試算總表
st.header("📊 稅負試算總表")

# 條件摘要
st.markdown("### 💡 本次情境條件")
if owner == "父母":
    st.markdown(f"- 目前由父母持有，未來預計 **{transfer_type}**")
else:
    st.markdown(f"- 目前由子女持有，購屋資金來源為：**{fund_source}**")

# 各稅項列出
st.markdown(f"""
📍 **土地增值稅**：約 **{land_increment_tax:.1f} 萬元**（{'自用10%' if is_self_use else '一般20~40%'}）  
- 計算式：{formula_land_tax}

📄 **印花稅**：約 **{stamp_tax:.1f} 萬元**  
- 計算式：{stamp_formula}

📄 **契稅**：約 **{contract_tax:.1f} 萬元**  
- 計算式：{contract_formula}

🏢 **房地合一稅**：約 **{real_estate_tax:.1f} 萬元**  
- 計算式：{real_estate_formula}
""")

if gift_tax > 0:
    st.markdown(f"""
🎁 **贈與稅**：約 **{gift_tax:.1f} 萬元**  
- 計算式：{gift_formula}
""")

if estate_tax > 0:
    st.markdown(f"""
🪦 **遺產稅**：約 **{estate_tax:.1f} 萬元**  
- 計算式：{estate_formula}
""")

# 稅負總額
total_tax = land_increment_tax + stamp_tax + contract_tax + real_estate_tax + gift_tax + estate_tax
st.markdown(f"💰 **總稅負金額**：預估約 **{total_tax:.1f} 萬元**")

# 頁尾
st.markdown("---")
st.markdown("""
<div style='display: flex; justify-content: center; align-items: center; gap: 1.5em; font-size: 14px; color: gray;'>
  <a href='/' style='color:#006666; text-decoration: underline;'>《影響力》傳承策略平台</a>
  <a href='https://gracefo.com' target='_blank'>永傳家族辦公室</a>
  <a href='mailto:123@gracefo.com'>123@gracefo.com</a>
</div>
""", unsafe_allow_html=True)
