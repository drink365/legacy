import streamlit as st
import pandas as pd
from modules.tax_constants import TaxConstants
from modules.tax_calculator import EstateTaxCalculator

def render_estate_tax_ui(calculator: EstateTaxCalculator):
    st.markdown("## 遺產稅試算工具")

    # 使用者輸入區
    st.markdown("### 請填寫基本資訊")
    total_assets = st.number_input("總資產（單位：萬）", min_value=0, value=5000, step=100)
    spouse = st.checkbox("是否有配偶", value=False)
    adult_children = st.number_input("成年的子女數量", min_value=0, value=0, step=1)
    other_dependents = st.number_input("其他撫養親屬數量（兄弟姊妹、祖父母）", min_value=0, value=0, step=1)
    disabled_people = st.number_input("重度身心障礙者數量", min_value=0, value=0, step=1)
    parents = st.number_input("健在的父母數量", min_value=0, value=0, step=1)

    # 自動試算結果區
    taxable_amount, tax_due, deductions = calculator.calculate_estate_tax(
        total_assets, spouse, adult_children, other_dependents, disabled_people, parents
    )

    st.markdown("---")
    st.markdown("### 試算結果")
    st.write(f"課稅遺產淨額：{taxable_amount:,.0f} 萬元")
    st.write(f"預估遺產稅：{tax_due:,.0f} 萬元")
    st.write(f"總扣除額：{deductions:,.0f} 萬元")

    # 提示
    st.info("本試算為簡化版本，僅供參考，實際情況請諮詢專業顧問。")
