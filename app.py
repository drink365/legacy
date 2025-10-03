# app.py — 《影響力》傳承策略平台（新版頁面佈局＋隱藏左側欄）
# 說明：
# 1) 完全隱藏左側欄與展開按鈕
# 2) 置頂品牌導覽列：左 Logo / 右 使用者資訊（😊 姓名｜有效期限）
# 3) 登入後隱藏登入表單，僅顯示主內容
# 4) AUTHORIZED_USERS 以 TOML 格式定義（內含日期區間檢核）

import os
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
import streamlit as st

# -------------------------
# 頁面設定：wide 佈局，嘗試用 logo2.png 當 favicon，否則使用 ✨
# -------------------------
def _try_open_icon():
    from PIL import Image
    icon_path = Path("logo2.png")
    if icon_path.exists():
        try:
            return Image.open(icon_path)
        except Exception:
            pass
    return "✨"

st.set_page_config(
    page_title="《影響力》傳承策略平台",
    page_icon=_try_open_icon(),
    layout="wide",
)

# -------------------------
# 全域樣式：隱藏 Sidebar / 隱藏漢堡 / 隱藏頁尾 / 放大畫布寬度
# -------------------------
GLOBAL_CSS = """
<style>
/* 完全隱藏 Sidebar 與展開控制 */
[data-testid="stSidebar"] { display: none !important; }
[data-testid="stSidebarNav"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }

/* 隱藏右上角的預設選單與頁尾 */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }

/* 放大主容器寬度與減少邊距，讓畫面更滿 */
.main .block-container {
    padding-top: 0.6rem;
    padding-bottom: 2rem;
    padding-left: 2rem;
    padding-right: 2rem;
    max-width: 1600px;
}

/* 置頂導覽列 */
.yc-topbar {
    position: sticky;
    top: 0;
    z-index: 999;
    background: white;
    border-bottom: 1px solid rgba(0,0,0,0.08);
    padding: 10px 16px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

/* 左側：品牌區 */
.yc-brand {
    display: flex;
    align-items: center;
    gap: 12px;
    font-weight: 600;
    font-size: 16px;
}

/* 右側：使用者區 */
.yc-user {
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 14px;
    color: #333;
}

/* Logo 圖片大小控制（自適應，避免擠壓） */
.yc-logo {
    height: 28px;
    width: auto;
    object-fit: contain;
}

/* 主要內容區塊的卡片風格 */
.yc-card {
    border: 1px solid rgba(0,0,0,0.08);
    border-radius: 14px;
    padding: 18px;
    background: #fff;
    box-shadow: 0 2px 12px rgba(0,0,0,0.04);
}

/* 登入表單卡片 */
.yc-login {
    max-width: 560px;
    margin: 56px auto 24px auto;
}
.yc-muted {
    color: #666;
    font-size: 13px;
}
</style>
"""
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# -------------------------
# 使用者授權名單（可直接改這段 TOML）
# -------------------------
AUTHORIZED_USERS = """
[authorized_users.admin]
name = "管理者"
username = "admin"
password = "xxx"
role = "admin"
start_date = "2025-01-01"
end_date = "2026-12-31"

[authorized_users.grace]
name = "Grace"
username = "grace"
password = "xxx"
role = "vip"
start_date = "2025-01-01"
end_date = "2026-12-31"

[authorized_users.user1]
name = "使用者一"
username = "user1"
password = "xxx"
role = "member"
start_date = "2025-05-01"
end_date = "2025-10-31"
"""

def parse_authorized_users(toml_str: str) -> Dict[str, Any]:
    # 盡量使用內建 tomllib（Python 3.11+），否則退回第三方 toml
    try:
        import tomllib
        data = tomllib.loads(toml_str)
    except Exception:
        import toml  # type: ignore
        data = toml.loads(toml_str)
    return data.get("authorized_users", {})

USERS = parse_authorized_users(AUTHORIZED_USERS)

def is_within_date_range(start: str, end: str, now: Optional[datetime] = None) -> bool:
    now = now or datetime.now()
    try:
        s = datetime.strptime(start, "%Y-%m-%d")
        e = datetime.strptime(end, "%Y-%m-%d")
        return s <= now <= e
    except Exception:
        # 若日期格式錯誤，謹慎起見視為不通過
        return False

def auth_check(username: str, password: str) -> Optional[Dict[str, Any]]:
    for key, u in USERS.items():
        if username == u.get("username") and password == u.get("password"):
            if is_within_date_range(u.get("start_date", "1900-01-01"), u.get("end_date", "2999-12-31")):
                return u
            else:
                return {"__expired__": True, **u}
    return None

# -------------------------
# Session 初始
# -------------------------
if "is_authenticated" not in st.session_state:
    st.session_state.is_authenticated = False
