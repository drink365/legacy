import streamlit as st

st.set_page_config(page_title="不動產稅負評估", page_icon="🏠")
st.title("🏠 不動產稅負評估")

st.header("輸入條件")
owner = st.radio("房屋將登記在誰名下？", ["父母", "子女"])

# 初始化變數
mode = ""
parent_hold = 0
child_hold = 0
cash_amount = 0

if owner == "父母":
    future_plan = st.radio("未來預計如何處置？", ["留待繼承", "將來贈與給子女"])
    land_value = st.number_input("土地公告現值（萬元）", min_value=0, value=800, key="land_f")
    house_value = st.number_input("房屋評定現值（萬元）", min_value=0, value=200, key="house_f")
    child_hold = st.slider("繼承或贈與後子女預計持有年數", 0, 20, 1)
    parent_hold = 20 if future_plan == "留待繼承" else st.slider("父母預計持有年數", 0, 40, 10)
    mode = "繼承" if future_plan == "留待繼承" else "贈與房產"
else:
    source = st.radio("購屋資金來源？", ["子女自備款", "父母贈與現金"])
    land_value = st.number_input("土地公告現值（萬元）", min_value=0, value=800, key="land_c")
    house_value = st.number_input("房屋評定現值（萬元）", min_value=0, value=200, key="house_c")
    child_hold = st.slider("子女持有年數", 0, 20, 3)
    mode = "自備款" if source == "子女自備款" else "贈與現金"
    cash_amount = st.number_input("父母贈與現金金額（萬元）", min_value=0, value=3000) if source == "父母贈與現金" else 0

is_self_use = st.checkbox("是否為自用住宅", value=True)

submitted = st.button("開始試算")

# 稅率表
brackets = [
    (2811, 0.10, 0),
    (5621, 0.15, 281.1),
    (float("inf"), 0.20, 703.1)
]

# 房地合一稅率計算邏輯
def get_land_tax_rate(years, self_use):
    if self_use:
        if years >= 6:
            return 0.10
        elif years >= 2:
            return 0.20
    if years < 1:
        return 0.45
    elif years < 2:
        return 0.35
    elif years < 10:
        return 0.30
    else:
        return 0.20

# 累進稅額計算（萬→元）
def calc_tax(base, exemption):
    taxable = base - exemption
    if taxable <= 0:
        return 0
    for limit, rate, base_tax in brackets:
        if taxable <= limit:
            return int(taxable * rate * 10000)
    return 0

# 顯示試算結果
if submitted:
    st.header("試算結果")

    if owner == "子女":
        if mode == "贈與現金":
            gift_base = cash_amount
        else:
            gift_base = 0

        gift_tax = calc_tax(gift_base, 244) if gift_base > 0 else 0
        land_gain = land_value * 0.5
        land_tax = int(land_gain * (0.4 if not is_self_use else 0.2) * 10000)

        house_sale_price = land_value + house_value * 1.5
        cost_basis = cash_amount if mode == "贈與現金" else (land_value + house_value)
        profit = house_sale_price - cost_basis
        ho_rate = get_land_tax_rate(child_hold, is_self_use)
        ho_tax = int(profit * ho_rate * 10000)

        if gift_tax > 0:
            st.markdown(f"- 🎁 預估贈與稅：**{gift_tax:,} 元**")
        st.markdown(f"- 🧾 預估土地增值稅：**{land_tax:,} 元**")
        st.markdown(f"- 🏠 預估房地合一稅（未來售屋）：**{ho_tax:,} 元**")

    else:  # 父母名下
        estate_base = land_value + house_value
        if mode == "繼承":
            estate_tax = calc_tax(estate_base, 1333)
            ho_years = parent_hold + child_hold
        else:  # 贈與房產
            estate_tax = calc_tax(estate_base, 244)
            ho_years = child_hold

        house_sale_price = land_value + house_value * 1.5
        profit = house_sale_price - (land_value + house_value)
        ho_rate = get_land_tax_rate(ho_years, is_self_use)
        ho_tax = int(profit * ho_rate * 10000)

        st.markdown(f"- {'🧾 遺產稅' if mode == '繼承' else '🎁 贈與稅'}：**{estate_tax:,} 元**")
        st.markdown(f"- 🏠 預估房地合一稅（未來售屋）：**{ho_tax:,} 元**")
        st.markdown(f"- 💡 {'繼承可延續持有年限，有助於降低未來稅率。' if mode == '繼承' else '贈與會重置年限，可能稅負較重。'}")

    st.info("本工具採用105年新制房地合一課稅邏輯，並假設土地有增值。")
    st.caption("※ 試算僅供參考，實際稅負請洽稅務專業人員。")

# --- 聯絡資訊 ---
st.markdown("---")
st.markdown("""
<div style='display: flex; justify-content: center; align-items: center; gap: 1.5em; font-size: 14px; color: gray;'>
  <a href='/' style='color:#006666; text-decoration: underline;'>《影響力》傳承策略平台</a>
  <a href='https://gracefo.com' target='_blank'>永傳家族辦公室</a>
  <a href='mailto:123@gracefo.com'>123@gracefo.com</a>
</div>
""", unsafe_allow_html=True)
