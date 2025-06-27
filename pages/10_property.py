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
    土地增值稅：自用住宅統一稅率10%；買賣按漲價比例分級並考慮持有年限減徵
    """
    gain = max(new_value - old_value, 0)
    if is_self_use:
        rate = 0.10
        tax = gain * rate
        formula = f"{gain} * {rate}"
        return tax, formula
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
        return max(tax, 0), formula
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
    return max(tax, 0), formula


def calc_real_estate_tax(sell_price, cost, holding_years, is_self_use, is_resident):
    """
    房地合一稅計算
    """
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
st.markdown("根據不同取得與移轉方式，快速比較三種情境的稅負。")

# 選擇情境
scenario = st.selectbox(
    "請選擇分析情境",
    [
        "情境1：父母買進→繼承→子女出售",
        "情境2：父母買進→贈與→子女出售",
        "情境3：父母贈與現金→子女買進→子女出售"
    ]
)

# 主要輸入
st.header("📌 主要金額與條件")
buy_price      = st.number_input("一開始買進總價（萬元）", value=3000.0)
transfer_price = st.number_input("移轉時公告總價（萬元）", value=1800.0)
sell_price     = st.number_input("未來出售價格（萬元）", value=3800.0)

holding_years = st.number_input("子女持有年數", min_value=0, value=2)
is_self_use   = st.checkbox("是否符合自用住宅條件", value=False)
is_resident   = st.checkbox("是否為境內居住者", value=True)

# 稅負容器
section1, section2, section3 = [], [], []

def add_acquisition_taxes(container):
    # 契稅
    tax, fmt = calc_deed_tax(buy_price)
    container.append(("契稅", tax, fmt))
    # 印花稅（假設房屋/土地各半）
    house_v = buy_price * 0.5
    land_v  = buy_price * 0.5
    tax, fmt = calc_stamp_tax(house_v, land_v)
    container.append(("印花稅", tax, fmt))


def add_inheritance_taxes(container):
    tax, fmt = calc_estate_tax(transfer_price)
    container.append(("遺產稅", tax, fmt))


def add_property_gift_taxes(container):
    tax, fmt = calc_gift_tax(transfer_price)
    container.append(("贈與稅", tax, fmt))


def add_cash_gift_taxes(container):
    tax, fmt = calc_gift_tax(buy_price)
    container.append(("贈與（現金）稅", tax, fmt))


def add_sale_taxes(container, cost_basis):
    # 土地增值稅
    old_land = cost_basis * 0.5
    new_land = sell_price    * 0.5
    tax, fmt = calc_land_increment_tax(old_land, new_land, holding_years, is_self_use)
    container.append(("土地增值稅", tax, fmt))
    # 房地合一稅
    tax, fmt = calc_real_estate_tax(sell_price, cost_basis, holding_years, is_self_use, is_resident)
    container.append(("房地合一稅", tax, fmt))

# 根據選擇的情境組裝稅負
if scenario.startswith("情境1"):
    add_acquisition_taxes(section1)
    add_inheritance_taxes(section2)
    add_sale_taxes(section3, cost_basis=transfer_price)
elif scenario.startswith("情境2"):
    add_acquisition_taxes(section1)
    add_property_gift_taxes(section2)
    add_sale_taxes(section3, cost_basis=transfer_price)
else:
    add_cash_gift_taxes(section1)
    add_acquisition_taxes(section1)
    add_sale_taxes(section3, cost_basis=buy_price)

# 顯示明細
st.header("📋 稅負明細報告")
totals = []
for title, sec in [("1️⃣ 取得時稅負", section1), ("2️⃣ 移轉時稅負", section2), ("3️⃣ 出售時稅負", section3)]:
    if sec:
        st.subheader(title)
        subtotal = 0
        for lbl, amt, fmt in sec:
            st.markdown(f"- **{lbl}**：{amt:.2f} 萬元（{fmt}）")
            subtotal += amt
        st.markdown(f"**小計：{subtotal:.2f} 萬元**")
        totals.append(subtotal)

# 總稅負
total_tax = sum(totals)
st.markdown(f"## 💰 預估總稅負：**{total_tax:.2f} 萬元**")

# 頁尾
st.markdown("---")
st.markdown(
    """
    <div style='display:flex;justify-content:center;align-items:center;gap:1.5em;font-size:14px;color:gray;'>
      <a href='/' style='color:#006666;text-decoration:underline;'>《影響力》傳承策略平台</a>
      <a href='https://gracefo.com' target='_blank'>永傳家族辦公室</a>
      <a href='mailto:123@gracefo.com'>123@gracefo.com</a>
    </div>
    """,
    unsafe_allow_html=True
)
