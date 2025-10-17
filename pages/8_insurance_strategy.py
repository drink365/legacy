# -*- coding: utf-8 -*-
from __future__ import annotations
import streamlit as st
import pandas as pd
import sys, os

# 確保頁面配置並載入共用函數
ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
# 假設 ui_shared 檔案存在於專案根目錄
try:
    from ui_shared import ensure_page_config, render_header, render_footer
except ImportError:
    # Fallback if ui_shared is not available (for demonstration)
    def ensure_page_config(title=""): st.set_page_config(page_title=title, layout="wide")
    def render_header(): st.title("永傳數位家族辦公室")
    def render_footer(): st.write("---"); st.caption("© 永傳數位家族辦公室")

ensure_page_config('保單策略模組')
render_header()

# ---------------- 稅制常數（台灣贈與稅 - 簡化版） ----------------
# 台灣贈與稅制簡化常數 (以 114年/2025 年免稅額 NT$ 244萬為基礎)
EXEMPTION    = 2_440_000    # 年免稅額（單一贈與人）
RATE_10      = 0.10         # 贈與淨額 NT$ 2500萬以下稅率
BR10_NET_MAX = 25_000_000   # 10% 稅率淨額上限 (簡化)
RATE_15      = 0.15         # 贈與淨額 NT$ 2500萬到 5000萬稅率
BR15_NET_MAX = 50_000_000   # 15% 稅率淨額上限 (簡化)
RATE_20      = 0.20         # 贈與淨額 NT$ 5000萬以上稅率

def calculate_gift_tax(net_gift_amount: float) -> float:
    """計算贈與淨額應納贈與稅 (台灣稅制分級累進簡化)。"""
    if net_gift_amount <= 0:
        return 0
    
    tax = 0.0
    remaining_amount = net_gift_amount

    # 20% 稅率 (超過 5000萬部分)
    if remaining_amount > BR15_NET_MAX:
        taxable_20 = remaining_amount - BR15_NET_MAX
        tax += taxable_20 * RATE_20
        remaining_amount = BR15_NET_MAX

    # 15% 稅率 (2500萬到 5000萬部分)
    if remaining_amount > BR10_NET_MAX:
        taxable_15 = remaining_amount - BR10_NET_MAX
        tax += taxable_15 * RATE_15
        remaining_amount = BR10_NET_MAX

    # 10% 稅率 (2500萬以下部分)
    tax += remaining_amount * RATE_10
    
    return tax

def fmt_y(amount: float) -> str:
    """格式化金額為易讀的千分位字串。"""
    return f"{int(amount):,}"

def calculate_insurance_gift_simulation(
    annual_cash_flow: int, 
    change_year: int, 
    cv_ratio_at_change: float
) -> tuple[pd.DataFrame, float, float]:
    """計算保單變更要保人與現金贈與的稅務差異模擬。"""
    
    yearly_data = []
    
    # 累積值
    cumulative_tax_cash = 0.0
    
    # 執行年度模擬
    for year in range(1, change_year + 1):
        annual_input = annual_cash_flow

        # ------------------- 情境 A：現金贈與 -------------------
        # 假設每年都贈與現金，並每年使用免稅額
        gift_cash = annual_input
        net_gift_cash = max(0, gift_cash - EXEMPTION)
        tax_cash = calculate_gift_tax(net_gift_cash)
        cumulative_tax_cash += tax_cash

        # ------------------- 情境 B：保單變更要保人 -------------------
        tax_insurance = 0.0
        gift_insurance = 0.0
        
        # 第 N 年：變更要保人，贈與價值為累積保費的 CV 比例
        if year == change_year:
            cumulative_premium = annual_cash_flow * change_year
            gift_insurance = cumulative_premium * cv_ratio_at_change
            
            # 贈與淨額 = CV - 免稅額 (只在變更年計算一次贈與稅)
            net_gift_insurance = max(0, gift_insurance - EXEMPTION)
            tax_insurance = calculate_gift_tax(net_gift_insurance)

        yearly_data.append({
            "年度": year,
            "現金投入（元）": annual_input,
            "現金贈與稅累計（元）": cumulative_tax_cash,
            "保單：累積保費（元）": annual_cash_flow * year,
            "保單：變更時贈與值（元）": gift_insurance if year == change_year else 0,
            "保單：變更時應納稅（元）": tax_insurance if year == change_year else 0,
        })
        
    df = pd.DataFrame(yearly_data)
    
    # 最終結果總結
    total_tax_cash = cumulative_tax_cash # 現金贈與是每年發生，已在循環中累積
    total_tax_insurance = df["保單：變更時應納稅（元）"].sum() # 保單贈與只在變更年發生一次

    return df, total_tax_cash, total_tax_insurance

# ---------------- 頁面內容 ----------------

st.subheader("📦 保單策略｜智慧傳承引擎")
st.markdown("保單是家族資產守護與傳承藍圖的**核心配置**。透過**要保人變更**、**保額分層**與**分期給付（類信託）**等精妙設計，在合規前提下，達成資產安全、稅務效率與金流秩序三大目標。")

