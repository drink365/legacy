import base64
from pathlib import Path
import streamlit as st
from app_config import ensure_page_config

# ✅ 統一設定 favicon、版面配置（全站適用）
ensure_page_config()

# ------------------------
# Page config
# ------------------------
APP_TITLE = "永傳家族傳承導師｜影響力傳承平台"
root = Path(__file__).parent
fav = root / "favicon.png"
if fav.exists():
    pass
# favicon handled globally by ensure_page_config()

# ------------------------
# Global styles
# ------------------------
st.markdown(
    """
<style>
[data-testid="stSidebar"], [data-testid="stSidebarNav"], [data-testid="collapsedControl"] { display: none !important; }
.stAppDeployButton, button[kind="header"], [data-testid="BaseButton-header"], [data-testid="stToolbar"] { display: none !important; }
[data-testid="stAppViewContainer"] .main .block-container { max-width: 1280px; padding-left: 24px; padding-right: 24px; }
.hero h1 { font-size: 42px; font-weight: 800; margin: 0 0 8px; color: #004c4c; letter-spacing: .5px; }
.hero p  { font-size: 20px; color: #333; line-height: 1.8; margin: 0; }
.hero .cta { display:inline-block; margin-top: 20px; background:#006666; color:#fff; padding:12px 24px; border-radius:10px; text-decoration:none; font-weight:600; }
.section { margin-top: 40px; }
.section h2 { font-size: 28px; margin-bottom: 10px; color: #004c4c; }
.section p  { color:#333; }
.divider { height: 1px; background: #e9ecef; margin: 36px 0; }
.cards { display:flex; gap:20px; flex-wrap:wrap; justify-content:center; }
.card { width: 320px; padding: 20px; border-radius: 14px; background: #ffffff; box-shadow: 0 2px 14px rgba(0,0,0,.06); text-align: left; }
.card h3 { margin: 0 0 8px; }
.card p  { margin: 0; color:#444; line-height:1.7; }
.footer { display:flex; justify-content:center; align-items:center; gap: 1.25rem; font-size: 14px; color: gray; }
.footer a { color:#006666; text-decoration: underline; }
.anchor { position: relative; top: -80px; visibility: hidden; }
</style>
""",
    unsafe_allow_html=True,
)

# ------------------------
# Assets helpers
# ------------------------
def load_b64(p: Path) -> str | None:
    try:
        with p.open("rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return None

logo_b64 = load_b64(root / "logo.png")
qr_b64 = load_b64(root / "qrcode.png")

# ------------------------
# Header / Brand
# ------------------------
with st.container():
    if logo_b64:
        st.markdown(
            f"""
            <div style='text-align:center;margin-top:8px;'>
              <img src='data:image/png;base64,{logo_b64}' width='200' alt='logo'/>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class='hero' style='text-align:center; margin-top: 10px;'>
          <h1>讓傳承，成為愛的延續</h1>
          <p>
            《影響力》是一個結合 <b>AI</b> 與 <b>專業顧問智慧</b> 的傳承策略平台，
            專為高資產家庭打造，陪你完成 <b>資產配置</b>、<b>稅務節省</b> 與 <b>跨世代安排</b>。
          </p>
          <a href="#get-started" class="cta">了解如何開始規劃</a>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ------------------------
# 品牌使命（含影片封面）
# ------------------------
st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
st.markdown(
    """
<div class='section'>
  <h2>品牌使命</h2>
  <p>
    我們相信，每個家庭的成功都值得被延續。<br/>
    《影響力》致力於推動財富傳承教育，以專業顧問與科技工具，
    協助家族以更低成本、更高效率，完成愛與責任的交棒。
  </p>
</div>
""",
    unsafe_allow_html=True,
)

# ------------------------
# ▶ 2 分鐘了解《影響力》（使用封面圖＋頻道連結）
# ------------------------
with st.expander("▶ 2 分鐘了解《影響力》（永傳科創學院）", expanded=False):
    st.image("ace3079b-b394-41c4-bc30-f7815a903161.png", use_container_width=True)
    st.markdown(
        "[前往永傳科創學院 YouTube 頻道 🎥](https://www.youtube.com/@gracefo)",
        unsafe_allow_html=True,
    )

with st.expander("💬 來自客戶與顧問的回饋", expanded=False):
    st.markdown("- \"有結構、有溫度，讓家人快速形成共識。\"")
    st.markdown("- \"把保單、稅務與信託用同一張圖講清楚，效率大幅提升。\"")

# ------------------------
# Final CTA
# ------------------------
st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
st.markdown(
    """
<div class='section' style='text-align:center;'>
  <h2>準備好開始你的家族傳承旅程了嗎？</h2>
  <p>留下聯繫方式，或直接以右下角 QR code 與我們聯繫。</p>
</div>
""",
    unsafe_allow_html=True,
)

cols = st.columns([1,1,1])
with cols[1]:
    st.markdown(
        """
        <div style='display:flex;gap:12px;justify-content:center;align-items:center;'>
          <a href='#role' class='cta' style='background:#006666;color:#fff;padding:10px 18px;border-radius:10px;text-decoration:none;'>馬上開始</a>
          <a href='mailto:123@gracefo.com' class='cta' style='background:#004c4c;color:#fff;padding:10px 18px;border-radius:10px;text-decoration:none;'>預約顧問</a>
        </div>
        """,
        unsafe_allow_html=True,
    )

if qr_b64:
    st.markdown(
        f"""
        <div style='text-align:center;margin-top:14px;'>
          <img src='data:image/png;base64,{qr_b64}' width='120' alt='contact-qr'/>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ------------------------
# Footer
# ------------------------
st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
st.markdown(
    """
    <div class='footer'>
      <a href='?' >《影響力》傳承策略平台</a>
      <a href='https://gracefo.com' target='_blank'>永傳家族辦公室</a>
      <a href='mailto:123@gracefo.com'>123@gracefo.com</a>
    </div>
    """,
    unsafe_allow_html=True,
)
