import streamlit as st

# 頁面設定
st.set_page_config(page_title="不動產稅負評估工具", layout="wide")
st.title("🏠 不動產稅負評估工具")

st.markdown("請依序輸入以下資訊，系統將自動試算買賣、贈與與繼承的各項稅負。")

# 🔹 房屋與土地資訊
st.header("📌 房屋與土地資訊")
current_price = st.number_input("市價（萬元）", min_value=0.0, value=3000.0)
current_land_value = st.number_input("土地公告現值（萬元）", min_value=0.0, value=1000.0)
current_house_value = st.number_input("房屋評定現值（萬元）", min_value=0.0, value=200.0)

# 🔹 資產登記與資金來源
st.header("🏷️ 資產登記與資金來源")
owner = st.radio("目前登記在誰名下？", ["父母", "子女"])

transfer_type = ""
fund_source = ""
if owner == "父母":
    transfer_type = st.radio("將來打算如何移轉給子女？", ["留待繼承", "贈與房產"])
else:
    fund_source = st.radio("子女購屋資金來源為？", ["自行購屋", "父母贈與現金"])

# 🔹 贈與／繼承時價格
if owner == "父母":
    st.header("🔄 贈與或繼承時的價格資訊")
    transfer_price = st.number_input("贈與／繼承時市價（萬元）", min_value=0.0, value=3200.0)
    transfer_land_value = st.number_input("贈與／繼承時土地公告現值（萬元）", min_value=0.0, value=1100.0)
    transfer_house_value = st.number_input("贈與／繼承時房屋評定現值（萬元）", min_value=0.0, value=220.0)
else:
    transfer_price = current_price
    transfer_land_value = current_land_value
    transfer_house_value = current_house_value

# 🔹 預估未來出售資訊
st.header("📈 預估未來出售資訊")
future_price = st.number_input("預估未來出售價格（萬元）", min_value=0.0, value=3800.0)
future_land_value = st.number_input("預估未來土地公告現值（萬元）", min_value=0.0, value=1200.0)
future_house_value = st.number_input("預估未來房屋評定現值（萬元）", min_value=0.0, value=250.0)

# 🔹 基本條件
st.header("⏳ 其他基本條件")
holding_years = st.number_input("子女持有年數", min_value=0, value=2)
is_self_use = st.checkbox("是否為自用住宅", value=False)

# ✅ 土地增值稅
increased_value = future_land_value - transfer_land_value
if is_self_use:
    land_increment_tax = increased_value * 0.10
    formula_land_tax = f"{increased_value:.1f} × 10%"
else:
    first = min(increased_value, 400)
    second = min(max(increased_value - 400, 0), 400)
    third = max(increased_value - 800, 0)
    land_increment_tax = first * 0.2 + second * 0.3 + third * 0.4
    formula_land_tax = f"{first:.1f}×20% + {second:.1f}×30% + {third:.1f}×40%"

# ✅ 印花稅與契稅（子女取得當下）
stamp_tax = transfer_price * 0.001
stamp_formula = f"{transfer_price:.1f} × 0.1%"

contract_tax = transfer_price * 0.06
contract_formula = f"{transfer_price:.1f} × 6%"

# === 房地合一稅試算 ===

# 情境判斷（設定取得成本）
if owner == "子女" and fund_source == "自行購屋":
    # 情境1：子女自行購屋
    acquisition_cost = current_price

elif owner == "父母" and transfer_type == "留待繼承":
    # 情境2：繼承取得，成本為繼承時公告價
    acquisition_cost = future_land_value + future_house_value

elif owner == "父母" and transfer_type == "贈與房產":
    # 情境3：贈與取得，成本為父母原始取得成本
    acquisition_cost = current_land_value + current_house_value

elif owner == "子女" and fund_source == "父母贈與現金":
    # 情境4：贈與現金購屋，成本為當初市價購買
    acquisition_cost = current_price

# 獲利計算
real_estate_gain = future_price - acquisition_cost

# 稅率與優惠邏輯
if holding_years <= 2:
    rate = 0.45
    real_estate_tax = real_estate_gain * rate
    real_estate_formula = f"({future_price:.1f} - {acquisition_cost:.1f}) × 45%"
elif holding_years <= 5:
    rate = 0.35
    real_estate_tax = real_estate_gain * rate
    real_estate_formula = f"({future_price:.1f} - {acquisition_cost:.1f}) × 35%"
