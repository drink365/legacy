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
    - 非境內居住者:
      * 持有2年內：45%
      * >2年：35%
    - 境內居住者:
      * 自用住宅且持有>6年：利潤扣除400萬後10%
      * 持有2年內：45%
      * >2至5年：35%
      * >5至10年：20%
      * >10年：15%
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
        taxable_profit = max(profit - 400, 0)
        rate = 0.10
        tax = taxable_profit * rate
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
    """
    贈與稅：年度免稅額244萬，超過部分適用累進稅率
    累進差額公式：
      - 免稅額後金額<=2811：税率10%
      - <=5621：税率15%，進位扣除140.55
      - >5621：税率20%，進位扣除421.6
    """
    exemption = 244
    taxable = max(value - exemption, 0)
    # 台灣贈與稅閾值 (單位：萬元)
    thr1, thr2 = 2811, 5621
    if taxable <= thr1:
        tax = taxable * 0.10
        formula = f"{taxable} * 0.10"
    elif taxable <= thr2:
        # progressive diff 140.55 萬元
        tax = taxable * 0.15 - 140.55
        formula = f"{taxable} * 0.15 - 140.55"
    else:
        # progressive diff 421.6 萬元
        tax = taxable * 0.20 - 421.6
        formula = f"{taxable} * 0.20 - 421.6"
    return max(tax, 0), formula


def calc_estate_tax(value):
    """
    遺產稅：基本免稅額1333萬，超過部分適用累進稅率
    累進差額公式：
      - 免稅額後金額<=5621：税率10%
      - <=11242：税率15%，扣除281.05
      - >11242：税率20%，扣除843.15
    """
    exemption = 1333
    taxable = max(value - exemption, 0)
    # 台灣遺產稅閾值 (單位：萬元)
    thr1_e, thr2_e = 5621, 11242
    if taxable <= thr1_e:
        tax = taxable * 0.10
        formula = f"{taxable} * 0.10"
    elif taxable <= thr2_e:
        tax = taxable * 0.15 - 281.05
        formula = f"{taxable} * 0.15 - 281.05"
    else:
        tax = taxable * 0.20 - 843.15
        formula = f"{taxable} * 0.20 - 843.15"
    return max(tax, 0), formula

# ------------------------------
# Streamlit UI
# ------------------------------

st.set_page_config(page_title="不動產稅負評估工具", layout="wide")

st.title("🏠 不動產稅負評估工具")
st.markdown("根據不同取得方式與出售情境，評估整體稅負。")

# 🏷️ 資產登記與資金來源
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
is_resident = st.checkbox("是否為境內居住者", value=True)

# 📌 買進的房產資訊
st.header("📌 買進的房產資訊")
buy_price = st.number_input("買進總價（萬元）", min_value=0.0, value=3000.0)
current_land_value = st.number_input("土地公告現值（萬元）", min_value=0.0, value=1000.0)
current_house_value = st.number_input("房屋評定現值（萬元）", min_value=0.0, value=200.0)

# 🎁 贈與／繼承時的公告價格
st.header("🎁 贈與／繼承時的公告價格")
transfer_land_value = st.number_input("贈與／繼承時土地公告現值（萬元）", min_value=0.0, value=1100.0)
transfer_house_value = st.number_input("贈與／繼承時房屋評定現值（萬元）", min_value=0.0, value=180.0)

# 📈 預估未來出售資料
st.header("📈 預估未來出售資料")
future_price = st.number_input("未來出售價格（萬元）", min_value=0.0, value=3800.0)
future_land_value = st.number_input("未來土地公告現值（萬元）", min_value=0.0, value=1200.0)
future_house_value = st.number_input("未來房屋評定現值（萬元）", min_value=0.0, value=190.0)

# ------------------------------
# 計算並顯示稅負
# ------------------------------
section1_taxes = []
section2_taxes = []
section3_taxes = []

def add_tax(lst, label, func, *args):
    tax, formula = func(*args)
    lst.append((label, tax, formula))

# Section1: 取得時稅負
def compute_section1():
    add_tax(section1_taxes, "契稅", calc_deed_tax, current_house_value)
    add_tax(section1_taxes, "印花稅", calc_stamp_tax, current_house_value, current_land_value)

# Section2 & Section3 根據情境
def compute_sections():
    if owner == "子女":
        if fund_source == "父母贈與現金":
            add_tax(section -->