st.markdown("---")
st.markdown("#### 🎁 贈與稅務效率模擬：現金 vs. 保單變更要保人")

st.caption("透過將現金流轉為保單，利用保單價值準備金（CV）在特定年期內低於已繳保費的特性，**壓縮贈與價值**，達到稅務效率。")

# 模擬參數輸入
with st.form("insurance_strategy_form"):
    c1, c2 = st.columns(2)
    with c1:
        annual_cash_flow = st.number_input(
            "每年可運用現金流 (Premium/Gift)",
            min_value=1_000_000,
            max_value=100_000_000,
            value=10_000_000,
            step=1_000_000,
            format="%d"
        )
        change_year = st.slider(
            "決定變更要保人的年份 (第 N 年)", 
            min_value=2, max_value=10, value=5
        )
    
    with c2:
        st.markdown("請輸入第 N 年時，保單價值準備金 (CV) 佔**累積**保費的比例 (%)")
        cv_ratio_at_change_percent = st.slider(
            f"第 {change_year} 年 CV/累積保費 (%)", 
            min_value=10, max_value=100, value=65, step=5
        )
        cv_ratio_at_change = cv_ratio_at_change_percent / 100.0
        
    st.markdown("---")
    submitted = st.form_submit_button("執行模擬計算", type="primary")

if submitted:
    # 執行計算
    df_result, total_tax_cash, total_tax_insurance = calculate_insurance_gift_simulation(
        annual_cash_flow, change_year, cv_ratio_at_change
    )

    st.markdown(f"#### 📊 模擬結果摘要 (至第 {change_year} 年)")
    
    col_sum1, col_sum2, col_sum3 = st.columns(3)
    
    with col_sum1:
        st.metric(
            "總現金流投入", 
            f"NT$ {fmt_y(annual_cash_flow * change_year)}"
        )
    
    with col_sum2:
        # 情境 A 摘要
        taxable_base_cash = max(0, annual_cash_flow - EXEMPTION) * change_year
        st.metric(
            "情境 A：現金贈與**總稅額**", 
            f"NT$ {fmt_y(total_tax_cash)}",
            delta=f"總應稅淨額：NT$ {fmt_y(taxable_base_cash)}"
        )

    with col_sum3:
        # 情境 B 摘要
        gift_val_insurance = df_result['保單：變更時贈與值（元）'].iloc[-1]
        taxable_base_insurance = max(0, gift_val_insurance - EXEMPTION)
        st.metric(
            "情境 B：保單變更**總稅額**", 
            f"NT$ {fmt_y(total_tax_insurance)}",
            delta=f"總應稅淨額：NT$ {fmt_y(taxable_base_insurance)}"
        )
        
    # 節稅效果分析
    if total_tax_cash > total_tax_insurance:
        savings = total_tax_cash - total_tax_insurance
        st.success(f"🎉 **保單變更要保人** 策略共節省贈與稅 **NT$ {fmt_y(savings)}**", icon="💰")
    elif total_tax_cash < total_tax_insurance:
        st.warning("⚠️ 此情境下，保單策略的贈與稅負可能更高，建議調整變更年期或確認保單 CV 比例。")
    else:
        st.info("兩者稅負相同，但保單提供了額外的保障與金流秩序性。")

    st.markdown("---")
    st.markdown(f"#### 📜 年度明細表 (至變更年第 {change_year} 年)")
    
    # 格式化顯示的 DataFrame
    df_show = df_result.copy()
    for col in df_show.columns:
        if "（元）" in col:
            # 確保年度欄位不被格式化
            df_show[col] = df_show[col].apply(lambda x: fmt_y(x) if x > 0 or col == '現金投入（元）' else '—')
    
    st.dataframe(df_show, use_container_width=True, hide_index=True)

    # 匯出 CSV (使用未格式化的原始數據)
    csv_bytes = df_result.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "下載模擬明細 (CSV)",
        data=csv_bytes,
        file_name="保單策略_贈與稅模擬明細.csv",
        mime="text/csv"
    )

st.markdown("---")
st.markdown("### 🔑 核心策略亮點：分期給付 (類信託)")
st.write("除了贈與稅務效率，壽險最大的價值在於**傳承秩序**。利用保險契約的條款設計，指定受益人**分期領取**保險金，而非一次領取。此舉能：")
st.markdown("""
* **確保金流秩序**：避免受益人一次性獲得大額資金後不當使用，達成類似**信託目的**的資產管理效果。
* **拉長照護年期**：用於長輩照護或子女教育金時，能確保資金能穩定供應至特定年限或達成特定條件。
* **高度確定性**：保單契約一旦生效，給付條件具備法律約束力，執行效率高。
* **債權隔離**：在法律允許的範圍內，保險金受法律保護，具有一定的債權隔離功能，守護資產安全。
""")
st.markdown("---")
st.page_link("pages/5_estate_tax.py", label="搭配遺產/贈與稅敏感度模組 →", use_container_width=True)


render_footer()
