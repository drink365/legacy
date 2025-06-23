import streamlit as st

# 頁面設定
st.set_page_config(page_title="不動產稅負評估工具", layout="wide")
st.title("🏠 不動產稅負評估工具")
st.markdown("請依據實際情境輸入資料，系統將自動試算各類稅負。")

# 房產基本資訊輸入
st.header("📌 房產基本資訊（取得時）")
current_price = st.number_input("市價（萬元）", min_value=0.0, value=3000.0)
current_land_value = st.number_input("土地公告現值（萬元）", min_value=0.0, value=1000.0)
current_house_value = st.number_input("房屋評定現值（萬元）", min_value=0.0, value=250.0)

# 資產登記與未來規劃
st.header("🏷️ 資產登記與未來規劃")
owner = st.radio("目前房產登記在誰名下？", ["父母", "子女"])
if owner == "父母":
    transfer_type = st.radio("未來打算如何移轉？", ["留待繼承", "贈與房產"])
else:
    transfer_type = "自行購屋"

# 移轉時資訊
if transfer_type in ["贈與房產", "留待繼承"]:
    st.header("📦 移轉時資產價值（預估）")
    transfer_land_value = st.number_input("贈與／繼承時 土地公告現值（萬元）", min_value=0.0, value=1100.0)
    transfer_house_value = st.number_input("贈與／繼承時 房屋評定現值（萬元）", min_value=0.0, value=240.0)
else:
    transfer_land_value = current_land_value
    transfer_house_value = current_house_value

# 出售資訊
st.header("📈 未來出售資訊")
sell_price = st.number_input("預估未來出售價格（萬元）", min_value=0.0, value=3800.0)
sell_land_value = st.number_input("未來出售時 土地公告現值（萬元）", min_value=0.0, value=1200.0)
sell_house_value = st.number_input("未來出售時 房屋評定現值（萬元）", min_value=0.0, value=230.0)

# 其他條件
st.header("⏳ 其他條件")
holding_years = st.number_input("子女持有年數", min_value=0, value=2)
is_self_use = st.checkbox("是否為自用住宅", value=True)

# ⬇️ 稅負計算邏輯區 ⬇️

# ➤ 房地合一稅（賣方）
if transfer_type == "自行購屋":
    cost_basis = current_price  # 自行購屋：成本為購買市價
elif transfer_type == "贈與房產":
    cost_basis = transfer_land_value + transfer_house_value  # 贈與：視為原持有價值
else:  # 留待繼承
    cost_basis = transfer_land_value + transfer_house_value  # 繼承起算

capital_gain = sell_price - cost_basis
rgh_tax_rate = 0.45 if holding_years <= 2 else (
    0.35 if holding_years <= 5 else (
        0.10 if is_self_use and holding_years >= 6 else (
            0.20 if holding_years <= 10 else 0.15)))
deduct = 400 if is_self_use and holding_years >= 6 else 0
rgh_taxable = max(capital_gain - deduct, 0)
real_estate_tax = rgh_taxable * rgh_tax_rate
real_estate_note = f"({sell_price:.1f} - {cost_basis:.1f}" + (f" - 400" if deduct else "") + f") × {int(rgh_tax_rate*100)}%"

# ➤ 土地增值稅（賣方或贈與人）
land_increase = sell_land_value - current_land_value
if transfer_type == "留待繼承":
    land_tax = 0
    land_tax_note = "繼承免繳"
else:
    if is_self_use:
        land_tax = land_increase * 0.10
        land_tax_note = f"{land_increase:.1f} × 10%"
    else:
        a = min(land_increase, 400)
        b = min(max(land_increase - 400, 0), 400)
        c = max(land_increase - 800, 0)
        land_tax = a * 0.2 + b * 0.3 + c * 0.4
        land_tax_note = f"{a}×20% + {b}×30% + {c}×40%"

# ➤ 契稅（買方或受贈人）
if transfer_type == "贈與房產":
    deed_tax = transfer_house_value * 0.06
    deed_tax_note = f"{transfer_house_value:.1f} × 6%"
elif transfer_type == "自行購屋":
    deed_tax = current_house_value * 0.06
    deed_tax_note = f"{current_house_value:.1f} × 6%"
else:
    deed_tax = 0
    deed_tax_note = "繼承免繳"

# ➤ 印花稅（買方或受贈人）
if transfer_type in ["贈與房產", "自行購屋"]:
    stamp_tax = sell_price * 0.001
    stamp_tax_note = f"{sell_price:.1f} × 0.1%"
else:
    stamp_tax = 0
    stamp_tax_note = "繼承免繳"

# ➤ 贈與稅（贈與者）
def calc_gift_tax(value):
    base = max(value - 244, 0)
    if base <= 2811:
        return base * 0.10, f"({value} - 244) × 10%"
    elif base <= 5621:
        return base * 0.15 - 140.55, f"({value} - 244) × 15% - 140.55"
    else:
        return base * 0.20 - 421.6, f"({value} - 244) × 20% - 421.6"

gift_tax = 0
gift_note = "無"
if transfer_type == "贈與房產":
    gift_tax, gift_note = calc_gift_tax(transfer_land_value + transfer_house_value)

# ➤ 遺產稅（繼承人）
def calc_estate_tax(value):
    base = max(value - 1333, 0)
    if base <= 5621:
        return base * 0.10, f"({value} - 1333) × 10%"
    elif base <= 11242:
        return base * 0.15 - 281.05, f"({value} - 1333) × 15% - 281.05"
    else:
        return base * 0.20 - 842.3, f"({value} - 1333) × 20% - 842.3"

estate_tax = 0
estate_note = "無"
if transfer_type == "留待繼承":
    estate_tax, estate_note = calc_estate_tax(transfer_land_value + transfer_house_value)

# ⬇️ 顯示區域 ⬇️
st.header("📊 稅負明細與說明")

# 條件摘要
st.markdown(f"**目前登記**：{owner}｜**規劃方式**：{transfer_type}｜**是否自用**：{'是' if is_self_use else '否'}｜**子女持有年數**：{holding_years}年")

# 明細表
st.markdown(f"""
### 💼 賣方／贈與人／被繼承人 應繳稅負

- 房地合一稅：約 **{real_estate_tax:.1f} 萬元**（{real_estate_note}）
- 土地增值稅：約 **{land_tax:.1f} 萬元**（{land_tax_note}）
- 贈與稅：約 **{gift_tax:.1f} 萬元**（{gift_note}）
- 遺產稅：約 **{estate_tax:.1f} 萬元**（{estate_note}）

### 🧾 買方／受贈人 應繳稅負

- 契稅：約 **{deed_tax:.1f} 萬元**（{deed_tax_note}）
- 印花稅：約 **{stamp_tax:.1f} 萬元**（{stamp_tax_note}）

---

💰 **總稅負合計**（含雙方）：約 **{real_estate_tax + land_tax + gift_tax + estate_tax + deed_tax + stamp_tax:.1f} 萬元**
""")

# 頁尾
st.markdown("---")
st.markdown("""
<div style='text-align:center; font-size:14px; color:gray;'>
由《影響力》傳承策略平台｜永傳家族辦公室 提供
｜ https://gracefo.com ｜ 聯絡信箱：123@gracefo.com
</div>
""", unsafe_allow_html=True)
