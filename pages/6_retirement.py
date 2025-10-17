# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np

# 假設 ui_shared 包含 ensure_page_config, render_header, render_footer
# 確保這些共用函式可以被正確導入
# 註: 專案內已有的 sys.path 處理邏輯，確保 ui_shared 可用，故此處僅保留精簡的導入。
from ui_shared import ensure_page_config, render_header, render_footer 

# 確保頁面設定
ensure_page_config('6 retirement')
render_header()

# ----------------------------------------------------
# 退休與永續現金流模擬工具
# ----------------------------------------------------

def format_currency(amount: float) -> str:
    """將數字格式化為帶有千位分隔符的字符串 (台幣風格)"""
    if pd.isna(amount) or amount < 0:
        # 負數或 NA 顯示為 0
        return "0"
    return f"{int(amount):,.0f}"

st.subheader("💼 退休與永續金流模擬器")
st.write("此模型用於快速評估退休金流的**可持續性 (Sustainability)**。它將資產、提領需求、報酬率和通膨納入考量，幫助您判斷目前的規劃是否能支應預計的餘命。")
st.caption("—  與保單、信託結合，建立可預期的現金流；同時保留彈性與治理秩序。")

# 連結到相關頁面
st.page_link("pages/8_insurance_strategy.py", label="查看保單金流設計 →", use_container_width=True)

st.divider()

# ----------------- 輸入區 -----------------
st.markdown("### 參數輸入")
col1, col2, col3 = st.columns(3)

with col1:
    initial_capital = st.number_input(
        "目前資產淨值 (元)", 
        min_value=1_000_000, 
        value=50_000_000, 
        step=5_000_000,
        help="不包含自住不動產的流動資產或投資組合總價值。",
        format="%d"
    )
    start_age = st.number_input(
        "目前年齡 (歲)", 
        min_value=30, 
        max_value=100, 
        value=55, 
        step=1
    )
    withdrawal_start = st.number_input(
        "每年提領金額 (元)", 
        min_value=100_000, 
        value=1_500_000, 
        step=100_000,
        help="退休後第一年預計提領的金額，用於生活開銷。",
        format="%d"
    )

with col2:
    retirement_age = st.number_input(
        "預計退休年齡 (歲)", 
        min_value=start_age + 1, # 至少大於目前年齡
        max_value=100, 
        value=65, 
        step=1
    )
    end_age = st.number_input(
        "規劃終點年齡 (歲)", 
        min_value=retirement_age + 1, 
        max_value=120, 
        value=90, 
        step=1,
        help="規劃計算終點，通常設定為預計壽命或更保守的年齡。"
    )

with col3:
    expected_return = st.slider(
        "年化報酬率 (退休後)", 
        min_value=0.0, 
        max_value=10.0, 
        value=5.0, 
        step=0.5,
        format="%.1f %%",
        help="退休後投資組合的年化預期報酬率 (稅後)。"
    ) / 100
    inflation_rate = st.slider(
        "通膨率 (提領增加率)", 
        min_value=0.0, 
        max_value=5.0, 
        value=3.0, 
        step=0.1,
        format="%.1f %%",
        help="提領金額每年因通膨增加的百分比。"
    ) / 100
    
# ----------------- 模擬計算 -----------------

if st.button("📈 執行退休金流模擬", type="primary"):
    
    # 檢查邏輯錯誤
    if retirement_age <= start_age or end_age <= retirement_age:
        st.error("請確認輸入：退休年齡必須大於目前年齡，且規劃終點年齡必須大於退休年齡。")
        st.stop()
        
    # 初始化變數
    current_balance = float(initial_capital)
    annual_withdrawal = float(withdrawal_start)
    
    # 退休前的年數 (簡化，假設這段時間資產成長率為 0)
    # 實際應用中，退休前的資產成長應另行計算，這裡為專注退休後金流而簡化
    current_balance = initial_capital 
    
    simulation_years = range(retirement_age, end_age + 1)
    results = []
    depletion_age = end_age
    
    # 退休後模擬
    for year_age in simulation_years:
        is_retirement_start = (year_age == retirement_age)
        
        # 提領金額 (如果不是退休第一年，則根據通膨調整)
        if not is_retirement_start:
            annual_withdrawal *= (1 + inflation_rate)
        
        # 資產增長 (以期初餘額計算)
        # 報酬率應考慮實際提領的時點，這裡簡化為期初餘額乘以報酬率
        portfolio_gain = current_balance * expected_return
        
        # 計算期末餘額
        next_balance = current_balance + portfolio_gain - annual_withdrawal
        
        # 檢查資產是否耗盡
        if next_balance <= 0:
            final_balance = 0.0
            depletion_age = year_age
            results.append({
                "年齡": year_age,
                "期初餘額 (元)": current_balance,
                "預期報酬 (元)": portfolio_gain,
                "提領金額 (元)": annual_withdrawal,
                "期末餘額 (元)": 0.0,
                "狀態": "資產耗盡"
            })
            break
        
        # 儲存結果
        results.append({
            "年齡": year_age,
            "期初餘額 (元)": current_balance,
            "預期報酬 (元)": portfolio_gain,
            "提領金額 (元)": annual_withdrawal,
            "期末餘額 (元)": next_balance,
            "狀態": "持續"
        })
        
        current_balance = next_balance
        
    # ----------------- 輸出區 -----------------
    if not results:
        st.warning("模擬期間過短或輸入參數有誤，請檢查年齡設定。")
        st.stop()
        
    df_results = pd.DataFrame(results)
    
    st.subheader("📊 模擬結果分析")
    
    # 最終狀態
    final_status_col, final_summary_col = st.columns([1, 2])
    
    if depletion_age < end_age:
        final_summary = f"在 **{depletion_age} 歲**，資產預計會耗盡。這比規劃終點 **{end_age} 歲** 提前了 {end_age - depletion_age} 年。"
        final_status_col.error(f"❌ 提早耗盡 ({depletion_age} 歲)")
    else:
        # 使用最後一年的期末餘額
        final_remaining_balance = df_results['期末餘額 (元)'].iloc[-1]
        final_summary = f"資產能持續到規劃終點 **{end_age} 歲**。屆時預計剩餘餘額約為 **{format_currency(final_remaining_balance)} 元**。"
        final_status_col.success(f"✅ 可持續到 {end_age} 歲")
        
    final_summary_col.markdown(final_summary)
    
    
    # 繪製圖表
    st.markdown("---")
    st.markdown("#### 資金餘額與提領趨勢")
    
    chart_data = df_results.copy()
    chart_data.set_index('年齡', inplace=True)
    chart_data.rename(columns={
        "期末餘額 (元)": "期末資產餘額",
        "提領金額 (元)": "每年實際提領金額"
    }, inplace=True)
    
    # 繪製資產餘額和提領金額趨勢圖
    st.line_chart(chart_data[["期末資產餘額", "每年實際提領金額"]])
    
    # 顯示詳細數據表
    st.markdown("---")
    st.markdown("#### 年度金流詳細明細")
    
    # 格式化數字欄位
    df_display = df_results.copy()
    for col in ["期初餘額 (元)", "預期報酬 (元)", "提領金額 (元)", "期末餘額 (元)"]:
        df_display[col] = df_display[col].apply(format_currency)
        
    st.dataframe(df_display, use_container_width=True, hide_index=True)


render_footer()
