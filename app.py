# app.py — Home
import streamlit as st
from utils.branding import APP_TITLE, APP_KICKER, APP_TAGLINE, FOOTER, LOGO_PATH, HIDE_DEFAULT_UI, BRAND_COLORS
from utils.auth import verify_user, topbar_html

st.set_page_config(page_title=APP_TITLE, page_icon="🌏", layout="wide")
st.markdown(HIDE_DEFAULT_UI, unsafe_allow_html=True)
st.markdown(BRAND_COLORS, unsafe_allow_html=True)

# Sidebar Login
st.sidebar.header("登入")
if "user" not in st.session_state: st.session_state.user = None

if st.session_state.user is None:
    username = st.sidebar.text_input("帳號")
    password = st.sidebar.text_input("密碼", type="password")
    if st.sidebar.button("登入", type="primary"):
        user, err = verify_user(username, password)
        if err: st.sidebar.error(err)
        else:
            st.session_state.user = user
            st.sidebar.success(f"歡迎回來，{user.name}！")
            st.rerun()
else:
    u = st.session_state.user
    st.sidebar.success(f"已登入：{u.name}（{u.role}）\n有效期限：{u.end_date}")
    if st.sidebar.button("登出"):
        st.session_state.user = None; st.rerun()

# Topbar Info
if st.session_state.user: st.markdown(topbar_html(st.session_state.user), unsafe_allow_html=True)

# Hero
left, right = st.columns([1,5])
with left:
    try: st.image(LOGO_PATH, use_container_width=True)
    except Exception: st.markdown("### 🌏")
with right:
    st.markdown(f'<div class="kicker">{APP_KICKER}</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero"><h1>讓家族資產一目了然，<br/>讓顧問提案快速成交。</h1>'
                f'<p class="lead">{APP_TAGLINE}</p></div>', unsafe_allow_html=True)
    st.markdown('<span class="pill">高資產家庭</span><span class="pill">創辦人與二代</span><span class="pill">保險與財稅顧問</span>', unsafe_allow_html=True)

st.write("")
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("#### 這是什麼？")
    st.markdown("AI 傳承策略平台：把繁雜的**資產盤點、稅務試算、保單規劃**變成清楚好懂、可立即行動的方案。")
with c2:
    st.markdown("#### 適合誰？")
    st.markdown("**高資產家庭（創辦人與二代）**、**保險/財稅顧問**，需要更快更穩的**交棒與提案流程**。")
with c3:
    st.markdown("#### 能帶來什麼？")
    st.markdown("**看見全貌 → 找到方案 → 建立信任**。以結果為導向，提升**安心感**與**成交率**。")

st.divider()
st.markdown('<div class="section-title">三大成果</div>', unsafe_allow_html=True)
g1, g2, g3 = st.columns(3)
with g1:
    st.markdown("##### 🗺️ 看見全貌")
    st.markdown('<div class="value-card muted">資產傳承圖、跨境盤點、現金流可視化。<br/>把複雜結構變成 1 張圖，跨代溝通更順。</div>', unsafe_allow_html=True)
with g2:
    st.markdown("##### 🧭 找到方案")
    st.markdown('<div class="value-card muted">稅負試算 × 保單模擬 × 贈與壓縮。<br/>快速收斂可行解，縮短決策時間。</div>', unsafe_allow_html=True)
with g3:
    st.markdown("##### 🤝 建立信任")
    st.markdown('<div class="value-card muted">提案生成器＋顧問語庫。<br/>從「商品」走向「策略」，專業差異化。</div>', unsafe_allow_html=True)

st.divider()
st.markdown('<div class="section-title">立即開始</div>', unsafe_allow_html=True)
cta1, cta2, cta3 = st.columns([1.1, 1.1, 1])
with cta1:
    st.markdown("**📦 保單策略模擬器**")
    st.markdown('<p class="muted">找出「保障 × 傳承 × 現金流」最佳結構。</p>', unsafe_allow_html=True)
    if st.button("👉 開始體驗", type="primary"):
        st.switch_page("pages/1_insurance_planner.py")
with cta2:
    st.markdown("**📊 遺產稅試算與壓縮**")
    st.markdown('<p class="muted">先看稅，再排解；用保單與節點設計壓縮負擔。</p>', unsafe_allow_html=True)
    if st.button("👉 立即試算", type="primary"):
        st.switch_page("pages/2_estate_tax.py")
with cta3:
    st.markdown("**🧑‍💼 顧問專用方案**")
    st.markdown('<p class="muted">一鍵生成提案＋對話語庫，提升成交率。</p>', unsafe_allow_html=True)
    if st.button("👉 了解方案"):
        st.switch_page("pages/3_advisor_plan.py")

st.write("")
st.caption(FOOTER)
