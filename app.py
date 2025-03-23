
import streamlit as st
import base64
from modules.strategy_module import get_strategy_suggestions

# --- 基本設定 ---
st.set_page_config(
    page_title="永傳 AI 傳承教練",
    page_icon="🌿",
    layout="centered"
)

# --- 品牌 LOGO 顯示（置中顯示圖片 Base64） ---
def load_logo_base64(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

logo_base64 = load_logo_base64("logo.png")
st.markdown(f"""
<div style='text-align: center;'>
    <img src='data:image/png;base64,{logo_base64}' width='300'><br>
    <div style='font-size: 18px; font-weight: bold; margin-top: 0.5em;'>傳承您的影響力</div>
</div>
""", unsafe_allow_html=True)

# --- 傳承開場語 ---
st.markdown("""
<br>
<div style='text-align: center; font-size: 20px; font-weight: bold; margin-top: 1em;'>
🌱 每一位家族的掌舵者，都是家族傳承的種子。<br>
我們陪您，讓這份影響力持續茁壯。
</div>
<br>
""", unsafe_allow_html=True)

# --- 初始狀態設計 ---
if "show_module_one" not in st.session_state:
    st.session_state.show_module_one = False
if "started" not in st.session_state:
    st.session_state.started = False
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "next_step" not in st.session_state:
    st.session_state.next_step = False
if "module_two_done" not in st.session_state:
    st.session_state.module_two_done = False
if "module_three_done" not in st.session_state:
    st.session_state.module_three_done = False
if "module_four_done" not in st.session_state:
    st.session_state.module_four_done = False

# --- 起手式引導語與按鈕 ---
if not st.session_state.show_module_one:
    st.markdown("""
    <div style='text-align: center; font-size: 17px; margin-bottom: 1em;'>
    這不是一份問卷，也不是填資料的流程，<br>
    而是一段為自己慢慢梳理方向的對話。
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔍 開始探索我的下一步"):
        st.session_state.show_module_one = True

# --- 模組一 ---
if st.session_state.show_module_one:
    st.markdown("## 模組一：經營的是事業，留下的是故事")
    st.markdown("我們陪您一起梳理這段歷程，為後人留下的不只是成果，更是一種精神。")

    if not st.session_state.started:
        if st.button("開始整理"):
            st.session_state.started = True

    if st.session_state.started and not st.session_state.submitted:
        st.markdown("---")
        st.markdown("### 最近，您常想些什麼？")

        options = st.multiselect(
            "您最近比較常想的是：",
            [
                "公司的未來要怎麼安排？",
                "孩子適不適合承接家業？",
                "退休後的生活要怎麼過？",
                "怎麼分配資產才公平？",
                "家族成員之間的關係",
                "萬一健康出現變化怎麼辦？",
                "我想慢慢退下來，但不知道從哪開始",
            ]
        )

        custom_input = st.text_area("還有什麼最近常出現在您心裡的？（可以不填）")

        if st.button("繼續"):
            st.session_state.options = options
            st.session_state.custom_input = custom_input
            st.session_state.submitted = True

# 後續模組二～模組五（略），維持不變邏輯條件顯示即可（保留原來的觸發順序）
