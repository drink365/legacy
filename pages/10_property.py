import streamlit as st
import pandas as pd

# ------------------------------
# 計算函式定義
# ------------------------------

def calc_deed_tax(house_value):
    rate = 0.06
    tax = house_value * rate
    return tax, f"{house_value} * {rate}"


def calc_stamp_tax(house_value, land_value):
    rate = 0.001
    base = house_value + land_value
    tax = base * rate
    return tax, f"({house_value} + {land_value}) * {rate}"


def calc_land_increment_tax(old_value, new_value, holding_years, is_self_use):
    gain = max(new_value - old_value, 0)
    if is_self_use:
        rate = 0.10
        return gain * rate, f"{gain} * {rate}"
    ratio = gain / old_value if old_value > 0 else float('inf')
    if ratio < 1:
        rate = 0.20
        return gain * rate, f"{gain} * {rate}"
    if ratio < 2:
        if holding_years <= 20:
            rate, b_rate = 0.30, 0.10
        elif holding_years <= 30:
            rate, b_rate = 0.28, 0.08
        elif holding_years <= 40:
            rate, b_rate = 0.27, 0.07
        else:
            rate, b_rate = 0.26, 0.06
        tax = max(gain * rate - old_value * b_rate, 0)
        return tax, f"{gain} * {rate} - {old_value} * {b_rate}"
    if holding_years <= 20:
        rate, b_rate = 0.40, 0.30
    elif holding_years <= 30:
        rate, b_rate = 0.36, 0.24
    elif holding_years <= 40:
        rate, b_rate = 0.34, 0.21
    else:
        rate, b_rate = 0.32, 0.18
    tax = max(gain * rate - old_value * b_rate, 0)
    return tax, f"{gain} * {rate} - {old_value} * {b_rate}"


def calc_real_estate_tax(sell_price, cost, holding_years, is_self_use, is_resident):
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
    tax, remaining, lower, parts = 0, taxable, 0, []
    for upper, rate in brackets:
        portion = max(min(remaining, upper - lower), 0)
        if portion <= 0:
            break
        tax += portion * rate
        parts.append(f"{portion} * {rate}")
        remaining -= portion
        lower = upper
    return tax, " + ".join(parts) if parts else "0"


def calc_gift_tax(value):
    exemption = 244
    taxable = max(value - exemption, 0)
    brackets = [(5000, 0.10), (10000, 0.15), (float('inf'), 0.20)]
    tax, formula = calc_progressive_tax(taxable, brackets)
    if taxable == 0:
        formula = f"0 (免稅額{exemption}萬元)"
    return tax, formula


def calc_estate_tax(value):
    exemption = 1333
    taxable = max(value - exemption, 0)
    brackets = [(5000, 0.10), (10000, 0.15), (float('inf'), 0.20)]
    tax, formula = calc_progressive_tax(taxable, brackets)
    if taxable == 0:
        formula = f"0 (免稅額{exemption}萬元)"
    return tax, formula

# ------------------------------
# Streamlit UI
# ------------------------------
st.set_page_config(page_title="不動產稅負評估工具", layout="wide")
st.title("🏠 不動產稅負評估工具")
st.markdown("比較三種情境的稅負，並展示每項稅負明細。")

# 輸入欄位
st.header("📌 主要金額與持有條件")
buy_price = st.number_input("買進總價（萬元）", value=3000.0)
transfer_price = st.number_input("移轉時公告總價（萬元）", value=1800.0)
sell_price = st.number_input("出售價格（萬元）", value=3800.0)
holding_years = st.number_input("持有年數", min_value=0, value=2)
is_self_use = st.checkbox("自用住宅", value=False)
is_resident = st.checkbox("境內居住者", value=True)

# 計算函式

def compute_scenario(acq, trans, sale, sc):
    sec = {"取得時": [], "移轉時": [], "出售時": []}
    # 取得時
    if sc in [1, 2]:
        tax, fmt = calc_deed_tax(acq)
        sec["取得時"].append(("契稅", tax, fmt))
        h, l = acq*0.5, acq*0.5
        tax, fmt = calc_stamp_tax(h, l)
        sec["取得時"].append(("印花稅", tax, fmt))
    else:
        tax, fmt = calc_gift_tax(acq)
        sec["取得時"].append(("現金贈與稅", tax, fmt))
        tax, fmt = calc_deed_tax(acq)
        sec["取得時"].append(("契稅", tax, fmt))
        h, l = acq*0.5, acq*0.5
        tax, fmt = calc_stamp_tax(h, l)
        sec["取得時"].append(("印花稅", tax, fmt))
    # 移轉時
    if sc == 1:
        tax, fmt = calc_estate_tax(trans)
        sec["移轉時"].append(("遺產稅", tax, fmt))
    elif sc == 2:
        tax, fmt = calc_gift_tax(trans)
        sec["移轉時"].append(("贈與稅", tax, fmt))
    # 出售時
    base = trans if sc in [1,2] else acq
    old_l, new_l = base*0.5, sale*0.5
    tax, fmt = calc_land_increment_tax(old_l, new_l, holding_years, is_self_use)
    sec["出售時"].append(("土地增值稅", tax, fmt))
    tax, fmt = calc_real_estate_tax(sale, base, holding_years, is_self_use, is_resident)
    sec["出售時"].append(("房地合一稅", tax, fmt))
    return sec

# 執行計算
scenarios = {"情境1：買進→繼承→出售": compute_scenario(buy_price, transfer_price, sell_price, 1),
             "情境2：買進→贈與→出售": compute_scenario(buy_price, transfer_price, sell_price, 2),
             "情境3：贈與現金→買進→出售": compute_scenario(buy_price, transfer_price, sell_price, 3)}

# 組成比較表格
rows = []
for name, data in scenarios.items():
    s1 = sum(t for _, t, _ in data["取得時"])
    s2 = sum(t for _, t, _ in data["移轉時"])
    s3 = sum(t for _, t, _ in data["出售時"])
    rows.append([name, s1, s2, s3, s1+s2+s3])
df = pd.DataFrame(rows, columns=["情境", "取得時小計", "移轉時小計", "出售時小計", "總稅負"])

st.subheader("📊 三種情境稅負比較表")
st.table(df)

# 展開明細
for name, data in scenarios.items():
    with st.expander(f"🔍 {name} 明細"):        
        for stage, items in data.items():
            st.write(f"**{stage}**")
            detail_df = pd.DataFrame(items, columns=["稅目", "金額 (萬)", "計算公式"])            
            st.table(detail_df)

# 頁尾
st.markdown("---")
st.markdown(
    "<div style='display:flex;justify-content:center;align-items:center;gap:1.5em;font-size:14px;color:gray;'>"
    "<a href='/' style='color:#006666;text-decoration:underline;'>《影響力》傳承策略平台</a>"
    "<a href='https://gracefo.com' target='_blank'>永傳家族辦公室</a>"
    "<a href='mailto:123@gracefo.com'>123@gracefo.com</a>"
    "</div>",
    unsafe_allow_html=True
)
