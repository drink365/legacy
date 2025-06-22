import streamlit as st

# 頁面設定
st.set_page_config(page_title="不動產稅負評估工具", layout="wide")
st.title("🏠 不動產稅負評估工具")
st.markdown("請依序輸入以下資訊，系統將自動試算各類型移轉與出售的稅負。")

# 共用函式
def calc_gift_tax(amount):
    if amount <= 2811:
        return amount * 0.10, f"{amount:.1f} × 10%"
    elif amount <= 5621:
        return amount * 0.15 - 140.55, f"{amount:.1f} × 15% - 140.55"
    else:
        return amount * 0.20 - 421.6, f"{amount:.1f} × 20% - 421.6"

def calc_estate_tax(amount):
    if amount <= 5621:
        return amount * 0.10, f"{amount:.1f} × 10%"
    elif amount <= 11242:
        return amount * 0.15 - 281.05, f"{amount:.1f} × 15% - 281.05"
    else:
        return amount * 0.20 - 842.3, f"{amount:.1f} × 20% - 842.3"

def calc_land_increment_tax(old_lv, new_lv, is_self_use):
    increase = new_lv - old_lv
    if increase <= 0:
        return 0, "未增值"
    if is_self_use:
        return increase * 0.10, f"{increase:.1f} × 10%"
    else:
        first = min(increase, 400)
        second = min(max(increase - 400, 0), 400)
        third = max(increase - 800, 0)
        tax = first * 0.2 + second * 0.3 + third * 0.4
        formula = f"{first:.1f}×20% + {second:.1f}×30% + {third:.1f}×40%"
        return tax, formula

def calc_real_estate_tax(sale_price, cost_basis):
    gain = sale_price - cost_basis
    return gain * 0.35, f"({sale_price:.1f} - {cost_basis:.1f}) × 35%"

# 輸入區塊
st.header("📌 房屋與土地資訊（當初取得）")
original_price = st.number_input("市價（萬元）", min_value=0.0, value=3000.0)
original_land_value = st.number_input("土地公告現值（萬元）", min_value=0.0, value=1000.0)
original_house_value = st.number_input("房屋評定現值（萬元）", min_value=0.0, value=200.0)

st.header("🏷️ 資產登記與移轉情境")
owner = st.radio("目前登記在誰名下？", ["父母", "子女"])
transfer_type = ""
fund_source = ""

if owner == "父母":
    transfer_type = st.radio("將來打算如何移轉給子女？", ["留待繼承", "贈與房產"])
else:
    fund_source = st.radio("子女購屋資金來源為？", ["自行購屋", "父母贈與現金"])

st.header("🏠 移轉時的價格")
transfer_price = st.number_input("市價（萬元）", min_value=0.0, value=3000.0)
transfer_land_value = st.number_input("土地公告現值（萬元）", min_value=0.0, value=1000.0)
transfer_house_value = st.number_input("房屋評定現值（萬元）", min_value=0.0, value=200.0)

st.header("📈 將來出售資訊")
future_price = st.number_input("未來市價（萬元）", min_value=0.0, value=3800.0)
future_land_value = st.number_input("未來土地公告現值（萬元）", min_value=0.0, value=1200.0)
future_house_value = st.number_input("未來房屋評定現值（萬元）", min_value=0.0, value=250.0)

st.header("⏳ 其他條件")
is_self_use = st.checkbox("是否為自用住宅", value=False)

# 稅負計算
gift_tax = estate_tax = land_tax = stamp_tax = contract_tax = real_tax = 0
desc = []

# 第一次移轉
if owner == "父母":
    if transfer_type == "贈與房產":
        gift_tax, gf = calc_gift_tax(transfer_land_value + transfer_house_value)
        desc.append(f"🎁 贈與稅：{gift_tax:.1f} 萬元（{gf}）")
        land1, lf1 = calc_land_increment_tax(original_land_value, transfer_land_value, is_self_use)
        land_tax += land1
        desc.append(f"📍 土地增值稅（贈與）：{land1:.1f} 萬元（{lf1}）")
        stamp_tax = transfer_price * 0.001
        contract_tax = transfer_price * 0.06
        desc.append(f"📄 印花稅：{stamp_tax:.1f} 萬元")
        desc.append(f"📄 契稅：{contract_tax:.1f} 萬元")

    elif transfer_type == "留待繼承":
        estate_tax, ef = calc_estate_tax(transfer_land_value + transfer_house_value)
        desc.append(f"🪦 遺產稅：{estate_tax:.1f} 萬元（{ef}）")

elif owner == "子女":
    if fund_source == "父母贈與現金":
        gift_tax, gf = calc_gift_tax(transfer_price)
        desc.append(f"🎁 贈與稅（現金）：{gift_tax:.1f} 萬元（{gf}）")
        stamp_tax = transfer_price * 0.001
        contract_tax = transfer_price * 0.06
        desc.append(f"📄 印花稅：{stamp_tax:.1f} 萬元")
        desc.append(f"📄 契稅：{contract_tax:.1f} 萬元")

# 第二次出售
cost_basis = transfer_land_value + transfer_house_value
real_tax, rf = calc_real_estate_tax(future_price, cost_basis)
desc.append(f"🏢 房地合一稅：{real_tax:.1f} 萬元（{rf}）")
land2, lf2 = calc_land_increment_tax(transfer_land_value, future_land_value, is_self_use)
land_tax += land2
desc.append(f"📍 土地增值稅（出售）：{land2:.1f} 萬元（{lf2}）")

# 總稅額
total_tax = gift_tax + estate_tax + land_tax + stamp_tax + contract_tax + real_tax

st.header("📊 稅負試算總表")
for item in desc:
    st.markdown("- " + item)
st.markdown(f"💰 **總稅負：{total_tax:.1f} 萬元**")

# 頁尾
st.markdown("---")
st.markdown("""
<div style='text-align:center; font-size: 14px; color: gray;'>
  《影響力》傳承策略平台｜<a href='https://gracefo.com' target='_blank'>永傳家族辦公室</a>｜聯絡信箱：123@gracefo.com
</div>
""", unsafe_allow_html=True)
