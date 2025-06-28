import streamlit as st
import pandas as pd

# ------------------------------
# 計算函式定義
# ------------------------------

def calc_deed_tax(house_value):
    tax = house_value * 0.06
    return tax, f"{house_value} * 0.06"

def calc_stamp_tax(house_value, land_value):
    rate = 0.001
    base = house_value + land_value
    tax = base * rate
    return tax, f"({house_value} + {land_value}) * {rate}"

def calc_land_increment_tax(old_announced, new_announced, holding_years, is_self_use):
    gain = max(new_announced - old_announced, 0)
    if is_self_use:
        tax = gain * 0.10
        return tax, f"{gain} * 0.10"
    ratio = gain / old_announced if old_announced > 0 else float('inf')
    if ratio < 1:
        tax = gain * 0.20
        return tax, f"{gain} * 0.20"
    if ratio < 2:
        if holding_years <= 20:
            rate, b = 0.30, 0.10
        elif holding_years <= 30:
            rate, b = 0.28, 0.08
        elif holding_years <= 40:
            rate, b = 0.27, 0.07
        else:
            rate, b = 0.26, 0.06
        tax = max(gain * rate - old_announced * b, 0)
        return tax, f"{gain} * {rate} - {old_announced} * {b}"
    if holding_years <= 20:
        rate, b = 0.40, 0.30
    elif holding_years <= 30:
        rate, b = 0.36, 0.24
    elif holding_years <= 40:
        rate, b = 0.34, 0.21
    else:
        rate, b = 0.32, 0.18
    tax = max(gain * rate - old_announced * b, 0)
    return tax, f"{gain} * {rate} - {old_announced} * {b}"

def calc_real_estate_tax(sell_market, cost_basis, holding_years, is_self_use, is_resident):
    profit = max(sell_market - cost_basis, 0)
    if not is_resident:
        rate = 0.45 if holding_years <= 2 else 0.35
        return profit * rate, f"{profit} * {rate}"
    if is_self_use and holding_years > 6:
        taxable = max(profit - 400, 0)
        return taxable * 0.10, f"{taxable} * 0.10"
    if holding_years <= 2:
        rate = 0.45
    elif holding_years <= 5:
        rate = 0.35
    elif holding_years <= 10:
        rate = 0.20
    else:
        rate = 0.15
    return profit * rate, f"{profit} * {rate}"

def calc_progressive_tax(val, brackets):
    tax = 0
    rem = val
    low = 0
    parts = []
    for up, r in brackets:
        p = max(min(rem, up - low), 0)
        if p <= 0:
            break
        tax += p * r
        parts.append(f"{p} * {r}")
        rem -= p
        low = up
    return tax, " + ".join(parts) if parts else "0"

def calc_gift_tax(val):
    ex = 244
    txbl = max(val - ex, 0)
    br = [(5000, 0.10), (10000, 0.15), (float('inf'), 0.20)]
    tax, fmt = calc_progressive_tax(txbl, br)
    if txbl == 0:
        fmt = f"0 (免稅額{ex}萬元)"
    return tax, fmt

def calc_estate_tax(val):
    ex = 1333
    txbl = max(val - ex, 0)
    br = [(5000, 0.10), (10000, 0.15), (float('inf'), 0.20)]
    tax, fmt = calc_progressive_tax(txbl, br)
    if txbl == 0:
        fmt = f"0 (免稅額{ex}萬元)"
    return tax, fmt

# ------------------------------
# Streamlit UI
# ------------------------------
st.set_page_config(page_title="不動產稅負評估工具", layout="wide")
st.title("🏠 不動產稅負評估工具")
st.markdown("比較三種情境與各階段市價/公告價稅負，並顯示明細。")

