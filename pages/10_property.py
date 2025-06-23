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


def calc_land_increment_tax(old_value, new_value):
    """
    土地增值稅：增值部分 * 20%
    """
    gain = max(new_value - old_value, 0)
    rate = 0.20
    tax = gain * rate
    formula = f"({new_value} - {old_value}) * {rate}"
    return tax, formula


def calc_real_estate_tax(sell_price, cost, holding_years, is_self_use, is_resident):
    """
    房地合一稅計算：
    - 境內居住者:
      * 持有2年內：45%
      * >2至5年：35%
      * >5至10年：20%
      * >10年：15%
      * 自用住宅且持有>6年：總利潤扣除400萬後10%
    - 非境內居住者:
      * 持有2年內：45%
      * >2年：35%
    """
    profit = max(sell_price - cost, 0)
    # 非境內居住者
    if not is_resident:
        rate = 0.45 if holding_years <= 2 else 0.35
        tax = profit * rate
        formula = f"({sell_price} - {cost}) * {rate}"
        return tax, formula

    # 境內居住者
    if is_self_use and holding_years > 6:
        taxable = max(profit - 400, 0)
        rate = 0.10
        tax = taxable * rate
        formula = f"({sell_price} - {cost} - 400) * {rate}"
        return tax, formula
    else:
        if holding_years <= 2:
            rate = 0.45
        elif holding_years <= 5:
            rate = 0.35
        elif holding_years <= 10:
            rate = 0.20
        else:
            rate = 0.15
        tax = profit * rate
        formula = f"({sell_price} - {cost}) * {rate}"
        return tax, formula


def calc_gift_tax(value):
    rate = 0.10
    tax = value * rate
    formula = f"{value} * {rate}"
    return tax, formula


def calc_estate_tax(value):
    rate = 0.10
    tax = value * rate
    formula = f"{value} * {rate}"
    return tax, formula

# ------------------------------
# Streamlit UI
# ------------------------------

st.set_page_config(page_title="不動產稅負評估工具", layout="wide")

st.title("🏠 不動產稅負評估工具")
st.markdown("根據不同取得方式與出售情境，評估整體稅負。")

# 🏷️ 資產登記與資金來源 (放置最上方)
st.header("🏷️ 資產登記與資金來源")
owner = st.radio("目前房產登記在誰名下？", ["父母", "子女"])
if owner == "父母":
    transfer_type = st.radio("將來如何移轉給子女？", ["留待繼承", "贈與房產"])
else:
    fund_source = st.radio("子女資金來源為？", ["自行購屋", "父母贈與現金"])

# ⏳ 基本條件
st.header("⏳ 基本條件")
holding_years = st.number_input("子女持有年數", min_value=0, value=2)
is_self_use = st.checkbox("是否符合自用住宅條件", value=False)
# 新增：稅務身分判斷
is_resident = st.checkbox("是否為境內居住者", value=True)

# 📌 房屋與土地資訊
st.header("📌 房屋與土地資訊")
current_land_value = st.number_input("現在土地公告現值（萬元）", min_value=0.0, value=1000.0)
current_house_value = st.number_input("現在房屋評定現值（萬元）", min_value=0.0, value=200.0)

# 🎁 贈與／繼承時的公告價格
st.header("🎁 贈與／繼承時的公告價格")
transfer_land_value = st.number_input("贈與／繼承時土地公告現值（萬元）", min_value=0.0, value=1100.0)
transfer_house_value = st.number_input("贈與／繼承時房屋評定現值（萬元）", min_value=0.0, value=180.0)

# 📈 預估未來出售資料
st.header("📈 預估未來出售資料")
future_price = st.number_input("未來出售價格（萬元）", min_value=0.0, value=3800.0)
future_land_value = st.number_input("未來土地公告現值（萬元）", min_value=0.0, value=1200.0)
future_house_value = st.number_input("未來房屋評定現值（萬元）", min_value=0.0, value=190.0)

