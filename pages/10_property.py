import streamlit as st

# 頁面設定
st.set_page_config(page_title="不動產稅負評估", layout="wide")
st.title("🏠 不動產稅負評估工具")
st.markdown("請依序輸入以下資訊，系統將自動試算買賣、贈與與繼承的各項稅負。")

# 房屋與土地資訊輸入
st.header("📌 房屋與土地資訊")
current_price = st.number_input("現值｜市價（萬元）", min_value=0.0, value=3000.0, key="cur_price")
current_land_value = st.number_input("現值｜土地公告現值（萬元）", min_value=0.0, value=1000.0, key="cur_land")
current_house_value = st.number_input("現值｜房屋評定現值（萬元）", min_value=0.0, value=200.0, key="cur_house")

# 資產登記與資金來源
st.header("🏷️ 資產登記與資金來源")
owner = st.radio("目前登記在誰名下？", ["父母", "子女"], key="owner_select")

transfer_type = ""
fund_source = ""
if owner == "父母":
    transfer_type = st.radio("將來打算如何移轉給子女？", ["留待繼承", "贈與房產"], key="transfer_type")
else:
    fund_source = st.radio("子女購屋資金來源為？", ["自行購屋", "父母贈與現金"], key="fund_source")

# 贈與／繼承當下的三種價格（若父母持有）
gift_price = gift_land = gift_house = 0.0
if owner == "父母":
    st.header("🎁 贈與或繼承時的價格")
    gift_price = st.number_input("贈與或繼承時的市價（萬元）", min_value=0.0, value=3000.0, key="gift_price")
    gift_land = st.number_input("贈與或繼承時的土地公告現值（萬元）", min_value=0.0, value=1000.0, key="gift_land")
    gift_house = st.number_input("贈與或繼承時的房屋評定現值（萬元）", min_value=0.0, value=200.0, key="gift_house")

# 預估未來出售資料
st.header("📈 預估未來出售資訊")
future_price = st.number_input("預估未來出售價格（萬元）", min_value=0.0, value=3800.0, key="future_price")
future_land_value = st.number_input("預估未來土地公告現值（萬元）", min_value=0.0, value=1200.0, key="future_land")
future_house_value = st.number_input("預估未來房屋評定現值（萬元）", min_value=0.0, value=250.0, key="future_house")

# 基本參數
st.header("⏳ 其他基本條件")
holding_years = st.number_input("子女持有年數", min_value=0, value=2, key="holding_year")
is_self_use = st.checkbox("是否為自用住宅", value=False, key="self_use")

st.markdown("---")
st.success("✅ 已整合三階段價格輸入欄位，可進一步加入完整試算邏輯與稅負分析。")
