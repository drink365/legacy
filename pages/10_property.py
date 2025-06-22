import streamlit as st

st.set_page_config(page_title="不動產稅負評估", page_icon="🏠")
st.title("🏠 不動產稅負評估")

# 使用者輸入區
st.header("輸入條件")
with st.form("input_form"):
    ownership = st.radio("登記持有人", ["子女", "父母"])
    mode = st.radio("贈與方式（僅限子女名下）", ["贈與房產", "贈與現金讓子女購屋"])

    land_value = st.number_input("土地公告現值（萬元）", min_value=0, value=800)
    house_value = st.number_input("房屋評定現值（萬元）", min_value=0, value=200)
    cash_amount = st.number_input("贈與現金金額（萬元）", min_value=0, value=3000)

    if ownership == "父母":
        parent_hold = st.slider("父母持有年數", 0, 40, 10)
        child_hold = st.slider("子女持有年數（繼承後）", 0, 10, 1)
    else:
        child_hold = st.slider("子女持有年數", 0, 10, 3)
        parent_hold = 0

    is_self_use = st.checkbox("是否為自用住宅", value=True)

    submitted = st.form_submit_button("開始試算")

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

    if ownership == "子女":
        if mode == "贈與現金讓子女購屋":
            gift_base = cash_amount
        else:
            gift_base = land_value + house_value

        gift_tax = calc_tax(gift_base, 244)
        land_gain = land_value * 0.5  # 假設增值 50%
        land_tax = int(land_gain * (0.4 if not is_self_use else 0.2) * 10000)

        house_sale_price = land_value + house_value * 1.5
        cost_basis = cash_amount if mode == "贈與現金讓子女購屋" else (land_value + house_value)
        profit = house_sale_price - cost_basis
        ho_rate = get_land_tax_rate(child_hold, is_self_use)
        ho_tax = int(profit * ho_rate * 10000)

        st.markdown(f"- 🎁 預估贈與稅：**{gift_tax:,} 元**")
        st.markdown(f"- 🧾 預估土地增值稅：**{land_tax:,} 元**")
        st.markdown(f"- 🏠 預估房地合一稅（未來售屋）：**{ho_tax:,} 元**")

    else:  # 父母名下（遺產＋房地合一稅）
        estate_base = land_value + house_value
        estate_tax = calc_tax(estate_base, 1333)
        ho_years = parent_hold + child_hold

        house_sale_price = land_value + house_value * 1.5
        profit = house_sale_price - (land_value + house_value)
        ho_rate = get_land_tax_rate(ho_years, is_self_use)
        ho_tax = int(profit * ho_rate * 10000)

        st.markdown(f"- 🧾 預估遺產稅：**{estate_tax:,} 元**")
        st.markdown(f"- 🏠 預估房地合一稅（未來售屋）：**{ho_tax:,} 元**")
        st.markdown("- 💡 備註：繼承可延續持有年限，有助於降低未來房地合一稅率。")

    st.info("本工具採用105年新制房地合一課稅邏輯，並假設贈與土地已有增值。")
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
