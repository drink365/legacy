import streamlit as st
from modules.strategy_module import get_strategy_suggestions
from modules.pdf_generator import generate_pdf
from modules.cta_section import render_cta

st.set_page_config(
    page_title="永傳 AI 傳承教練",
    page_icon="🌿",
    layout="centered"
)

for key in ["submitted", "module_two_done", "module_three_done", "module_four_done", "legacy_quiz_done"]:
    if key not in st.session_state:
        st.session_state[key] = False

if "start_from_home" in st.session_state and st.session_state.start_from_home:
    st.session_state.start_from_home = False
    st.success("✅ 已為您啟動永傳 AI 傳承教練探索流程")

# 模組一：風格小測驗
if not st.session_state.legacy_quiz_done:
    st.markdown("""
    <div style='background-color: #e8f5e9; padding: 1em; border-radius: 8px;'>
        <h4>🟩 模組一：傳承風格小測驗</h4>
        <p>請根據您的直覺，選出最貼近您想法的選項。</p>
    </div>
    """, unsafe_allow_html=True)

    questions = [
        ("傳承的出發點對我來說，最重要的是：", ["家人能持續相處和睦", "資產能安全地傳承下去", "我的理念能被理解與延續"]),
        ("當子女表達不想接班，我會：", ["不勉強他們，找外部幫手也可", "再觀察是否只是短期情緒", "引導他們理解我創業的初衷"]),
        ("我最擔心未來的哪種情況？", ["家人產生衝突", "資產糾紛或稅務出錯", "後代迷失方向、失去初衷"]),
        ("面對傳承，我比較喜歡的風格是：", ["柔和溝通，建立共識", "明確制度、先講規則", "敘說理念，引導願景"]),
        ("我最希望扮演的角色是：", ["和平橋樑，維持關係", "安排者，設計制度與策略", "領航者，引領下一代看見方向"]),
    ]
    selections = []
    for i, (q, opts) in enumerate(questions):
        choice = st.radio(f"{i+1}. {q}", opts, key=f"quiz_{i}")
        selections.append(choice)

    st.markdown("🔽 請完成上方題目後，點選下方按鈕")
    if st.button("✅ 完成風格測驗"):
        a_count = sum([s.startswith("家人") or s.startswith("不勉強") or s.startswith("家人產生") or s.startswith("柔和") or s.startswith("和平") for s in selections])
        b_count = sum([s.startswith("資產") or s.startswith("再觀察") or s.startswith("資產糾紛") or s.startswith("明確") or s.startswith("安排者") for s in selections])
        c_count = sum([s.startswith("我的理念") or s.startswith("引導") or s.startswith("後代") or s.startswith("敘說") or s.startswith("領航者") for s in selections])

        if a_count >= max(b_count, c_count):
            st.session_state.legacy_style_result = "❤️ 關係守護者型：您重視家庭和諧、情感平衡，適合建立家族共識與柔性傳承策略。"
        elif b_count >= max(a_count, c_count):
            st.session_state.legacy_style_result = "💼 策略家型：您偏好制度與規劃，適合以信託、股權與稅務工具建構穩定架構。"
        else:
            st.session_state.legacy_style_result = "🧭 領航者型：您重視理念與精神的延續，適合透過願景建立、生命故事傳承影響力。"

        st.session_state.legacy_quiz_done = True

# 顯示結果
if st.session_state.legacy_quiz_done and not st.session_state.submitted:
    st.markdown("""
    <div style='background-color: #e8f5e9; padding: 1em; border-radius: 8px;'>
        <h4>🟩 您的傳承風格分析結果</h4>
    </div>
    """, unsafe_allow_html=True)
    st.success(st.session_state.legacy_style_result)

    st.markdown("---")
    st.markdown("### 模組二：最近，您常想些什麼？")
    st.markdown("請選出最近比較常出現在您心裡的事：")
    options = st.multiselect(
        "近期的焦慮與思考方向（可複選）",
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
    custom_input = st.text_area("是否還有其他想法？（選填）")

    st.markdown("🔽 請完成上方選項後，點下方繼續")
    if st.button("▶️ 繼續探索下一步"):
        st.session_state.options = options
        st.session_state.custom_input = custom_input
        st.session_state.submitted = True

# 後續模組照原樣保留，建議逐步依此邏輯加入視覺提示與區塊結構
# 我可再依據你是否滿意這種風格，協助全面改版後半段 🌱