if "user" not in st.session_state:
    st.session_state.user = None

# -------------------------
# 置頂導覽列（登入前後都顯示；右側內容會依狀態變化）
# -------------------------
def render_topbar():
    # 左側品牌區：優先顯示 logo.png；若沒有就顯示文字
    logo_html = ""
    logo_path = Path("logo.png")
    if logo_path.exists():
        # 將圖片轉成 base64 嵌入
        import base64
        with open(logo_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        logo_html = f'<img class="yc-logo" src="data:image/png;base64,{b64}" alt="logo" />'
    else:
        # 沒有檔案時，顯示文字品牌
        logo_html = '<span style="font-weight:700;">《影響力》傳承策略平台</span>'

    # 右側使用者區
    if st.session_state.is_authenticated and st.session_state.user:
        u = st.session_state.user
        name = u.get("name", "")
        end_date = u.get("end_date", "")
        role = u.get("role", "")
        right = f"""
        <div class="yc-user">
            <span>😊 {name}｜有效期限：{end_date}</span>
        </div>
        """
    else:
        right = """
        <div class="yc-user">
            <span class="yc-muted">請先登入以使用平台</span>
        </div>
        """

    topbar = f"""
    <div class="yc-topbar">
        <div class="yc-brand">
            {logo_html}
            <span>《影響力》傳承策略平台</span>
        </div>
        {right}
    </div>
    """
    st.markdown(topbar, unsafe_allow_html=True)

render_topbar()

# -------------------------
# 登入表單（未登入時顯示）
# -------------------------
def render_login():
    st.markdown('<div class="yc-card yc-login">', unsafe_allow_html=True)
    st.subheader("登入平台")
    st.caption("請輸入帳號與密碼（帳號權限與有效期限已內建檢核）")

    with st.form("login_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        with col1:
            username = st.text_input("帳號（username）*")
        with col2:
            password = st.text_input("密碼（password）*", type="password")
        submitted = st.form_submit_button("登入", use_container_width=True)

    error_box = st.empty()
    st.markdown('</div>', unsafe_allow_html=True)

    if submitted:
        res = auth_check(username.strip(), password.strip())
        if res is None:
            error_box.error("帳號或密碼不正確，請再試一次。")
        elif "__expired__" in res:
            sd = res.get("start_date", "")
            ed = res.get("end_date", "")
            error_box.error(f"帳號已不在有效期間（{sd} ～ {ed}）。如需延長，請聯繫管理者。")
        else:
            st.session_state.is_authenticated = True
            st.session_state.user = res
            st.rerun()

# -------------------------
# 主內容（已登入後顯示）
# -------------------------
def render_main_content():
    st.markdown("### 👋 歡迎使用《影響力》傳承策略平台")
    st.markdown(
        "在這裡，我們以**準備與從容**的運動員哲學，協助高資產家庭完成："
        "富足退休、富裕一生、富貴傳承的完整解決方案。"
    )

    # 示意：主要功能入口（您可替換為實際模組）
    c1, c2, c3 = st.columns(3)
    with c1:
        with st.container(border=True):
            st.markdown("#### 📦 保單策略規劃")
            st.caption("為高資產家庭設計最適保障結構。")
            st.button("進入模組", key="go_policy", use_container_width=True)
    with c2:
        with st.container(border=True):
            st.markdown("#### 🧭 傳承地圖")
            st.caption("建立家族資產分類、風險視圖與行動建議。")
            st.button("進入模組", key="go_map", use_container_width=True)
    with c3:
        with st.container(border=True):
            st.markdown("#### 💬 永傳對話語庫™")
            st.caption("顧問語言設計：情境語句、引導問題、金句與話術。")
            st.button("進入模組", key="go_dialog", use_container_width=True)

    st.markdown("")
    with st.container(border=True):
        st.markdown("#### 最新公告")
        st.write(
            "- 若您需要新增使用者或延長到期日，請聯繫管理者。\n"
            "- Logo 建議尺寸：寬 240~360px（透明 PNG），檔名：`logo.png`。\n"
            "- Favicon 可放 `logo2.png`，系統將自動優先使用。"
        )

    st.markdown("")
    colL, colR = st.columns([1, 1])
    with colL:
        if st.button("🔓 登出", use_container_width=True):
            st.session_state.is_authenticated = False
            st.session_state.user = None
            st.rerun()
    with colR:
        st.caption("《影響力》傳承策略平台｜永傳家族辦公室  •  https://gracefo.com  •  聯絡信箱：123@gracefo.com")

# -------------------------
# 路由：依登入狀態渲染
# -------------------------
if st.session_state.is_authenticated:
    render_main_content()
else:
    render_login()
