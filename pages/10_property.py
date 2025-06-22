import streamlit as st

# 頁面設定
st.set_page_config(page_title="不動產稅負評估", layout="wide")

st.title("🏠 不動產稅負評估工具")
st.markdown("請依序輸入以下資訊，系統將自動試算買賣、贈與與繼承的各項稅負。")

# 房屋與土地資訊輸入
st.header("📌 房屋與土地資訊")
current_land_value = st.number_input("土地公告現值（萬元）", min_value=0.0, value=400.0)
current_price = st.number_input("市價（萬元）", min_value=0.0, value=3800.0)
current_house_value = st.number_input("房屋評定現值（萬元）", min_value=0.0, value=200.0)

future_price = st.number_input("預估未來出售價格（萬元）", min_value=0.0, value=3800.0)
future_land_value = st.number_input("預估未來土地公告現值（萬元）", min_value=0.0, value=600.0)
future_house_value = st.number_input("預估未來房屋評定現值（萬元）", min_value=0.0, value=320.0)

holding_years = st.number_input("持有年數", min_value=0, value=2)
is_self_use = st.checkbox("是否為自用住宅", value=False)

# 土增稅計算
increased_value = future_land_value - current_land_value

if is_self_use:
    land_tax_rate = 0.10
    land_increment_tax = increased_value * land_tax_rate
    formula_land_tax = f"{increased_value:.1f} × 10%"
else:
    first = min(increased_value, 400)
    second = min(max(increased_value - 400, 0), 400)
    third = max(increased_value - 800, 0)
    land_increment_tax = first * 0.2 + second * 0.3 + third * 0.4
    formula_land_tax = f"{first:.1f}×20% + {second:.1f}×30% + {third:.1f}×40%"

# 印花稅與契稅
stamp_tax = future_price * 0.001
stamp_formula = f"{future_price:.1f} × 0.1%"

contract_tax = future_price * 0.06
contract_formula = f"{future_price:.1f} × 6%"

# 房地合一稅（以35%固定稅率）
acquisition_cost = current_price - current_land_value + current_house_value
real_estate_tax_base = future_price - acquisition_cost
real_estate_tax = real_estate_tax_base * 0.35
real_estate_formula = f"({future_price:.1f} - {acquisition_cost:.1f}) × 35%"

# 顯示稅負結果
st.header("📊 稅負試算總表")
st.markdown(f"""
📍 **土地增值稅**：約 **{land_increment_tax:.1f} 萬元**（{'自用優惠稅率10%' if is_self_use else '一般用地累進稅率20~40%'}，持有 {holding_years} 年）  
- 計算式：{formula_land_tax}

📄 **印花稅**：約 **{stamp_tax:.1f} 萬元**（0.1%）  
- 計算式：{stamp_formula}

📄 **契稅**：約 **{contract_tax:.1f} 萬元**（6%）  
- 計算式：{contract_formula}

🏢 **房地合一稅**：約 **{real_estate_tax:.1f} 萬元**（預估獲利 × 35%）  
- 計算式：{real_estate_formula}
""")

# 頁尾
st.markdown("---")
st.markdown("""
<div style='display: flex; justify-content: center; align-items: center; gap: 1.5em; font-size: 14px; color: gray;'>
  <a href='/' style='color:#006666; text-decoration: underline;'>《影響力》傳承策略平台</a>
  <a href='https://gracefo.com' target='_blank'>永傳家族辦公室</a>
  <a href='mailto:123@gracefo.com'>123@gracefo.com</a>
</div>
""", unsafe_allow_html=True)
