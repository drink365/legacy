# app.py — 保單規劃｜用同樣現金流，更聰明完成贈與（1～3 年極簡版＋8點好處＋明細表＋下載）
# 執行：streamlit run app.py
# 需求：pip install streamlit pandas

import pandas as pd
import streamlit as st
from typing import Tuple

st.set_page_config(page_title="保單規劃｜用同樣現金流，更聰明完成贈與", layout="wide")

# ---------------- 稅制常數（114年/2025） ----------------
EXEMPTION    = 2_440_000    # 年免稅額（單一贈與人）
BR10_NET_MAX = 28_110_000   # 10% 淨額上限
BR15_NET_MAX = 56_210_000   # 15% 淨額上限
RATE_10, RATE_15, RATE_20 = 0.10, 0.15, 0.20
MAX_ANNUAL   = 100_000_000  # 每年現金投入上限：1 億

# ---------------- 初始化 Session State ----------------
# 確保所有需要的鍵都在 Session State 中
DEFAULTS = {
    "change_year": 1,
    "y1_prem": 10_000_000,
    "y2_prem": 10_000_000,
    "y3_prem": 10_000_000,
    "y1_cv":   5_000_000,
    "y2_cv":  14_000_000,
    "y3_cv":  24_000_000,
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v
    # 確保 y2_prem 和 y3_prem 初始值與 y1_prem 同步
    if k.startswith('y1_prem'):
         st.session_state["y2_prem"] = st.session_state["y1_prem"]
         st.session_state["y3_prem"] = st.session_state["y1_prem"]

# ---------------- 樣式 ----------------
st.markdown(
    """
<style>
:root { --ink:#0f172a; --sub:#475569; --line:#E6E8EF; --bg:#FAFBFD; --gold:#C8A96A; --emerald:#059669; --green-light:#ecfdf5;}
.block-container { max-width:1320px; padding-top:1rem; padding-bottom:2rem; }
hr.custom{ border:none; border-top:1px solid var(--line); margin:12px 0 6px; }
.small{ color:var(--sub); font-size:.95rem; line-height:1.6; }

/* 基礎 KPI 卡片 */
.kpi{ border:1px solid var(--line); border-left:5px solid var(--gold); border-radius:12px; padding:14px 16px; background:#fff; box-shadow:0 1px 2px rgba(10,22,70,.04);}
.kpi .label{ color:var(--sub); font-size:.95rem; margin-bottom:6px;}
.kpi .value{ font-weight:700; font-variant-numeric:tabular-nums; font-size:1.05rem; }
.kpi .note{ color:var(--emerald); font-size:.9rem; margin-top:4px; }

/* 稅務節省突出卡片 */
.kpi.highlight { border-left-color: var(--emerald); background:var(--green-light); border-color: var(--emerald); }
.kpi.highlight .value { font-size: 1.15rem; color: var(--emerald); }

.section{ background:var(--bg); border:1px solid var(--line); border-radius:14px; padding:16px; }
.footer-note{ margin-top:18px; padding:14px 16px; border:1px dashed var(--line); background:#fff; border-radius:12px; color:#334155; font-size:.92rem; }
.benefit-list li { margin-bottom: 12px; line-height: 1.6; }

/* 讓 Streamlit subheaders 更有質感 */
h2 {
    border-bottom: 2px solid var(--line);
    padding-bottom: 8px;
    margin-top: 1.5rem !important;
}
</style>
""",
    unsafe_allow_html=True
)

def card(label: str, value: str, note: str = "", style_class: str = ""):
    """生成 KPI 卡片的 HTML 結構，可選樣式類別"""
    html = f'<div class="kpi {style_class}"><div class="label">{label}</div><div class="value">{value}</div>'
    if note: html += f'<div class="note">{note}</div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

def fmt(n: float) -> str: return f"{n:,.0f}"
def fmt_y(n: float) -> str: return f"{fmt(n)} 元"

def tax_calc(net: int) -> Tuple[int, str]:
    """計算贈與稅額和適用稅率"""
    if net <= 0: return 0, "—"
    net_float = float(net)
    
    if net_float <= BR10_NET_MAX: return int(round(net_float * RATE_10)), "10%"
    if net_float <= BR15_NET_MAX:
        base = BR10_NET_MAX * RATE_10
        extra = (net_float - BR10_NET_MAX) * RATE_15
        return int(round(base + extra)), "15%"
    
    base = BR10_NET_MAX * RATE_10 + (BR15_NET_MAX - BR10_NET_MAX) * RATE_15
    extra = (net_float - BR15_NET_MAX) * RATE_20
    return int(round(base + extra)), "20%"

def _on_prem_change():
    """年繳保費變動時，同步其他年份保費，並建議重置 CV 以確保數據準確"""
    p = int(st.session_state.y1_prem)
    st.session_state.y2_prem = p
    st.session_state.y3_prem = p
    # 當保費大幅變動時，保價金幾乎會失真，因此建議重置為 0 讓使用者重新輸入
    # st.session_state.y1_cv = 0
    # st.session_state.y2_cv = 0
    # st.session_state.y3_cv = 0
    # 由於 CV 是重要輸入，為了避免使用者覺得麻煩，這邊不強制重置，讓使用者自行調整

# ---------------- 標題與摘要 ----------------
st.title("保單規劃｜用同樣現金流，更聰明完成贈與")
st.caption("單位：新台幣。稅制假設（114年/2025）：年免稅 $2,440,000$；10% 淨額上限 $28,110,000$；15% 淨額上限 $56,210,000$。")

# ---------------- 輸入：保費與交棒年份 ----------------
col_prem, col_year = st.columns([2, 1])

with col_prem:
    st.number_input("💸 每年現金投入（年繳保費，元）",
        min_value=0, max_value=MAX_ANNUAL,
        step=1_000_000, format="%d",
        key="y1_prem", on_change=_on_prem_change)

with col_year:
    st.selectbox("⏲️ 第幾年變更要保人（交棒贈與）",
        options=[1, 2, 3], index=0, key="change_year",
        help="選擇在哪一年將保單要保人變更給子女，以此時的保價金作為贈與價值。")

st.markdown('<hr class="custom">', unsafe_allow_html=True)

# ---------------- 輸入：保價金 ----------------
p = int(st.session_state.y1_prem)
# 計算各年度累積投入的最大值作為保價金輸入的上限（邏輯上保價金不應超過累積投入）
max_y1 = p * 1
max_y2 = p * 2
max_y3 = p * 3

st.subheader("📊 前三年保價金（年末現金價值）")
st.markdown("<p class='small'>由於保價金（CV）數值取決於保險商品設計，請<strong>手動輸入</strong>各年度預估的年末現金價值。CV不得超過當年度累積投入金額。</p>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    st.number_input("第 1 年保價金（元）", min_value=0, max_value=max_y1, step=100_000, format="%d", key="y1_cv")
with c2:
    st.number_input("第 2 年保價金（元）", min_value=0, max_value=max_y2, step=100_000, format="%d", key="y2_cv")
with c3:
    st.number_input("第 3 年保價金（元）", min_value=0, max_value=max_y3, step=100_000, format="%d", key="y3_cv")

# ---------------- 年度資料與計算 ----------------
def build_schedule_3y():
    """建立 3 年度的投入與保價金資料表"""
    rows, cum = [], 0
    for y in (1, 2, 3):
        premium = int(st.session_state.y1_prem)
        cum += premium
        cv = int(st.session_state[f"y{y}_cv"])
        rows.append({"年度": y, "每年投入（元）": premium, "累計投入（元）": cum, "年末現金價值（元）": cv})
    return pd.DataFrame(rows)

df_years = build_schedule_3y()
change_year = int(st.session_state.change_year)

# 1. 保單規劃模式 (變更要保人)
# 變更當年，贈與價值 = 當年保單價值準備金 (CV)
cv_at_change = int(df_years.loc[df_years["年度"] == change_year, "年末現金價值（元）"].iloc[0])
# 名目累積移轉金額（用於 KPI 卡片顯示）
nominal_transfer_to_N = int(df_years.loc[df_years["年度"] <= change_year, "每年投入（元）"].sum())

gift_with_policy = cv_at_change
net_with_policy  = max(0, gift_with_policy - EXEMPTION)
tax_with_policy, rate_with = tax_calc(net_with_policy)

# 2. 現金贈與模式 (逐年贈與)
total_tax_no_policy, yearly_tax_list = 0, []
for _, r in df_years[df_years["年度"] <= change_year].iterrows():
    annual_i = int(r["每年投入（元）"])
    net = max(0, annual_i - EXEMPTION)
    t, rate = tax_calc(net)
    total_tax_no_policy += t
    yearly_tax_list.append({
        "年度": int(r["年度"]),
        "現金贈與（元）": annual_i,
        "免稅後淨額（元）": net,
        "應納贈與稅（元）": t,
        "適用稅率": rate
    })

# 3. 差異計算
tax_saving     = total_tax_no_policy - tax_with_policy
saving_label   = "節省之贈與稅" if tax_saving >= 0 else "增加之贈與稅"
saving_note    = "保單規劃優於現金贈與" if tax_saving > 0 else ""
saving_style   = "highlight" if tax_saving > 0 else ""


# ---------------- 成果指標卡 ----------------
st.markdown('<hr class="custom">', unsafe_allow_html=True)
st.subheader("💡 贈與方案比較結果")
colA, colB, colC = st.columns(3)

# A: 保單規劃模式
with colA:
    st.markdown(f"**保單規劃（第 {change_year} 年變更要保人）**")
    card(f"累積投入（名目）至第 {change_year} 年", fmt_y(nominal_transfer_to_N))
    card("變更當年視為贈與（保單價值準備金）", fmt_y(gift_with_policy))
    card("總應納贈與稅", fmt_y(tax_with_policy), note=f"單次贈與，適用稅率 {rate_with}")

# B: 現金贈與模式
with colB:
    st.markdown(f"**現金贈與（第 1～{change_year} 年逐年贈與）**")
    card(f"累積投入（名目）至第 {change_year} 年", fmt_y(nominal_transfer_to_N))
    # 這裡顯示逐年贈與的贈與價值總和，應與名目投入相同，但卡片強調稅額
    card("累計贈與稅", fmt_y(total_tax_no_policy), note="逐年單獨計算稅負後加總")

# C: 稅負差異
with colC:
    st.markdown("**稅負差異 (策略效益)**")
    # 將節稅金額放在顯眼卡片
    card(f"總 {saving_label}", fmt_y(abs(tax_saving)), note=saving_note, style_class=saving_style)
    # 放置一個簡單的空白卡片填補空間
    st.markdown('<div class="kpi" style="border:1px dashed var(--line); border-left:none; background:#fff; height:93px;"><div class="label" style="text-align:center;">策略目的：用最低稅負完成資產移轉</div></div>', unsafe_allow_html=True)


# ---------------- 明細（收合＋下載 CSV） ----------------
st.markdown("")  # 空一行
with st.expander("📝 年度明細與逐年稅額（點擊展開）", expanded=False):
    st.markdown("**年度現金價值（1～3 年投入與 CV 資訊）**")
    df_show = df_years.assign(
        **{
            "每年投入（元）": lambda d: d["每年投入（元）"].map(fmt),
            "累計投入（元）": lambda d: d["累計投入（元）"].map(fmt),
            "年末現金價值（元）": lambda d: d["年末現金價值（元）"].map(fmt),
        }
    )
    st.dataframe(df_show, use_container_width=True, hide_index=True)

    st.markdown("---")

    st.markdown("**現金贈與：逐年稅額試算（第 1～變更年）**")
    df_no = pd.DataFrame(sorted(yearly_tax_list, key=lambda x: x["年度"]))
    df_no_show = df_no.copy()
    for c in ["現金贈與（元）", "免稅後淨額（元）", "應納贈與稅（元）"]:
        df_no_show[c] = df_no_show[c].map(fmt_y)
    st.dataframe(df_no_show, use_container_width=True, hide_index=True)

    st.markdown("---")

    # 匯出 CSV
    csv_all = pd.concat([df_years, df_no.drop(columns=["年度"], errors='ignore')], axis=1) # 避免年度重複
    csv_bytes = csv_all.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "💾 下載完整明細（CSV）",
        data=csv_bytes,
        file_name="保單贈與稅務規劃明細.csv",
        mime="text/csv",
        type="primary"
    )

# ---------------- 8 點好處 ----------------
st.subheader("✅ 贈與完成後：可達成之八大效果")
st.markdown(
    f"""
<ul class="benefit-list">
<li>1️⃣ **降低一代資產與贈與稅負**：
至第 {change_year} 年，**一代資產壓縮額**約為名目累積投入 **{fmt_y(nominal_transfer_to_N)}**。透過**變更要保人**，以保價金認列贈與價值，可**降低總贈與稅負**（相較現金逐年贈與），實現稅務效率。</li>

<li>2️⃣ **資產傳承的放大效果**：
資產置於銀行，價值為 $1:1$；但放進保單，可透過身價保障機制，為家族提供**倍數效果**的流動性資金。</li>

<li>3️⃣ **財富公平調控**：
銀行存款須依民法平均分配，但保單受益人可**彈性指定**，能針對資產差異較大的子女進行差額補強或特殊安排，落實傳承意圖。</li>

<li>4️⃣ **分期給付的秩序性**：
保單可透過**類信託**的方式進行分期給付，不僅能保障資產分配的秩序，還能避免額外的信託管理費用，更具成本效益。</li>

<li>5️⃣ **預留二代稅源**：
保單的身故保險金可作為**稅源預備金**，避免後代因繳納遺產稅或其他稅負，被迫在不當時機處分資產。</li>

<li>6️⃣ **完成資產快速移轉**：
透過要保人變更，快速完成資產名義上的歸屬移轉，避免資產過度集中在一代名下，有助於**整體家族資產的壓縮**。</li>

<li>7️⃣ **遺產外的即時現金**：
保險金屬於**遺產外的即時現金**，繼承人可快速取得，緩解繼承時可能面臨的資金需求。</li>

<li>8️⃣ **資產的專款專用**：
保單可確保資金流向指定受益人，實現資產的**專款專用**意圖，減少家庭紛爭。</li>
</ul>
"""
,
    unsafe_allow_html=True
)

# ---------------- 重要提醒 ----------------
st.markdown(
    """
<div class="footer-note">
<b>⚠️ 重要提醒：</b>本頁內容僅為示範與教育性說明參考，實際權利義務以<strong>保單條款</strong>、
保險公司<strong>核保／保全規定</strong>與<strong>個別化規劃文件</strong>為準。稅制數值採目前假設，
若法規調整，請以最新公告為準。
</div>
""",
    unsafe_allow_html=True
)
