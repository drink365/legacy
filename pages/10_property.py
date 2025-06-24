import streamlit as st

# ------------------------------
# 計算函式定義
# ------------------------------

def calc_deed_tax(house_value):
    """
    契稅：以房屋評定現值的6%計算
    """
    rate = 0.06
    tax = house_value * rate
    formula = f"{house_value} * {rate}"
    return tax, formula


def calc_stamp_tax(house_value, land_value):
    """
    印花稅：房屋現值 + 土地現值 的 0.1%
    """
    rate = 0.001
    base = house_value + land_value
    tax = base * rate
    formula = f"({house_value} + {land_value}) * {rate}"
    return tax, formula


def calc_land_increment_tax(old_value, new_value, holding_years, is_self_use):
    """
    土地增值稅（參考財政部一般用地稅率速算表）：
    - 自用住宅：統一稅率10%
    - 買賣：依漲價比率分級並考慮持有年限減徵
      * 漲價比例 <100%：稅率20%
      * 100%≤漲價比例<200%：第二級税率與扣抵
      * 漲價比例≥200%：第三級税率與扣抵
    漲價比例 = (new_value - old_value) / old_value
    各級稅率和減徵表請參閱財政部資料
    """
    gain = max(new_value - old_value, 0)
    # 自用住宅優惠
    if is_self_use:
        rate = 0.10
        tax = gain * rate
        formula = f"{gain} * {rate}"
        return tax, formula
    # 計算漲價比例
    ratio = gain / old_value if old_value > 0 else float('inf')
    # 第一級
    if ratio < 1:
        rate = 0.20
        tax = gain * rate
        formula = f"{gain} * {rate}"
        return tax, formula
    # 第二級
    if ratio < 2:
        if holding_years <= 20:
            rate, b_rate = 0.30, 0.10
        elif holding_years <= 30:
            rate, b_rate = 0.28, 0.08
        elif holding_years <= 40:
            rate, b_rate = 0.27, 0.07
        else:
            rate, b_rate = 0.26, 0.06
        tax = gain * rate - old_value * b_rate
        formula = f"{gain} * {rate} - {old_value} * {b_rate}"
        tax = max(tax, 0)
        return tax, formula
    # 第三級
    if holding_years <= 20:
        rate, b_rate = 0.40, 0.30
    elif holding_years <= 30:
        rate, b_rate = 0.36, 0.24
    elif holding_years <= 40:
        rate, b_rate = 0.34, 0.21
    else:
        rate, b_rate = 0.32, 0.18
    tax = gain * rate - old_value * b_rate
    formula = f"{gain} * {rate} - {old_value} * {b_rate}"
    tax = max(tax, 0)
    return tax, formula


def calc_real_estate_tax(sell_price, cost, holding_years, is_self_use, is_resident):
    """房地合一稅計算...（同前）"""
    profit = max(sell_price - cost, 0)
    if not is_resident:
        rate = 0.45 if holding_years <= 2 else 0.35
        return profit * rate, f"{profit} * {rate}"
    if is_self_use and holding_years > 6:
        taxable = max(profit - 400, 0)
        rate = 0.10
        return taxable * rate, f"{taxable} * {rate}"
    if holding_years <= 2:
        rate = 0.45
    elif holding_years <= 5:
        rate = 0.35
    elif holding_years <= 10:
        rate = 0.20
    else:
        rate = 0.15
    return profit * rate, f"{profit} * {rate}"


def calc_progressive_tax(taxable, brackets):
    tax, remaining, lower = 0.0, taxable, 0
    parts = []
    for upper, rate in brackets:
        portion = max(min(remaining, upper - lower), 0)
        if portion <= 0:
            break
        tax += portion * rate
        parts.append(f"{portion} * {rate}")
        remaining -= portion
        lower = upper
    formula = " + ".join(parts) or "0"
    return tax, formula


def calc_gift_tax(value):
    exemption = 244
    taxable = max(value - exemption, 0)
    brackets = [(5000, 0.10), (10000, 0.15), (float('inf'), 0.20)]
    tax, formula = calc_progressive_tax(taxable, brackets)
    if taxable == 0:
        formula = f"0 (免稅額 {exemption} 萬元)"
    return tax, formula


