
import streamlit as st

# 頁面設定
st.set_page_config(page_title="傳承人生：你能守住多少家族財富？", layout="centered")

st.markdown("<h1 style='text-align: center;'>傳承人生：你能守住多少家族財富？</h1>", unsafe_allow_html=True)
st.markdown("請依直覺作答，每一題都沒有對錯，只有更貼近你的人生思維。")

# 題目與選項設定
questions = {
    "Q1. 當你思考將企業或資產交給下一代時，你的直覺反應是？": [
        ("A", "我會提前規劃並慢慢放手，陪伴他們成長"),
        ("B", "等自己無法處理了再交給他們比較穩當"),
        ("C", "我會依照孩子們的意願，他們想接再說"),
        ("D", "找專業經理人接手，再看孩子要不要參與")
    ],
    "Q2. 面對家中三位子女，每人個性與能力不同，你傾向怎麼分配資產？": [
        ("A", "每人平均，公平最重要"),
        ("B", "根據貢獻或需要調整，理性安排"),
        ("C", "留給最會管理的人，其餘人另安排保障"),
        ("D", "設立信託或架構，不直接分配給個人")
    ],
    "Q3. 如果傳承規劃遭遇家人反對或誤解，你會？": [
        ("A", "保持沉默，等時機成熟再談"),
        ("B", "主動溝通，希望取得共識"),
        ("C", "尊重每個人想法，不勉強"),
        ("D", "找第三方顧問幫忙說明與協調")
    ],
    "Q4. 如果遺產稅大幅上升，你的應對方式是？": [
        ("A", "提早規劃保單、信託，避開風險"),
        ("B", "了解法規後做必要調整"),
        ("C", "照現有安排進行，不做太大更動"),
        ("D", "找財稅顧問設計合法架構")
    ],
    "Q5. 若只能留下一樣東西，你希望留給孩子的是？": [
        ("A", "一筆保障未來的財富"),
        ("B", "他們能獨立面對人生的能力"),
        ("C", "家族的精神與價值觀"),
        ("D", "一套清晰且穩固的傳承架構")
    ]
}

# 儲存答案
scores = {"A": 0, "B": 0, "C": 0, "D": 0}
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

if not st.session_state.submitted:
    for idx, (q, opts) in enumerate(questions.items(), 1):
        choice = st.radio(f"{q}", [label for _, label in opts], key=f"q{idx}")
        for code, label in opts:
            if choice == label:
                scores[code] += 1

    if st.button("送出答案，看看你的傳承風格"):
        st.session_state.submitted = True
        st.session_state.scores = scores
        st.experimental_rerun()

# 呈現結果
else:
    scores = st.session_state.scores
    top_choice = max(scores, key=scores.get)

    # 對應風格
    result_map = {
        "A": ("智慧守護者", "你深知，傳承不是財富的分割，而是責任的延續。"),
        "B": ("理性規劃者", "你相信，每一分資源都該安排得其所，讓愛與秩序同行。"),
        "C": ("價值傳承者", "你知道，最珍貴的，不是資產，而是家族共同的信念與故事。"),
        "D": ("策略建構者", "你相信制度比情感更能守住未來，好架構能讓感情少傷痕。")
    }

    role, message = result_map[top_choice]
    st.success(f"你的傳承風格是：**{role}**")
    st.markdown(f"💬 _「{message}」_")

    # 行動引導
    st.markdown("---")
    st.markdown("### 🎯 下一步行動建議")
    st.markdown("- 使用 [AI 傳承教練](https://gracefo.com/legacy) 進一步分析您的資產結構")
    st.markdown("- 預約免費諮詢，與專業顧問討論最適合您家庭的傳承方案")
    st.markdown("- 或分享這個遊戲給朋友，看看他們是哪種風格 😊")

    if st.button("🔁 再玩一次"):
        st.session_state.submitted = False
        st.experimental_rerun()
