import streamlit as st
import pandas as pd

# 頁面設定
st.set_page_config(page_title="不動產三種取得情境稅負比較", layout="wide")

st.title("🏡 三種不動產取得方式稅負比較")
st.markdown("比較房地產以三種方式取得（自行購屋、父母贈與、父母繼承）時的稅負差異。")

# 輸入參數
st.header("📌 基本資料輸入")
col1, col2, col3 = st.columns(3)
with col1:
    current_price = st.number_input("市價（萬元）", value=3000.0, min_value=0.0)
with col2:
    land_value = st.number_input("土地公告現值（萬元）", value=1000.0, min_value=0.0)
with col3:
    house_value = st.number_input("房屋評定現值（萬元）", value=200.0, min_value=0.0)

col4, col5 = st.columns(2)
with col4:
    future_price = st.number_input("預估未來出售價格（萬元）", value=3800.0, min_value=0.0)
with col5:
    holding_years = st.number_input("持有年數", value=3, min_value=0)

is_self_use = st.checkbox("是否為自用住宅", value=False)

# 稅率與級距設定
def 房地合一稅率(holding_years, is_self_use):
    if holding_years <= 2:
        return 0.45
    elif holding_years <= 5:
        return 0.35
    elif holding_years <= 10 and not is_self_use:
        return 0.20
    elif holding_years > 10 and not is_self_use:
        return 0.15
    elif holding_years >= 6 and is_self_use:
        return 0.10
    else:
        return 0.35

def 房地合一稅額(成本, 未來市價, holding_years, is_self_use):
    利得 = 未來市價 - 成本
    if holding_years >= 6 and is_self_use:
        利得 -= 400
        利得 = max(利得, 0)
    稅率 = 房地合一稅率(holding_years, is_self_use)
    return 利得 * 稅率

def 土地增值稅(土地現值, 原公告, 是否自用):
    增值 = 土地現值 - 原公告
    if 是否自用:
        return 增值 * 0.10
    first = min(增值, 400)
    second = min(max(增值 - 400, 0), 400)
    third = max(增值 - 800, 0)
    return first * 0.2 + second * 0.3 + third * 0.4

def 贈與稅(公告總值):
    扣除額 = 244
    淨贈與 = max(公告總值 - 扣除額, 0)
    if 淨贈與 <= 2811:
        return 淨贈與 * 0.10
    elif 淨贈與 <= 5621:
        return 淨贈與 * 0.15 - 140.55
    else:
        return 淨贈與 * 0.20 - 421.6

def 遺產稅(公告總值):
    扣除額 = 1333
    淨遺產 = max(公告總值 - 扣除額, 0)
    if 淨遺產 <= 5621:
        return 淨遺產 * 0.10
    elif 淨遺產 <= 11242:
        return 淨遺產 * 0.15 - 281.05
    else:
        return 淨遺產 * 0.20 - 842.3

def 契稅(房屋現值):
    return 房屋現值 * 0.06

def 印花稅(成交價):
    return 成交價 * 0.001

# 情境一：自行購屋
成本1 = current_price
房地合一1 = 房地合一稅額(成本1, future_price, holding_years, is_self_use)
土地增值1 = 土地增值稅(land_value, land_value, is_self_use)
契稅1 = 契稅(house_value)
印花1 = 印花稅(current_price)
贈與1 = 0
遺產1 = 0

# 情境二：父母贈與
贈與公告總值 = land_value + house_value
成本2 = 贈與公告總值
房地合一2 = 房地合一稅額(成本2, future_price, holding_years, is_self_use)
土地增值2 = 土地增值稅(land_value, land_value * 0.8, is_self_use)
契稅2 = 契稅(house_value)
印花2 = 印花稅(current_price)
贈與2 = 贈與稅(贈與公告總值)
遺產2 = 0

# 情境三：父母繼承
繼承公告總值 = land_value + house_value
成本3 = 繼承公告總值
房地合一3 = 房地合一稅額(成本3, future_price, holding_years, is_self_use)
土地增值3 = 0
契稅3 = 0
印花3 = 0
贈與3 = 0
遺產3 = 遺產稅(繼承公告總值)

# 顯示表格
df = pd.DataFrame({
    "情境": ["自行購屋", "父母贈與", "父母繼承"],
    "房地合一稅": [房地合一1, 房地合一2, 房地合一3],
    "土地增值稅": [土地增值1, 土地增值2, 土地增值3],
    "契稅": [契稅1, 契稅2, 契稅3],
    "印花稅": [印花1, 印花2, 印花3],
    "贈與稅": [贈與1, 贈與2, 贈與3],
    "遺產稅": [遺產1, 遺產2, 遺產3],
})

df["總稅負"] = df[["房地合一稅", "土地增值稅", "契稅", "印花稅", "贈與稅", "遺產稅"]].sum(axis=1)

st.header("📊 各情境稅負比較表")
st.dataframe(df.style.format("{:.1f}"))
