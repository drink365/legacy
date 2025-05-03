
import streamlit as st

st.set_page_config(page_title="傳承風險盤點測驗", layout="centered")

st.markdown("<h1 style='text-align: center;'>🛡️ 傳承風險盤點測驗</h1>", unsafe_allow_html=True)
st.markdown("請依實際情況回答以下問題，我們將快速協助您辨識家族傳承中的潛在風險。")

questions = [
    ("您的父母或長輩是否已立下遺囑？", "未立遺囑 → 恐有未來爭產風險"),
    ("您是否清楚目前家庭資產結構（包含股權、保單、不動產等）？", "資產結構不明 → 傳承規劃難以落實"),
    ("是否有為配偶設計足夠的保障或財產分配安排？", "配偶保障不足 → 老後可能陷入經濟風險"),
    ("您是否已開始規劃稅務影響（如贈與稅、遺產稅）？", "未提前規劃稅務 → 可能產生高額稅負"),
    ("公司股權是否有清楚的接班與移轉安排？", "公司股權未安排 → 恐影響企業穩定與家族關係"),
    ("家庭成員之間是否已共識財產分配方向？", "缺乏共識 → 潛藏親情裂痕與衝突風險")
]

# 初始化狀態
if "risk_answers" not in st.session_state:
    st.session_state.risk_answers = {}
if "show_risk_result" not in st.session_state:
    st.session_state.show_risk_result = False

# 問答區域或結果區
if not st.session_state.show_risk_result:
    st.markdown("### 請回答以下問題：")
    for idx, (q, _) in enumerate(questions, 1):
        st.session_state.risk_answers[f"risk{idx}"] = st.radio(
            f"{idx}. {q}",
            ["是", "否"],
            key=f"risk{idx}_key"
        )
    if st.button("🔍 產出我的風險清單"):
        st.session_state.show_risk_result = True

else:
    st.success("✅ 傳承風險盤點完成")
    flags = []
    for idx, (_, risk) in enumerate(questions, 1):
        ans = st.session_state.risk_answers.get(f"risk{idx}")
        if ans == "否":
            flags.append(risk)

    if flags:
        st.markdown("### ⚠️ 您的潛在風險如下：")
        for r in flags:
            st.markdown(f"- ❗ {r}")
        st.markdown("---")
        st.markdown("### 🎯 建議行動")
        st.markdown("- 使用 AI 傳承教練進一步釐清資產結構")
        st.markdown("- 預約專業顧問，一對一討論家族風險管理")
        st.markdown("- 分享給家族成員一同盤點風險與共識建立")
    else:
        st.balloons()
        st.markdown("🎉 恭喜您，目前家族傳承結構相對完整！")

    if st.button("🔁 重新填寫"):
        st.session_state.show_risk_result = False
