import streamlit as st

# 頁面設定
st.set_page_config(page_title="不動產稅負評估", layout="wide")
st.title("🏠 不動產稅負評估工具")
st.markdown("請依序輸入以下資訊，系統將自動試算買賣、贈與與繼承的各項稅負。")

# 房屋與土地資訊輸入
st.header("📌 房屋與土地資訊")
current_price = st.number_input("現值｜市價（萬元）", min_value=0.0, value=3000.0, key="cur_price")
current_land_value = st.number_input("現值｜土地公告現值（萬元）", min_value=0.0, value=1000.0, key="cur_land")
current_house_value = st.number_input("現值｜房屋評定現值（萬元）", min_value=0.0, value=200.0, key="cur_house")

# 資產登記與資金來源
st.header("🏷️ 資產登記與資金來源")
owner = st.radio("目前登記在誰名下？", ["父母", "子女"], key="owner_select")

transfer_type = ""
fund_source = ""
if owner == "父母":
    transfer_type = st.radio("將來打算如何移轉給子女？", ["留待繼承", "贈與房產"], key="transfer_type")
    context_summary = f"目前資產登記在【父母】名下，預計未來以【{transfer_type}】方式移轉。"
else:
    fund_source = st.radio("子女購屋資金來源為？", ["自行購屋", "父母贈與現金"], key="fund_source")
    context_summary = f"目前資產已登記在【子女】名下，購屋資金來源為【{fund_source}】。"

# 贈與／繼承當下的三種價格（若父母持有）
gift_price = gift_land = gift_house = 0.0
if owner == "父母":
    st.header("🎁 贈與或繼承時的價格")
    gift_price = st.number_input("贈與或繼承時的市價（萬元）", min_value=0.0, value=3000.0, key="gift_price")
    gift_land = st.number_input("贈與或繼承時的土地公告現值（萬元）", min_value=0.0, value=1000.0, key="gift_land")
    gift_house = st.number_input("贈與或繼承時的房屋評定現值（萬元）", min_value=0.0, value=200.0, key="gift_house")

# 預估未來出售資料
st.header("📈 預估未來出售資訊")
future_price = st.number_input("預估未來出售價格（萬元）", min_value=0.0, value=3800.0, key="future_price")
future_land_value = st.number_input("預估未來土地公告現值（萬元）", min_value=0.0, value=1200.0, key="future_land")
future_house_value = st.number_input("預估未來房屋評定現值（萬元）", min_value=0.0, value=250.0, key="future_house")

# 基本參數
st.header("⏳ 其他基本條件")
holding_years = st.number_input("子女持有年數", min_value=0, value=2, key="holding_year")
is_self_use = st.checkbox("是否為自用住宅", value=False, key="self_use")

# --------- 試算邏輯定義 ---------
def calc_gift_tax(amount):
    amount -= 244  # 贈與免稅額
    if amount <= 0:
        return 0, "未超過244萬免稅額"
    if amount <= 2811:
        return amount * 0.10, f"({amount:.1f}) × 10%"
    elif amount <= 5621:
        return amount * 0.15 - 140.55, f"({amount:.1f}) × 15% - 140.55"
    else:
        return amount * 0.20 - 421.6, f"({amount:.1f}) × 20% - 421.6"

def calc_estate_tax(amount):
    amount -= 1333  # 遺產免稅額
    if amount <= 0:
        return 0, "未超過1333萬免稅額"
    if amount <= 5621:
        return amount * 0.10, f"({amount:.1f}) × 10%"
    elif amount <= 11242:
        return amount * 0.15 - 281.05, f"({amount:.1f}) × 15% - 281.05"
    else:
        return amount * 0.20 - 842.3, f"({amount:.1f}) × 20% - 842.3"

def calc_land_tax(start, end, self_use=False):
    increase = end - start
    if self_use:
        return increase * 0.10, f"{increase:.1f} × 10%"
    first = min(increase, 400)
    second = min(max(increase - 400, 0), 400)
    third = max(increase - 800, 0)
    total = first * 0.2 + second * 0.3 + third * 0.4
    return total, f"{first:.1f}×20% + {second:.1f}×30% + {third:.1f}×40%"

# --------- 計算區 ---------
gift_tax = estate_tax = land_tax = stamp_tax = contract_tax = realty_tax = 0
gift_formula = estate_formula = land_formula = stamp_formula = contract_formula = realty_formula = ""

# 成本以取得時價格為準
if owner == "子女":
    cost = current_land_value + current_house_value
elif transfer_type == "贈與房產":
    cost = gift_land + gift_house
elif transfer_type == "留待繼承":
    cost = gift_land + gift_house
else:
    cost = 0

# 土地增值稅
if owner == "父母" and transfer_type == "留待繼承":
    land_tax, land_formula = calc_land_tax(gift_land, future_land_value, is_self_use)
else:
    land_tax, land_formula = calc_land_tax(current_land_value, future_land_value, is_self_use)

# 房地合一稅
profit = future_price - cost
realty_tax = profit * 0.35
realty_formula = f"({future_price:.1f} - {cost:.1f}) × 35%"

# 印花稅與契稅
stamp_tax = future_price * 0.001
stamp_formula = f"{future_price:.1f} × 0.1%"

contract_tax = future_price * 0.06
contract_formula = f"{future_price:.1f} × 6%"

# 贈與稅或遺產稅
if owner == "父母":
    total_value = gift_land + gift_house
    if transfer_type == "贈與房產":
        gift_tax, gift_formula = calc_gift_tax(total_value)
    elif transfer_type == "留待繼承":
        estate_tax, estate_formula = calc_estate_tax(total_value)

# --------- 顯示區 ---------
total_tax = land_tax + realty_tax + stamp_tax + contract_tax + gift_tax + estate_tax

st.markdown("### 📘 資產背景條件")
st.info(context_summary)

st.markdown(f"""
### 💰 總稅負：約 **{total_tax:.1f} 萬元**

📍 **土地增值稅**：{land_tax:.1f} 萬元  
- 計算式：{land_formula}

🏢 **房地合一稅**：{realty_tax:.1f} 萬元  
- 計算式：{realty_formula}

📄 **印花稅**：{stamp_tax:.1f} 萬元  
- 計算式：{stamp_formula}

📄 **契稅**：{contract_tax:.1f} 萬元  
- 計算式：{contract_formula}
""")

if gift_tax:
    st.markdown(f"""
🎁 **贈與稅**：{gift_tax:.1f} 萬元  
- 計算式：{gift_formula}
""")

if estate_tax:
    st.markdown(f"""
🪦 **遺產稅**：{estate_tax:.1f} 萬元  
- 計算式：{estate_formula}
""")

# 頁尾
st.markdown("---")
st.markdown("""
<div style='display: flex; justify-content: center; align-items: center; gap: 1.5em; font-size: 14px; color: gray;'>
  <a href='/' style='color:#006666; text-decoration: underline;'>《影響力》傳承策略平台</a>
  <a href='https://gracefo.com' target='_blank'>永傳家族辦公室</a>
  <a href='mailto:123@gracefo.com'>123@gracefo.com</a>
</div>
""", unsafe_allow_html=True)
