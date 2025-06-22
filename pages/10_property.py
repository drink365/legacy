import streamlit as st

# 頁面設定
st.set_page_config(page_title="不動產稅負評估工具", layout="wide")

st.title("🏠 不動產稅負評估工具")
st.markdown("請依序輸入以下資訊，系統將自動試算買賣、贈與與繼承的各項稅負。")

# --- 房屋與土地原始取得資料 ---
st.header("📌 房屋與土地資訊（當初取得）")
original_price = st.number_input("市價（萬元）｜當初取得", min_value=0.0, value=3000.0)
original_land_value = st.number_input("土地公告現值（萬元）｜當初取得", min_value=0.0, value=1000.0)
original_house_value = st.number_input("房屋評定現值（萬元）｜當初取得", min_value=0.0, value=200.0)

# --- 移轉時資料 ---
st.header("🔄 移轉資訊（贈與或繼承時）")
transfer_price = st.number_input("市價（萬元）｜移轉時", min_value=0.0, value=3000.0)
transfer_land_value = st.number_input("土地公告現值（萬元）｜移轉時", min_value=0.0, value=1000.0)
transfer_house_value = st.number_input("房屋評定現值（萬元）｜移轉時", min_value=0.0, value=200.0)

# --- 未來出售預估資料 ---
st.header("📈 未來出售資訊")
future_price = st.number_input("市價（萬元）｜未來出售", min_value=0.0, value=3800.0)
future_land_value = st.number_input("土地公告現值（萬元）｜未來出售", min_value=0.0, value=1200.0)
future_house_value = st.number_input("房屋評定現值（萬元）｜未來出售", min_value=0.0, value=250.0)

# --- 基本條件 ---
st.header("⏳ 其他基本條件")
holding_years = st.number_input("子女持有年數", min_value=0, value=2)
is_self_use = st.checkbox("是否為自用住宅", value=False)

# --- 土地增值稅試算 ---
increased_value = future_land_value - transfer_land_value
if is_self_use:
    land_increment_tax = increased_value * 0.10
    formula_land_tax = f"{increased_value:.1f} × 10%"
else:
    first = min(increased_value, 400)
    second = min(max(increased_value - 400, 0), 400)
    third = max(increased_value - 800, 0)
    land_increment_tax = first * 0.2 + second * 0.3 + third * 0.4
    formula_land_tax = f"{first:.1f}×20% + {second:.1f}×30% + {third:.1f}×40%"

# --- 印花稅與契稅（以未來價格計） ---
stamp_tax = future_price * 0.001
contract_tax = future_price * 0.06

# --- 房地合一稅（以取得成本與未來價格差額估） ---
acquisition_cost = transfer_land_value + transfer_house_value
real_estate_tax_base = future_price - acquisition_cost
real_estate_tax = real_estate_tax_base * 0.35

# --- 贈與稅與遺產稅 ---
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

tax_base = transfer_land_value + transfer_house_value
gift_tax, gift_formula = calc_gift_tax(tax_base)
estate_tax, estate_formula = calc_estate_tax(tax_base)

# --- 顯示稅負試算總表 ---
st.header("📊 稅負試算總表")
st.markdown(f"""
📍 **土地增值稅**：約 **{land_increment_tax:.1f} 萬元**（{'自用10%' if is_self_use else '一般用地20~40%'}）  
- 計算式：{formula_land_tax}

📄 **印花稅**：約 **{stamp_tax:.1f} 萬元**（0.1%）  
📄 **契稅**：約 **{contract_tax:.1f} 萬元**（6%）

🏢 **房地合一稅**：約 **{real_estate_tax:.1f} 萬元**（假設獲利×35%）

🎁 **贈與稅**：約 **{gift_tax:.1f} 萬元**（如為贈與）  
- 計算式：{gift_formula}

🪦 **遺產稅**：約 **{estate_tax:.1f} 萬元**（如為繼承）  
- 計算式：{estate_formula}
""")

# --- 稅負總和（預估）---
total_tax = land_increment_tax + stamp_tax + contract_tax + real_estate_tax + gift_tax + estate_tax
st.markdown(f"💰 **總稅負金額（含贈與或遺產稅）**：預估約 **{total_tax:.1f} 萬元**")

# --- 頁尾 ---
st.markdown("""
---
<div style='display: flex; justify-content: center; align-items: center; gap: 1.5em; font-size: 14px; color: gray;'>
  <a href='/' style='color:#006666; text-decoration: underline;'>《影響力》傳承策略平台</a>
  <a href='https://gracefo.com' target='_blank'>永傳家族辦公室</a>
  <a href='mailto:123@gracefo.com'>123@gracefo.com</a>
</div>
""", unsafe_allow_html=True)
