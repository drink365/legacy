# -*- coding: utf-8 -*-
import streamlit as st
from ui_shared import ensure_page_config, render_header, render_footer
from typing import List

# ------------------------------
# 稅制常數 (根據使用者提供之最新資訊)
# ------------------------------

# 遺產稅 (Estate Tax) - 淨額級距
# 淨額5621萬以下10%
# 淨額5621萬～1億1242萬，15%
# 淨額1億1242萬以上，20%
ET_THRESHOLDS = [56_210_000, 112_420_000] # 超過此金額進入下一級距
ET_RATES      = [0.10, 0.15, 0.20]

# 贈與稅 (Gift Tax) - 淨額級距
# 淨額2811萬以下10%
# 淨額2811萬～5621萬，15%
# 淨額5621萬以上，20%
GT_THRESHOLDS = [28_110_000, 56_210_000] # 超過此金額進入下一級距
GT_RATES      = [0.10, 0.15, 0.20]
GT_EXEMPTION  = 2_440_000 # 每年贈與免稅額（113年，每人）

# ------------------------------
# 輔助函式
# ------------------------------

def fmt_y(amount: float) -> str:
    """格式化為台幣金額顯示"""
    return f"NT$ {amount:,.0f}"

def calculate_progressive_tax(net_amount: float, thresholds: List[int], rates: List[float]) -> float:
    """
    計算累進稅額。
    
    Args:
        net_amount (float): 應稅淨額。
        thresholds (List[int]): 級距的上限金額列表 (例如 [A, B])。
        rates (List[float]): 對應的稅率列表 (例如 [R1, R2, R3])。
        
    Returns:
        float: 應納稅額。
    """
    tax = 0.0
    remaining_amount = net_amount
    
    # 處理第一級距
    threshold_1 = thresholds[0]
    rate_1 = rates[0]
    
    if remaining_amount <= threshold_1:
        tax += remaining_amount * rate_1
        return tax

    tax += threshold_1 * rate_1
    remaining_amount -= threshold_1
    
    # 處理第二級距
    threshold_2 = thresholds[1]
    rate_2 = rates[1]
    
    taxable_2 = min(remaining_amount, threshold_2 - threshold_1) # 第二級距的課稅基礎
    tax += taxable_2 * rate_2
    remaining_amount -= taxable_2
    
    # 處理第三級距（最高級距）
    rate_3 = rates[2]
    tax += remaining_amount * rate_3

    return tax

# ------------------------------
# Streamlit UI 頁面
# ------------------------------

ensure_page_config('5 estate tax')
render_header()

st.subheader("💡 遺產/贈與稅｜敏感度與壓縮試算")
st.caption("本工具根據您提供的最新稅率級距（淨額制）進行試算，結果僅供參考。")

# -------------------- 稅別選擇與輸入 --------------------
col1, col2 = st.columns(2)
with col1:
    tax_type = st.selectbox(
        "選擇計算稅別",
        ["贈與稅 (Gift Tax)", "遺產稅 (Estate Tax)"],
        index=0,
        help="贈與稅適用於生前贈與，遺產稅適用於身後傳承。"
    )

with col2:
    if tax_type == "贈與稅 (Gift Tax)":
        gross_amount = st.number_input(
            "請輸入**年度總贈與金額** (NT$)", 
            min_value=0, 
            value=35_000_000, 
            step=1_000_000,
            format="%d",
            help="此為尚未扣除免稅額前的贈與總額。"
        )
        # 贈與稅淨額 = 總贈與金額 - 免稅額
        taxable_net_amount = max(0, gross_amount - GT_EXEMPTION)
        tax_thresholds = GT_THRESHOLDS
        tax_rates = GT_RATES
        tax_name = "贈與稅"
        st.markdown(f"年度免稅額：**{fmt_y(GT_EXEMPTION)}** (已預扣)")
    else: # 遺產稅 (Estate Tax)
        # 遺產稅計算複雜，此處為簡化版，假設已扣除免稅額及扣除額
        taxable_net_amount = st.number_input(
            "請輸入**遺產稅應納稅淨額** (NT$)", 
            min_value=0, 
            value=70_000_000, 
            step=1_000_000,
            format="%d",
            help="此淨額為遺產總額扣除免稅額、扣除額及農業用地等不計入項目後之金額。"
        )
        tax_thresholds = ET_THRESHOLDS
        tax_rates = ET_RATES
        tax_name = "遺產稅"
        st.markdown(f"應稅淨額：**{fmt_y(taxable_net_amount)}**")

# -------------------- 稅額計算 --------------------
st.markdown("---")

if taxable_net_amount > 0:
    total_tax = calculate_progressive_tax(taxable_net_amount, tax_thresholds, tax_rates)
    
    st.markdown(f"### 預估應納 {tax_name} 稅額")
    st.metric(f"應納 {tax_name} 總額", fmt_y(total_tax))
    
    # -------------------- 級距明細顯示 --------------------
    st.markdown("#### 應稅淨額分佈與稅率明細")
    
    threshold_1 = tax_thresholds[0]
    threshold_2 = tax_thresholds[1]
    rate_1, rate_2, rate_3 = tax_rates
    
    tax_details = []
    
    # 級距 1：10%
    taxable_1 = min(taxable_net_amount, threshold_1)
    tax_1 = taxable_1 * rate_1
    tax_details.append({
        "淨額區間": f"NT$ 0 ~ {fmt_y(threshold_1)}",
        "適用稅率": f"{rate_1*100:.0f}%",
        "應稅淨額": fmt_y(taxable_1),
        "應納稅額": fmt_y(tax_1)
    })
    
    remaining = taxable_net_amount - taxable_1
    
    # 級距 2：15%
    if remaining > 0:
        taxable_2_max = threshold_2 - threshold_1
        taxable_2 = min(remaining, taxable_2_max)
        tax_2 = taxable_2 * rate_2
        tax_details.append({
            "淨額區間": f"NT$ {fmt_y(threshold_1+1)} ~ {fmt_y(threshold_2)}",
            "適用稅率": f"{rate_2*100:.0f}%",
            "應稅淨額": fmt_y(taxable_2),
            "應納稅額": fmt_y(tax_2)
        })
        remaining -= taxable_2

    # 級距 3：20%
    if remaining > 0:
        tax_3 = remaining * rate_3
        tax_details.append({
            "淨額區間": f"NT$ {fmt_y(threshold_2+1)} 以上",
            "適用稅率": f"{rate_3*100:.0f}%",
            "應稅淨額": fmt_y(remaining),
            "應納稅額": fmt_y(tax_3)
        })

    # 轉換為 DataFrame 顯示
    import pandas as pd
    df_tax_details = pd.DataFrame(tax_details)
    st.dataframe(df_tax_details, hide_index=True, use_container_width=True)

else:
    st.success(f"應稅淨額為零，無需繳納 {tax_name}。")

st.markdown("---")

st.page_link("pages/8_insurance_strategy.py", label="回到保單策略模組 →", use_container_width=True)

render_footer()
