import streamlit as st
from modules.tax_logic import TaxConstants, EstateTaxCalculator

st.set_page_config(
    page_title="AI 秒算遺產稅",
    page_icon="🧮",
    layout="centered"
)

st.markdown("# 🧮 AI 秒算遺產稅")

# 資料輸入表單
with st.form("tax_form"):
    st.markdown("### 請輸入資產與家庭狀況")

    total_assets = st.number_input("總資產（萬）", min_value=1000, max_value=100000, value=5000, step=100)
    spouse = st.checkbox("是否有配偶")
    adult_children = st.number_input("成年子女人數", min_value=0, max_value=10, value=0)
    parents = st.number_input("父母人數", min_value=0, max_value=2, value=0)
    disabled = st.number_input("重度身心障礙人數", min_value=0, max_value=5, value=0)
    other_dependents = st.number_input("其他受扶養親屬人數", min_value=0, max_value=5, value=0)

    submitted = st.form_submit_button("試算")

if submitted:
    constants = TaxConstants()
    calculator = EstateTaxCalculator(constants)

    taxable_amount, tax_due, deductions = calculator.calculate_estate_tax(
        total_assets, spouse, adult_children, other_dependents, disabled, parents
    )

    st.success(f"預估遺產稅：{int(tax_due):,} 萬元")

    with st.expander("詳細稅務計算"):
        st.markdown(f"- 課稅遺產淨額：{int(taxable_amount):,} 萬元")
        st.markdown(f"- 總扣除額：{int(deductions):,} 萬元")
        st.markdown("- 包括免稅額、喪葬費、配偶、子女、父母、障礙與扶養扣除等")

    st.markdown("---")
    st.markdown("### 想進一步規劃遺產稅？")
    st.markdown("""
        若您希望瞭解保險預留稅源、信託安排、或提前贈與等規劃工具，
        歡迎預約永傳團隊進行一對一諮詢。
        
        📧 <a href="mailto:123@gracefo.com">點我寄信預約</a>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align: center; font-size: 12px; color: gray;'>
    永傳家族辦公室｜<a href="https://gracefo.com" target="_blank">https://gracefo.com</a>
    </div>
    """, unsafe_allow_html=True)