def calc_estate_tax(value):
    exemption = 1333
    taxable = max(value - exemption, 0)
    brackets = [(5000, 0.10), (10000, 0.15), (float('inf'), 0.20)]
    tax, formula = calc_progressive_tax(taxable, brackets)
    if taxable == 0:
        formula = f"0 (免稅額 {exemption} 萬元)"
    return tax, formula

# ------------------------------
# Streamlit UI
# ------------------------------
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

# 贈與／繼承時公告價格
st.header("🎁 贈與／繼承時公告價格")
transfer_land_value = st.number_input("贈與／繼承時土地公告現值（萬元）", min_value=0.0, value=1100.0)
transfer_house_value = st.number_input("贈與／繼承時房屋評定現值（萬元）", min_value=0.0, value=180.0)

# 預估未來出售資料
st.header("📈 預估未來出售資料")
future_price = st.number_input("未來出售價格（萬元）", min_value=0.0, value=3800.0)
future_land_value = st.number_input("未來土地公告現值（萬元）", min_value=0.0, value=1200.0)
future_house_value = st.number_input("未來房屋評定現值（萬元）", min_value=0.0, value=190.0)

# 計算與顯示稅負
section1, section2, section3 = [], [], []
def add_tax(lbl, tax, fmt, container): container.append((lbl, tax, fmt))
# 取得時稅負
add_tax("契稅", *calc_deed_tax(current_house_value), section1)
add_tax("印花稅", *calc_stamp_tax(current_house_value, current_land_value), section1)
# 根據情境
if owner == "子女":
    if fund_source == "父母贈與現金":
        add_tax("贈與稅", *calc_gift_tax(buy_price), section2)
    add_tax("土地增值稅", *calc_land_increment_tax(current_land_value, future_land_value, holding_years, is_self_use), section3)
    add_tax("房地合一稅", *calc_real_estate_tax(future_price, buy_price, holding_years, is_self_use, is_resident), section3)
else:
    base = transfer_land_value + transfer_house_value
    if transfer_type == "贈與房產":
        add_tax("贈與稅", *calc_gift_tax(base), section2)
        add_tax("契稅(受贈人)", *calc_deed_tax(transfer_house_value), section2)
        add_tax("印花稅", *calc_stamp_tax(transfer_house_value, transfer_land_value), section2)
        add_tax("土地增值稅(受贈人)", *calc_land_increment_tax(current_land_value, transfer_land_value, holding_years, False), section2)
        add_tax("土地增值稅", *calc_land_increment_tax(transfer_land_value, future_land_value, holding_years, is_self_use), section3)
        add_tax("房地合一稅", *calc_real_estate_tax(future_price, base, holding_years, is_self_use, is_resident), section3)
    else:
        add_tax("遺產稅", *calc_estate_tax(base), section2)
        add_tax("土地增值稅", *calc_land_increment_tax(transfer_land_value, future_land_value, holding_years, False), section3)
        add_tax("房地合一稅", *calc_real_estate_tax(future_price, base, holding_years, is_self_use, is_resident), section3)
# 顯示明細
st.header("📋 稅負明細報告")
total = sum(x[1] for x in section1+section2+section3)
for title, sec in [("1️⃣ 取得時應繳稅負", section1),("2️⃣ 贈與或繼承時應繳稅負", section2),("3️⃣ 未來出售時應繳稅負", section3)]:
    if sec:
        st.subheader(title)
        for lbl, amt, fmt in sec:
            st.markdown(f"- **{lbl}**：{amt:.2f} 萬元（{fmt}）")
# 總稅負
st.markdown(f"## 💰 預估總稅負：**{total:.2f} 萬元**")
# 頁尾
st.markdown("---")
st.markdown("""
<div style='display:flex;justify-content:center;align-items:center;gap:1.5em;font-size:14px;color:gray;'>
  <a href='/' style='color:#006666;text-decoration:underline;'>《影響力》傳承策略平台</a>
  <a href='https://gracefo.com' target='_blank'>永傳家族辦公室</a>
  <a href='mailto:123@gracefo.com'>123@gracefo.com</a>
</div>
""",unsafe_allow_html=True)