# 使用者輸入
st.header("📌 市價與公告價輸入（萬元）")
# 買進
st.subheader("買進階段")
buy_market = st.number_input("買進市價", value=3000.0)
buy_land_ann = st.number_input("買進公告土地現值", value=900.0)
buy_house_ann = st.number_input("買進公告房屋評定現值", value=300.0)
# 移轉
st.subheader("移轉階段")
trans_land_ann = st.number_input("移轉公告土地現值", value=1400.0)
trans_house_ann = st.number_input("移轉公告房屋評定現值", value=280.0)
# 出售
st.subheader("出售階段")
sell_market = st.number_input("出售市價", value=4000.0)
sell_land_ann = st.number_input("出售公告土地現值", value=2000.0)
sell_house_ann = st.number_input("出售公告房屋評定現值", value=260.0)

# 通用條件
st.header("⏳ 持有與自用/居住條件")
hold_years = st.number_input("持有年數", min_value=0, value=2)
is_self = st.checkbox("自用住宅", value=False)
is_res = st.checkbox("境內居住者", value=True)

# 計算各情境

def compute(acq_mkt, acq_land, acq_house, tr_land, tr_house, sell_mkt, sell_land, sell_house, sc):
    sec = {"取得時": [], "移轉時": [], "出售時": []}
    # 取得
    if sc in [1, 2]:
        t, f = calc_deed_tax(acq_house)
        sec["取得時"].append(("契稅", t, f))
        t, f = calc_stamp_tax(acq_house, acq_land)
        sec["取得時"].append(("印花稅", t, f))
    else:
        t, f = calc_gift_tax(acq_mkt)
        sec["取得時"].append(("現金贈與稅", t, f))
        t, f = calc_deed_tax(acq_house)
        sec["取得時"].append(("契稅", t, f))
        t, f = calc_stamp_tax(acq_house, acq_land)
        sec["取得時"].append(("印花稅", t, f))
    # 移轉
    if sc == 1:
        t, f = calc_estate_tax(tr_land + tr_house)
        sec["移轉時"].append(("遺產稅", t, f))
    elif sc == 2:
        t, f = calc_gift_tax(tr_land + tr_house)
        sec["移轉時"].append(("贈與稅", t, f))
    # 出售
    old_land_ann = tr_land if sc in [1, 2] else acq_land
    t, f = calc_land_increment_tax(old_land_ann, sell_land, hold_years, is_self)
    sec["出售時"].append(("土地增值稅", t, f))
    basis = (tr_land + tr_house) if sc in [1, 2] else acq_mkt
    t, f = calc_real_estate_tax(sell_mkt, basis, hold_years, is_self, is_res)
    sec["出售時"].append(("房地合一稅", t, f))
    return sec

# 處理
scenarios = {
    "情境1：買進→繼承→出售": compute(buy_market, buy_land_ann, buy_house_ann,
                                trans_land_ann, trans_house_ann,
                                sell_market, sell_land_ann, sell_house_ann, 1),
    "情境2：買進→贈與→出售": compute(buy_market, buy_land_ann, buy_house_ann,
                                trans_land_ann, trans_house_ann,
                                sell_market, sell_land_ann, sell_house_ann, 2),
    "情境3：贈與現金→買進→出售": compute(buy_market, buy_land_ann, buy_house_ann,
                                trans_land_ann, trans_house_ann,
                                sell_market, sell_land_ann, sell_house_ann, 3)
}

# 比較表格
rows = []
for name, data in scenarios.items():
    s1 = sum(t for _, t, _ in data["取得時"])
    s2 = sum(t for _, t, _ in data["移轉時"])
    s3 = sum(t for _, t, _ in data["出售時"])
    rows.append([name, s1, s2, s3, s1 + s2 + s3])
df = pd.DataFrame(rows, columns=["情境", "取得時稅負", "移轉時稅負", "出售時稅負", "總稅負"])
st.subheader("📊 稅負比較表")
st.table(df)

# 明細展開
for name, data in scenarios.items():
    with st.expander(f"🔍 {name} 明細"):
        for stage, items in data.items():
            st.write(f"**{stage}**")
            st.table(pd.DataFrame(items, columns=["稅目", "金額(萬)", "公式"]))

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
