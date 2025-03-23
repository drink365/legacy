import streamlit as st

# --- 基本設定 ---
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
if "next_step" not in st.session_state:
    st.session_state.next_step = False
if "module_two_done" not in st.session_state:
    st.session_state.module_two_done = False

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

# --- 模組一 互動區 ---
if st.session_state.started and not st.session_state.submitted:
    st.markdown("---")
    st.markdown("### 最近，您常想些什麼？")
    st.markdown("請隨意勾選下面幾個選項，也可以補充自己的想法。")

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

# --- 模組一 回饋 + 引導語 ---
if st.session_state.submitted and not st.session_state.next_step:
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

    st.markdown("### 如果您願意，我們可以繼續往下看看")

    st.markdown("""
有時候，真正的關鍵，藏在一段話、或一個選擇背後的心念裡。  
如果您願意，我們接下來可以慢慢梳理，  
找出對您來說最重要的那幾件事，  
一步步，把未來安排得更清楚、更穩當。
""")

    if st.button("我願意繼續"):
        st.session_state.next_step = True

# --- 模組二：釐清最重要的事 ---
if st.session_state.next_step and not st.session_state.module_two_done:
    st.markdown("---")
    st.markdown("## 模組二：釐清內心的優先順序")

    st.markdown("""
在許多重要的事之中，總有一兩件，對您來說有特別的份量。  
我們不急著定義，也不急著安排，  
只是陪您靜靜看一眼——那個您一直放在心裡的想法。
""")

    # 讓使用者從剛剛選的選項中挑 1~2 項
    key_issues = st.multiselect(
        "從您剛剛選的事情中，哪一兩件對您來說最重要？",
        st.session_state.options,
        max_selections=2
    )

    # 輸入原因
    reason = st.text_area("為什麼這件事對您來說特別重要？")

    if st.button("完成這一段思考"):
        st.session_state.key_issues = key_issues
        st.session_state.reason = reason
        st.session_state.module_two_done = True

# --- 模組二回饋展示 ---
if st.session_state.module_two_done:
    st.markdown("---")
    st.markdown("### 您目前心中最重要的是：")
    if st.session_state.key_issues:
        for item in st.session_state.key_issues:
            st.write(f"• {item}")
    if st.session_state.reason.strip():
        st.markdown("**您說，它之所以重要，是因為：**")
        st.write(f"「{st.session_state.reason.strip()}」")

    st.markdown("""
謝謝您和我們分享這些想法。  
這是未來每一步規劃的起點。  
我們會陪您，從這個起點開始，慢慢畫出清楚的藍圖。
""")
