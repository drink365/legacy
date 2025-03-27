import streamlit as st
from modules.tax_constants import TaxConstants
from modules.tax_calculator import EstateTaxCalculator


def render_estate_tax_ui(calculator: EstateTaxCalculator):
    st.markdown("## 遺產稅快速試算")

    st.markdown("### 請輸入您的基本資訊")
    total_assets = st.number_input("💰 總資產（萬元）", min_value=0, value=5000, step=100)

    st.markdown("---")
    st.markdown("### 👨‍👩‍👧‍👦 家庭成員資訊")
    spouse = st.checkbox("有配偶（扣除額 553 萬）")
    adult_children = st.number_input("成年子女人數（每人扣除 56 萬）", min_value=0, value=0)
    parents = st.number_input("父母人數（每人扣除 138 萬）", min_value=0, max_value=2, value=0)
    disabled_people = st.number_input("重度以上身心障礙者人數（每人扣除 693 萬）", min_value=0, value=0)
    other_dependents = st.number_input("其他撫養親屬人數（每人扣除 56 萬）", min_value=0, value=0)

    st.markdown("---")

    if st.button("📊 立即試算遺產稅"):
        taxable_amount, tax_due, total_deductions = calculator.calculate_estate_tax(
            total_assets,
            spouse,
            adult_children,
            other_dependents,
            disabled_people,
            parents
        )

        st.success(f"💡 課稅遺產淨額：約 {taxable_amount:,.0f} 萬元")
        st.success(f"🧾 預估遺產稅：約 {tax_due:,.0f} 萬元")

        with st.expander("📌 詳細扣除項目"):
            st.markdown(f"- 免稅額：{calculator.constants.EXEMPT_AMOUNT} 萬")
            st.markdown(f"- 喪葬費扣除：{calculator.constants.FUNERAL_EXPENSE} 萬")
            if spouse:
                st.markdown(f"- 配偶扣除：{calculator.constants.SPOUSE_DEDUCTION_VALUE} 萬")
            st.markdown(f"- 子女扣除：{adult_children} 人 × {calculator.constants.ADULT_CHILD_DEDUCTION} 萬")
            st.markdown(f"- 父母扣除：{parents} 人 × {calculator.constants.PARENTS_DEDUCTION} 萬")
            st.markdown(f"- 障礙扣除：{disabled_people} 人 × {calculator.constants.DISABLED_DEDUCTION} 萬")
            st.markdown(f"- 其他撫養扣除：{other_dependents} 人 × {calculator.constants.OTHER_DEPENDENTS_DEDUCTION} 萬")
            st.markdown(f"---\n🧮 扣除總額：約 {total_deductions:,.0f} 萬元")

        st.markdown("---")
        st.markdown("📬 若希望針對保險規劃進行模擬與建議，歡迎與我們聯繫。")
        st.markdown("👉 <a href='mailto:123@gracefo.com?subject=預約遺產稅規劃諮詢' target='_blank'>點我寄信預約專人對談</a>", unsafe_allow_html=True)
