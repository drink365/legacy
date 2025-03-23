import streamlit as st

# --- 網頁基本設定 ---
st.set_page_config(
    page_title="永傳 AI 教練",
    page_icon="🌿",
    layout="centered"
)

# --- 初始化狀態 ---
if "started" not in st.session_state:
    st.session_state.started = False
if "submitted" not in st.session_state:
    st.session_state.submitted = False

# --- 品牌標題區 ---
st.markdown("### 永傳")
st.markdown("#### 傳承您的影響力")
st.markdown("---")

# --- 模組一 開場語 ---
st.markdown("## 模組一：經營的是事業，留下的是故事")
st.markdown("""
我們陪您一起梳理這段歷程，  
為後人留下的不只是成果，更是一種精神。
""")

# --- 開始整理按鈕 ---
if not st.session_state.started:
    if st.button("開始整理"):
        st.session_state.started = True

# --- 互動區 ---
if st.session_state.started and not st.session_state.submitted:
    st.markdown("---")
    st.markdown("### 最近，您常想些什麼？")
    st.markdown("請隨意勾選下面幾個選項，也可以補充自己的想法。")

    # 多選選項
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

    # 自由輸入欄位
    custom_input = st.text_area("還有什麼最近常出現在您心裡的？（可以不填）")

    # 繼續按鈕
    if st.button("繼續"):
        st.session_state.options = options
        st.session_state.custom_input = custom_input
        st.session_state.submitted = True

# --- 回饋區 ---
if st.session_state.submitted:
    st.markdown("---")
    st.markdown("### 您正在思考的，是這些事：")

    if st.session_state.options:
        for item in st.session_state.options:
            st.write(f"• {item}")
    if st.session_state.custom_input.strip():
        st.write(f"• {st.session_state.custom_input.strip()}")

    st.markdown("""
這些事，有的您已經想了很久，有的可能剛浮現。  
沒關係，我們接下來會慢慢陪您，一步步釐清，您真正在意的，是什麼。
""")
