import streamlit as st

# 計算函式定義
# 契稅：6%
def calc_deed_tax(house_value):
    rate = 0.06
    tax = house_value * rate
    formula = f"{house_value} * {rate}"
    return tax, formula

# 印花稅：房屋現值+土地現值 的0.1%
def calc_stamp_tax(house_value, land_value):
    rate = 0.001
    base = house_value + land_value
    tax = base * rate
    formula = f"({house_value} + {land_value}) * {rate}"
    return tax, formula

# 土地增值稅：增值部分*20%
def calc_land_increment_tax(old_value, new_value):
    gain = max(new_value - old_value, 0)
    rate = 0.20
    tax = gain * rate
    formula = f"({new_value} - {old_value}) * {rate}"
    return tax, formula

# 房地合一稅計算
def calc_real_estate_tax(sell_price, cost, holding_years, is_self_use, is_resident):
    profit = max(sell_price - cost, 0)
    if not is_resident:
        rate = 0.45 if holding_years <= 2 else 0.35
        return profit * rate, f"({sell_price} - {cost}) * {rate}"
    if is_self_use and holding_years > 6:
        taxable = max(profit - 400, 0)
        rate = 0.10
        return taxable * rate, f"({sell_price} - {cost} - 400) * {rate}"
    if holding_years <= 2:
        rate = 0.45
    elif holding_years <= 5:
        rate = 0.35
    elif holding_years <= 10:
        rate = 0.20
    else:
        rate = 0.15
    return profit * rate, f"({sell_price} - {cost}) * {rate}"

# 通用累進稅率函式
def calc_progressive_tax(taxable, brackets):
    tax = 0.0
    remaining = taxable
    lower = 0
    parts = []
    for upper, rate in brackets:
        portion = max(min(remaining, upper - lower), 0)
        if portion <= 0:
            break
        tax += portion * rate
        parts.append(f"({portion} * {rate})")
        remaining -= portion
        lower = upper
    formula = " + ".join(parts) if parts else "0"
    return tax, formula

# 贈與稅：免稅244萬後，累進稅率10/15/20
def calc_gift_tax(value):
    exemption = 244
    taxable = max(value - exemption, 0)
    brackets = [(5000, 0.10), (10000, 0.15), (float('inf'), 0.20)]
    tax, formula = calc_progressive_tax(taxable, brackets)
    if taxable == 0:
        formula = f"0 (免稅額: {exemption} 萬元)"
    return tax, formula

# 遺產稅：免稅1333萬後，累進稅率10/15/20
def calc_estate_tax(value):
    exemption = 1333
    taxable = max(value - exemption, 0)
    brackets = [(5000, 0.10), (10000, 0.15), (float('inf'), 0.20)]
    tax, formula = calc_progressive_tax(taxable, brackets)
    if taxable == 0:
        formula = f"0 (免稅額: {exemption} 萬元)"
    return tax, formula

# Streamlit UI
st.set_page_config(page_title="不動產稅負評估工具", layout="wide")
st.title("🏠 不動產稅負評估工具")
st.markdown("根據不同取得方式與出售情境，評估整體稅負。")

# 資產登記與資金來源
st.header("🏷️ 資產登記與資金來源")
owner = st.radio("目前房產登記在誰名下？", ["父母", "子女"])
if owner == "父母":
    transfer_type = st.radio("將來如何移轉給子女？", ["留待繼承", "贈與房產"])
else:
    fund_source = st.radio("子女資金來源為？", ["自行購屋", "父母贈與現金"])

# 基本條件
st.header("⏳ 基本條件")
holding_years = st.number_input("子女持有年數", min_value=0, value=2)
is_self_use = st.checkbox("是否符合自用住宅條件", value=False)
is_resident = st.checkbox("是否為境內居住者", value=True)

# 買進的房產資訊
st.header("📌 買進的房產資訊")
buy_price = st.number_input("買進總價（萬元）", min_value=0.0, value=3000.0)
current_land_value = st.number_input("土地公告現值（萬元）", min_value=0.0, value=1000.0)
current_house_value = st.number_input("房屋評定現值（萬元）", min_value=0.0, value=200.0)

