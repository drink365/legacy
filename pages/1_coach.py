import streamlit as st
from modules.strategy_module import get_strategy_suggestions
from modules.pdf_generator import generate_pdf
from modules.cta_section import render_cta

st.set_page_config(
    page_title="《影響力》傳承風格探索",
    page_icon="🌿",
    layout="centered"
)

# 頁面標題
st.markdown("""
# 《影響力》傳承風格探索
layout="centered"
""")

# 初始化 session_state
for key in ["submitted", "module_two_done", "module_three_done", "module_four_done", "legacy_quiz_done"]:
    if key not in st.session_state:
        st.session_state[key] = False

# 首頁跳轉提示
if "start_from_home" in st.session_state and st.session_state.start_from_home:
    st.session_state.start_from_home = False
    st.success("✅ 已為您啟動《影響力》探索流程")


# 傳承風格小測驗
if not st.session_state.legacy_quiz_done:
    st.markdown("### 傳承風格小測驗：我是怎麼看待家族傳承的？")
    st.markdown("請根據您的直覺選出最貼近您想法的選項。")

    questions = [
        ("傳承的出發點對我來說，最重要的是：", ["家人能持續相處和睦", "資產能安全地傳承下去", "我的理念能被理解與延續"]),
        ("當子女表達不想接班，我會：", ["不勉強他們，找外部幫手也可", "再觀察是否只是短期情緒", "引導他們理解我創業的初衷"]),
        ("我最擔心未來的哪種情況？", ["家人產生衝突", "資產糾紛或稅務出錯", "後代迷失方向、失去初衷"]),
        ("面對傳承，我比較喜歡的風格是：", ["柔和溝通，建立共識", "明確制度、先講規則", "敘說理念，引導願景"]),
        ("我最希望扮演的角色是：", ["和平橋樑，維持關係", "安排者，設計制度與策略", "領航者，引領下一代看見方向"]),
    ]
    selections = []
    for i, (q, opts) in enumerate(questions):
        choice = st.radio(q, opts, key=f"quiz_{i}")
        selections.append(choice)

    if st.button("完成風格測驗"):
        a_count = sum([s.startswith("家人") or s.startswith("不勉強") or s.startswith("家人產生") or s.startswith("柔和") or s.startswith("和平") for s in selections])
        b_count = sum([s.startswith("資產") or s.startswith("再觀察") or s.startswith("資產糾紛") or s.startswith("明確") or s.startswith("安排者") for s in selections])
        c_count = sum([s.startswith("我的理念") or s.startswith("引導") or s.startswith("後代") or s.startswith("敘說") or s.startswith("領航者") for s in selections])

        if a_count >= max(b_count, c_count):
            st.session_state.legacy_style_result = "關係守護者型：您重視家庭和諧、情感平衡，適合建立家族共識與柔性傳承策略。"
        elif b_count >= max(a_count, c_count):
            st.session_state.legacy_style_result = "策略家型：您偏好制度與規劃，適合以信託、股權與稅務工具建構穩定架構。"
        else:
            st.session_state.legacy_style_result = "領航者型：您重視理念與精神的延續，適合透過願景建立、生命故事傳承影響力。"

        st.session_state.legacy_quiz_done = True

# 顯示結果並進入模組一
if st.session_state.legacy_quiz_done and not st.session_state.submitted:
    st.markdown("## 您的傳承風格")
    st.success(st.session_state.legacy_style_result)
    st.markdown("---")
    st.markdown("### 模組一：最近，您常想些什麼？")
    options = st.multiselect(
        "請選出最近比較常想的事（可複選）：",
        [
            "公司的未來要怎麼安排？",
            "孩子適不適合承接家業？",
            "退休後的生活要怎麼過？",
            "怎麼分配資產才公平？",
            "家族成員之間的關係",
            "萬一健康出現變化怎麼辦？",
            "我想慢慢退下來，但不知道從哪開始"
        ]
    )
    custom_input = st.text_area("還有什麼最近常出現在您心裡的？（可以不填）")

    if st.button("繼續探索下一步"):
        st.session_state.options = options
        st.session_state.custom_input = custom_input
        st.session_state.submitted = True

