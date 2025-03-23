
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

# --- 傳承開場語（置中、加大加粗） ---
st.markdown("""
<br>
<div style='text-align: center; font-size: 20px; font-weight: bold; margin-top: 1em;'>
🌱 每一位家族的掌舵者，都是家族傳承的種子。<br>
我們陪您，讓這份影響力持續茁壯。
</div>
<br>
""", unsafe_allow_html=True)

# --- 初始化狀態 ---
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

# --- 模組一 ---
st.markdown("## 模組一：經營的是事業，留下的是故事")
st.markdown("""
我們陪您一起梳理這段歷程，  
為後人留下的不只是成果，更是一種精神。
""")

if not st.session_state.started:
    if st.button("開始整理"):
        st.session_state.started = True

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

# --- 模組二 ---
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

if st.session_state.next_step and not st.session_state.module_two_done:
    st.markdown("---")
    st.markdown("## 模組二：釐清內心的優先順序")

    st.markdown("""
在許多重要的事之中，總有一兩件，對您來說有特別的份量。  
我們不急著定義，也不急著安排，  
只是陪您靜靜思考——那個您一直放在心裡的想法。
""")

    combined_options = list(st.session_state.options)
    if st.session_state.custom_input.strip():
        combined_options.append(st.session_state.custom_input.strip())

    key_issues = st.multiselect(
        "從您剛剛提到的事情中，哪一兩件對您來說最重要？",
        combined_options,
        max_selections=2
    )

    reason = st.text_area("為什麼這件事對您來說特別重要？")

    if st.button("完成這一段思考"):
        st.session_state.key_issues = key_issues
        st.session_state.reason = reason
        st.session_state.module_two_done = True

# --- 模組三 ---
if st.session_state.module_two_done and not st.session_state.module_three_done:
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
如果您願意，我們可以再往前走一步，看看有哪些方向可以開始準備。
""")

    if st.button("好，我想繼續看看"):
        st.session_state.module_three_done = True

if st.session_state.module_three_done and not st.session_state.module_four_done:
    st.markdown("---")
    st.markdown("## 模組三：從想法，到方向")

    st.markdown("""
剛剛那些思緒與感受，也許正帶著您指向某個方向。  
現在，不如試著想一想：  
您希望事情能朝什麼樣的未來發展？
""")

    direction_choices = st.multiselect(
        "您希望事情未來可以朝哪些方向走？",
        [
            "希望有人能逐步接手，讓我放心退下來",
            "希望我退休後，也能保有影響力與參與感",
            "希望家人之間能建立共識與溝通模式",
            "希望財務安排穩妥清楚，避免未來爭議",
            "希望即使我不在，公司與資產仍能穩定運作",
        ]
    )

    custom_direction = st.text_area("其他想補充的方向？（可以不填）")

    if st.button("完成方向探索"):
        st.session_state.directions = direction_choices
        st.session_state.custom_direction = custom_direction
        st.session_state.module_four_done = True

# --- 模組四 ---
if st.session_state.module_four_done:
    st.markdown("---")
    st.markdown("## 模組四：行動策略，從這裡慢慢展開")

# --- 模組五：自動預約引導 ---
st.markdown("---")
st.markdown("## 模組五：預約諮詢")

st.markdown("""
您已經為自己釐清了許多關鍵的思考，  
如果您想讓這些想法進一步落實，  
我們也很樂意陪您慢慢規劃下一步。

---
📌 永傳家族辦公室  
💼 https://gracefo.com/  
📧 123@gracefo.com

點擊下方按鈕，即可發信與我們預約一對一諮詢。
""")

st.markdown("""
<a href="mailto:123@gracefo.com?subject=預約諮詢：我想了解家族傳承與退休安排&body=您好，我剛剛使用了永傳AI教練，想進一步與您聊聊我的規劃需求。" target="_blank">
    <button style='padding: 0.5em 1em; font-size: 16px; border-radius: 6px; background-color: #4CAF50; color: white; border: none;'>預約諮詢</button>
</a>
""", unsafe_allow_html=True)