# 初始化稅負列表
section1_taxes = []
section2_taxes = []
section3_taxes = []

# 計算 section1: 取得時稅負 (契稅 + 印花稅)
if owner in ["父母", "子女"]:
    deed_tax, deed_formula = calc_deed_tax(current_house_value)
    stamp_tax, stamp_formula = calc_stamp_tax(current_house_value, current_land_value)
    section1_taxes.append(("契稅", deed_tax, deed_formula))
    section1_taxes.append(("印花稅", stamp_tax, stamp_formula))

# 根據 owner 情境處理 section2, section3
if owner == "子女":
    # 子女自行購屋，僅在 section3 計算出售稅負
    land_tax, land_formula = calc_land_increment_tax(current_land_value, future_land_value)
    re_tax, re_formula = calc_real_estate_tax(future_price, current_house_value + current_land_value, holding_years, is_self_use, is_resident)
    section3_taxes.append(("土地增值稅", land_tax, land_formula))
    section3_taxes.append(("房地合一稅", re_tax, re_formula))
    if fund_source == "父母贈與現金":
        gift_tax, gift_formula = calc_gift_tax(current_house_value + current_land_value)
        section2_taxes.append(("贈與稅", gift_tax, gift_formula))
elif owner == "父母":
    if transfer_type == "贈與房產":
        # section2: 贈與階段稅負
        base_value = transfer_house_value + transfer_land_value
        gift_tax, gift_formula = calc_gift_tax(base_value)
        deed2_tax, deed2_formula = calc_deed_tax(transfer_house_value)
        stamp2_tax, stamp2_formula = calc_stamp_tax(transfer_house_value, transfer_land_value)
        land2_tax, land2_formula = calc_land_increment_tax(current_land_value, transfer_land_value)
        section2_taxes.extend([
            ("贈與稅", gift_tax, gift_formula),
            ("契稅（受贈人）", deed2_tax, deed2_formula),
            ("印花稅", stamp2_tax, stamp2_formula),
            ("土地增值稅（受贈人）", land2_tax, land2_formula),
        ])
        # section3: 子女出售階段
        sale_cost = base_value
        land3_tax, land3_formula = calc_land_increment_tax(transfer_land_value, future_land_value)
        re3_tax, re3_formula = calc_real_estate_tax(future_price, sale_cost, holding_years, is_self_use, is_resident)
        section3_taxes.append(("土地增值稅", land3_tax, land3_formula))
        section3_taxes.append(("房地合一稅", re3_tax, re3_formula))
    else:
        # 留待繼承
        base_value = transfer_house_value + transfer_land_value
        estate_tax, estate_formula = calc_estate_tax(base_value)
        section2_taxes.append(("遺產稅", estate_tax, estate_formula))
        land3_tax, land3_formula = calc_land_increment_tax(transfer_land_value, future_land_value)
        re3_tax, re3_formula = calc_real_estate_tax(future_price, base_value, holding_years, is_self_use, is_resident)
        section3_taxes.append(("土地增值稅", land3_tax, land3_formula))
        section3_taxes.append(("房地合一稅", re3_tax, re3_formula))

# 顯示稅負明細
st.header("📋 稅負明細報告")
if section1_taxes:
    st.subheader("1️⃣ 取得時應繳稅負")
    for label, amount, formula in section1_taxes:
        st.markdown(f"- **{label}**：{amount:.2f} 萬元（{formula}）")
if section2_taxes:
    st.subheader("2️⃣ 贈與或繼承時應繳稅負")
    for label, amount, formula in section2_taxes:
        st.markdown(f"- **{label}**：{amount:.2f} 萬元（{formula}）")
if section3_taxes:
    st.subheader("3️⃣ 未來出售時應繳稅負")
    for label, amount, formula in section3_taxes:
        st.markdown(f"- **{label}**：{amount:.2f} 萬元（{formula}）")

# 顯示總稅負
total_tax = sum(x[1] for x in section1_taxes + section2_taxes + section3_taxes)
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