elif holding_years <= 10:
    if is_self_use:
        if holding_years > 6 and real_estate_gain > 400:
            rate = 0.10
            taxable_gain = real_estate_gain - 400
            real_estate_tax = taxable_gain * rate
            real_estate_formula = f"({real_estate_gain:.1f} - 400) × 10%"
        elif holding_years > 6:
            real_estate_tax = 0.0
            real_estate_formula = f"({real_estate_gain:.1f} - 400) × 10% = 0"
        else:
            rate = 0.20
            real_estate_tax = real_estate_gain * rate
            real_estate_formula = f"({future_price:.1f} - {acquisition_cost:.1f}) × 20%"
    else:
        rate = 0.20
        real_estate_tax = real_estate_gain * rate
        real_estate_formula = f"({future_price:.1f} - {acquisition_cost:.1f}) × 20%"
else:
    if is_self_use and holding_years > 6:
        if real_estate_gain > 400:
            rate = 0.10
            taxable_gain = real_estate_gain - 400
            real_estate_tax = taxable_gain * rate
            real_estate_formula = f"({real_estate_gain:.1f} - 400) × 10%"
        else:
            real_estate_tax = 0.0
            real_estate_formula = f"({real_estate_gain:.1f} - 400) × 10% = 0"
    else:
        rate = 0.15
        real_estate_tax = real_estate_gain * rate
        real_estate_formula = f"({future_price:.1f} - {acquisition_cost:.1f}) × 15%"


# ✅ 贈與／遺產稅計算函數（含免稅額）
def calc_gift_tax(amount):
    base = max(amount - 244, 0)
    if base <= 2811:
        return base * 0.10, f"({amount:.1f}-244)×10%"
    elif base <= 5621:
        return base * 0.15 - 140.55, f"({amount:.1f}-244)×15%-140.55"
    else:
        return base * 0.20 - 421.6, f"({amount:.1f}-244)×20%-421.6"

def calc_estate_tax(amount):
    base = max(amount - 1333, 0)
    if base <= 5621:
        return base * 0.10, f"({amount:.1f}-1333)×10%"
    elif base <= 11242:
        return base * 0.15 - 281.05, f"({amount:.1f}-1333)×15%-281.05"
    else:
        return base * 0.20 - 842.3, f"({amount:.1f}-1333)×20%-842.3"

gift_tax = estate_tax = 0
gift_formula = estate_formula = ""

if owner == "父母":
    transfer_total = transfer_land_value + transfer_house_value
    if transfer_type == "贈與房產":
        gift_tax, gift_formula = calc_gift_tax(transfer_total)
    elif transfer_type == "留待繼承":
        estate_tax, estate_formula = calc_estate_tax(transfer_total)

# ✅ 稅負總表顯示
st.header("📊 稅負試算總表")
st.markdown(f"""
📌 **資產登記與資金來源**：{owner} → {transfer_type if owner == "父母" else fund_source}

📍 **土地增值稅**：約 **{land_increment_tax:.1f} 萬元**（{'自用10%' if is_self_use else '累進稅率20-40%'})
- 計算式：{formula_land_tax}

📄 **印花稅**：約 **{stamp_tax:.1f} 萬元**
- 計算式：{stamp_formula}

📄 **契稅**：約 **{contract_tax:.1f} 萬元**
- 計算式：{contract_formula}

🏢 **房地合一稅**：約 **{real_estate_tax:.1f} 萬元**
- 計算式：{real_estate_formula}
""")

if gift_tax:
    st.markdown(f"""
🎁 **贈與稅**：約 **{gift_tax:.1f} 萬元**
- 計算式：{gift_formula}
""")
if estate_tax:
    st.markdown(f"""
🪦 **遺產稅**：約 **{estate_tax:.1f} 萬元**
- 計算式：{estate_formula}
""")

# ✅ 總稅負
total_tax = land_increment_tax + stamp_tax + contract_tax + real_estate_tax + gift_tax + estate_tax
st.markdown(f"💰 **總稅負金額**：預估約 **{total_tax:.1f} 萬元**")

# 🔻 頁尾資訊
st.markdown("---")
st.markdown("""
<div style='display: flex; justify-content: center; align-items: center; gap: 1.5em; font-size: 14px; color: gray;'>
  <a href='/' style='color:#006666; text-decoration: underline;'>《影響力》傳承策略平台</a>
  <a href='https://gracefo.com' target='_blank'>永傳家族辦公室</a>
  <a href='mailto:123@gracefo.com'>123@gracefo.com</a>
</div>
""", unsafe_allow_html=True)