# 贈與／繼承時的公告價格
st.header("🎁 贈與／繼承時的公告價格")
transfer_land_value = st.number_input("贈與/繼承時土地公告現值（萬元）", min_value=0.0, value=1100.0)
transfer_house_value = st.number_input("贈與/繼承時房屋評定現值（萬元）", min_value=0.0, value=180.0)

# 預估未來出售資料
st.header("📈 預估未來出售資料")
future_price = st.number_input("未來出售價格（萬元）", min_value=0.0, value=3800.0)
future_land_value = st.number_input("未來土地公告現值（萬元）", min_value=0.0, value=1200.0)
future_house_value = st.number_input("未來房屋評定現值（萬元）", min_value=0.0, value=190.0)

# 計算稅負
section1 = []
section2 = []
section3 = []

def add_taxes(label, tax, formula, target):
    target.append((label, tax, formula))

# Section1: 取得時
deed, f1 = calc_deed_tax(current_house_value)
stamp, f2 = calc_stamp_tax(current_house_value, current_land_value)
add_taxes("契稅", deed, f1, section1)
add_taxes("印花稅", stamp, f2, section1)

# Section2 & 3
if owner == "子女":
    if fund_source == "父母贈與現金":
        tax, f = calc_gift_tax(buy_price)
        add_taxes("贈與稅", tax, f, section2)
    ltax, lf = calc_land_increment_tax(current_land_value, future_land_value)
    rtax, rf = calc_real_estate_tax(future_price, buy_price, holding_years, is_self_use, is_resident)
    add_taxes("土地增值稅", ltax, lf, section3)
    add_taxes("房地合一稅", rtax, rf, section3)
else:
    base = transfer_land_value + transfer_house_value
    if transfer_type == "贈與房產":
        gt, gf = calc_gift_tax(base)
        add_taxes("贈與稅", gt, gf, section2)
        dt, df = calc_deed_tax(transfer_house_value)
        add_taxes("契稅(受贈人)", dt, df, section2)
        stp, sf = calc_stamp_tax(transfer_house_value, transfer_land_value)
        add_taxes("印花稅", stp, sf, section2)
        lt, lf = calc_land_increment_tax(current_land_value, transfer_land_value)
        add_taxes("土地增值稅(受贈人)", lt, lf, section2)
        lt3, lf3 = calc_land_increment_tax(transfer_land_value, future_land_value)
        rt3, rf3 = calc_real_estate_tax(future_price, base, holding_years, is_self_use, is_resident)
        add_taxes("土地增值稅", lt3, lf3, section3)
        add_taxes("房地合一稅", rt3, rf3, section3)
    else:
        et, ef = calc_estate_tax(base)
        add_taxes("遺產稅", et, ef, section2)
        lt3, lf3 = calc_land_increment_tax(transfer_land_value, future_land_value)
        rt3, rf3 = calc_real_estate_tax(future_price, base, holding_years, is_self_use, is_resident)
        add_taxes("土地增值稅", lt3, lf3, section3)
        add_taxes("房地合一稅", rt3, rf3, section3)

# 顯示
st.header("📋 稅負明細報告")
total = 0
for title, datas in [("1️⃣ 取得時應繳稅負", section1), ("2️⃣ 贈與或繼承時應繳稅負", section2), ("3️⃣ 未來出售時應繳稅負", section3)]:
    if datas:
        st.subheader(title)
        for lbl, amt, frm in datas:
            st.markdown(f"- **{lbl}**: {amt:.2f} 萬元 ({frm})")
            total += amt
st.markdown(f"## 💰 預估總稅負: **{total:.2f} 萬元**")

# 頁尾
st.markdown("---")
st.markdown(
    """
    <div style='display: flex; justify-content: center; align-items: center; gap: 1.5em; font-size: 14px; color: gray;'>
      <a href='/' style='color: #006666; text-decoration: underline;'>《影響力》傳承策略平台</a>
      <a href='https://gracefo.com' target='_blank'>永傳家族辦公室</a>
      <a href='mailto:123@gracefo.com'>123@gracefo.com</a>
    </div>
    """,
    unsafe_allow_html=True
)