# 模組二
if st.session_state.submitted and not st.session_state.module_two_done:
    st.markdown("## 模組二：您最在意的重點")
    combined_options = list(st.session_state.options)
    if st.session_state.custom_input.strip():
        combined_options.append(st.session_state.custom_input.strip())
    key_issues = st.multiselect("從上面選項中，挑出對您最重要的一兩件：", combined_options, max_selections=2)
    reason = st.text_area("為什麼這件事對您特別重要？")

    if st.button("完成這一段思考"):
        st.session_state.key_issues = key_issues
        st.session_state.reason = reason
        st.session_state.module_two_done = True

# 模組三
if st.session_state.module_two_done and not st.session_state.module_three_done:
    st.markdown("## 模組三：您期望的未來方向")
    direction_choices = st.multiselect(
        "您希望事情未來可以朝哪些方向發展？",
        [
            "希望有人能逐步接手，讓我放心退下來",
            "希望我退休後，也能保有影響力與參與感",
            "希望家人之間能建立共識與溝通模式",
            "希望財務安排穩妥清楚，避免未來爭議",
            "希望即使我不在，公司與資產仍能穩定運作"
        ]
    )
    custom_direction = st.text_area("其他想補充的方向？（可以不填）")
    if st.button("完成方向探索"):
        st.session_state.directions = direction_choices
        st.session_state.custom_direction = custom_direction
        st.session_state.module_three_done = True

# 模組四
if st.session_state.module_three_done and not st.session_state.module_four_done:
    st.markdown("## 模組四：行動策略，從這裡慢慢展開")
    st.markdown("釐清了想法之後，這一步我們陪您看看有哪些小步驟可以開始安排，慢慢走、也走得穩。")
    st.markdown("### 您可以考慮的策略方向：")
    strategies = get_strategy_suggestions()
    for strategy in strategies:
        with st.expander(strategy["title"]):
            st.write(strategy["details"])
    if st.button("完成策略初步探索"):
        st.session_state.module_four_done = True

# 模組五
if st.session_state.module_four_done:
    st.markdown("---")
    st.markdown("## 下一步，我可以從哪裡開始？")
    st.markdown("🎉 您已經整理出一些非常重要的思考！")

    if "key_issues" in st.session_state:
        if any("關係" in item or "家族成員" in item for item in st.session_state.key_issues):
            st.markdown("✅ 如果您最在意的是『家人關係』：可以安排一次家庭晚餐，輕鬆聊聊大家對未來的想法。")
        if any("資產" in item or "分配" in item for item in st.session_state.key_issues):
            st.markdown("✅ 如果您在意的是『資產安排』：可以先盤點目前有哪些財產項目，例如帳戶、保單、房產或股權。")
        if any("公司" in item or "接班" in item for item in st.session_state.key_issues):
            st.markdown("✅ 如果您考慮的是『接班』：試著與您心中的接班人選聊聊，看看他對未來的想法。")

    st.markdown("---")
    st.markdown("### 📥 下載個人化探索紀錄（PDF）")
    pdf = generate_pdf()
    st.download_button(
        label="下載我的探索紀錄報告（PDF）",
        data=pdf,
        file_name="影響力_探索紀錄.pdf",
        mime="application/pdf"
    )

    render_cta()

    st.markdown("""
    ---
    📌 永傳家族辦公室｜<a href="https://gracefo.com" target="_blank">https://gracefo.com</a>  
    📧 聯絡我們：<a href="mailto:123@gracefo.com">123@gracefo.com</a>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("感謝您完成這段探索。我們相信，每一次釐清與行動，都是為未來鋪路的開始。")
    st.markdown("願您的影響力，代代傳承。🌿")
