import streamlit as st

# 頁面設定
st.set_page_config(page_title="不動產稅負評估工具", layout="wide")
st.title("🏠 不動產稅負評估工具")
st.markdown("請依序輸入資訊，系統將自動試算【買賣】【贈與】【繼承】下的不動產稅負。")

# 房屋與土地現況輸入
st.header("📌 房屋與土地現況")
current_price = st.number_input("市價（萬元）", min_value=0.0, value=3000.0)
current_land_value = st.number_input("土地公告現值（萬元）", min_value=0.0, value=1000.0)
current_house_value = st.number_input("房屋評定現值（萬元）", min_value=0.0, value=200.0)

# 持有人與資金來源
st.header("🏷️ 資產登記與資金來源")
owner = st.radio("目前登記在誰名下？", ["父母", "子女"])
transfer_type = ""
fund_source = ""
if owner == "父母":
    transfer_type = st.radio("將來打算如何移轉給子女？", ["留待繼承", "贈與房產"])
else:
    fund_source = st.radio("子女購屋資金來源為？", ["自行購屋", "父母贈與現金"])

# 贈與或繼承時的公告價與評定現值
gift_land_value = 0
gift_house_value = 0
if owner == "父母" and transfer_type in ["贈與房產", "留待繼承"]:
    st.header("🏠 贈與或繼承時的價格")
    gift_land_value = st.number_input("贈與或繼承時土地公告現值（萬元）", value=1100.0)
    gift_house_value = st.number_input("贈與或繼承時房屋評定現值（萬元）", value=190.0)

# 預估未來出售資訊
st.header("📈 未來出售資訊")
future_price = st.number_input("預估未來出售價格（萬元）", min_value=0.0, value=3800.0)
future_land_value = st.number_input("預估未來土地公告現值（萬元）", min_value=0.0, value=1200.0)
future_house_value = st.number_input("預估未來房屋評定現值（萬元）", min_value=0.0, value=180.0)

# 其他條件
st.header("⏳ 其他條件")
holding_years = st.number_input("子女持有年數", min_value=0, value=2)
is_self_use = st.checkbox("是否為自用住宅", value=False)

# 計算土地增值稅（僅適用贈與或買賣）
def calc_land_tax(origin, future, is_self_use):
    increased_value = future - origin
    if is_self_use:
        return increased_value * 0.10, f"{increased_value:.1f} × 10%"
    else:
        first = min(increased_value, 400)
        second = min(max(increased_value - 400, 0), 400)
        third = max(increased_value - 800, 0)
        tax = first*0.2 + second*0.3 + third*0.4
        formula = f"{first:.1f}×20% + {second:.1f}×30% + {third:.1f}×40%"
        return tax, formula

# 贈與與遺產稅級距
def calc_gift_tax(value):
    exempt = 244
    base = max(value - exempt, 0)
    if base <= 2811:
        return base * 0.10, f"({base:.1f})×10%"
    elif base <= 5621:
        return base * 0.15 - 140.55, f"({base:.1f})×15% - 140.55"
    else:
        return base * 0.20 - 421.6, f"({base:.1f})×20% - 421.6"

def calc_estate_tax(value):
    exempt = 1333
    base = max(value - exempt, 0)
    if base <= 5621:
        return base * 0.10, f"({base:.1f})×10%"
    elif base <= 11242:
        return base * 0.15 - 281.05, f"({base:.1f})×15% - 281.05"
    else:
        return base * 0.20 - 842.3, f"({base:.1f})×20% - 842.3"

# 房地合一稅率
def calc_real_estate_tax(acquired, sold, holding, is_self_use):
    gain = sold - acquired
    if holding <= 2:
        rate = 0.45
        tax = gain * rate
    elif holding <= 5:
        rate = 0.35
        tax = gain * rate
    elif holding > 6 and is_self_use:
        deduction = 400
        taxable = max(gain - deduction, 0)
        tax = taxable * 0.10
        rate = 0.10
    elif holding <= 10:
        rate = 0.20
        tax = gain * rate
    else:
        rate = 0.15
        tax = gain * rate
    return tax, f"({sold:.1f} - {acquired:.1f}) × {int(rate*100)}%"

# 建立稅負明細分類顯示
st.header("📊 稅負明細")

# 原始取得（子女自行購屋）
if owner == "子女" and fund_source == "自行購屋":
    acquisition = current_price
    land_tax, land_formula = calc_land_tax(current_land_value, future_land_value, is_self_use)
    real_tax, real_formula = calc_real_estate_tax(acquisition, future_price, holding_years, is_self_use)
    stamp_tax = current_price * 0.001
    contract_tax = current_house_value * 0.06
    st.subheader("📦 原始取得（自行購屋）稅負")
    st.markdown(f"""
📄 **印花稅（買方）**：{stamp_tax:.1f} 萬元  
📄 **契稅（買方）**：{contract_tax:.1f} 萬元  
📍 **土地增值稅（賣方）**：{land_tax:.1f} 萬元（{land_formula}）  
🏢 **房地合一稅（賣方）**：{real_tax:.1f} 萬元（{real_formula}）  
    """)

# 贈與房產
elif owner == "父母" and transfer_type == "贈與房產":
    land_tax, land_formula = calc_land_tax(current_land_value, future_land_value, is_self_use)
    gift_value = gift_land_value + gift_house_value
    gift_tax, gift_formula = calc_gift_tax(gift_value)
    stamp_tax = gift_value * 0.001
    contract_tax = gift_house_value * 0.06
    acquisition = gift_land_value + gift_house_value
    real_tax, real_formula = calc_real_estate_tax(acquisition, future_price, holding_years, is_self_use)
    st.subheader("🎁 贈與房產稅負")
    st.markdown(f"""
📍 **土地增值稅（由受贈人繳）**：{land_tax:.1f} 萬元（{land_formula}）  
📄 **印花稅（受贈人）**：{stamp_tax:.1f} 萬元  
📄 **契稅（受贈人）**：{contract_tax:.1f} 萬元  
💰 **贈與稅（贈與者）**：{gift_tax:.1f} 萬元（{gift_formula}）  
🏢 **房地合一稅（未來出售）**：{real_tax:.1f} 萬元（{real_formula}）  
    """)

# 繼承房產
elif owner == "父母" and transfer_type == "留待繼承":
    estate_value = gift_land_value + gift_house_value
    estate_tax, estate_formula = calc_estate_tax(estate_value)
    acquisition = gift_land_value + gift_house_value
    real_tax, real_formula = calc_real_estate_tax(acquisition, future_price, holding_years, is_self_use)
    st.subheader("🪦 繼承房產稅負")
    st.markdown(f"""
💰 **遺產稅（繼承者）**：{estate_tax:.1f} 萬元（{estate_formula}）  
🏢 **房地合一稅（未來出售）**：{real_tax:.1f} 萬元（{real_formula}）  
📌 **土地增值稅免繳、印花稅免繳、契稅免繳**  
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
