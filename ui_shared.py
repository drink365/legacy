# ui_shared.py — 精緻字寬按鈕（僅文字範圍淡底）＋ 隱藏側欄（正確順序）
# -*- coding: utf-8 -*-
from typing import Optional
import base64
from pathlib import Path
import streamlit as st

ASSETS_DIR = Path(__file__).parent / "assets"
LOGO_PATH = ASSETS_DIR / "logo.png"
FAVICON_PATH = ASSETS_DIR / "favicon.png"
TAGLINE = "專家洞見 × 智能科技 × 幸福傳承"

def ensure_page_config(
    page_title: str = "永傳家族辦公室",
    page_icon: Optional[str] = None,
    layout: str = "wide",
) -> None:
    """必須先 set_page_config，再注入任何 st.*"""
    icon = str(FAVICON_PATH) if FAVICON_PATH.exists() else (page_icon or "💠")

    if "page_config_set" not in st.session_state:
        st.set_page_config(
            page_title=page_title,
            page_icon=icon,
            layout=layout,
            initial_sidebar_state="collapsed",
        )
        st.session_state["page_config_set"] = True

    # 全站 CSS（字寬淡底按鈕＋隱藏側欄＋分隔線＋副標語）
    st.markdown("""
    <style>
      :root { --brand-navy:#091931; }

      /* 字寬按鈕：僅文字範圍淡底色（hover 稍加深） */
      .stPageLink{
        display:inline-block !important;
        width:auto !important;
        padding:4px 10px;
        border-radius:6px;
        background-color:rgba(0,0,0,0.02);
        transition:background-color .2s ease, color .2s ease;
      }
      .stPageLink a{
        color:#0B2545 !important;
        text-decoration:none !important;
        font-weight:700 !important;
      }
      .stPageLink:hover{ background-color:rgba(0,0,0,0.07); }

      /* 隱藏側欄與開關（雙保險；.streamlit/config.toml 仍建議啟用 showSidebarNavigation=false） */
      [data-testid="stSidebar"], [data-testid="collapsedControl"] { display:none !important; }

      /* 放大副標語 */
      .subtitle-tagline{
        font-size:24px; font-weight:700; color:#145DA0; letter-spacing:.5px; text-align:center;
      }

      /* 頂部下方分隔線 */
      .yc-top-hr{ margin-top:0; margin-bottom:24px; border-top:1px solid #eee; }
    </style>
    """, unsafe_allow_html=True)

def _logo_img_b64(width_px: int = 180) -> str:
    b64 = None
    try:
        path = LOGO_PATH if LOGO_PATH.exists() else (FAVICON_PATH if FAVICON_PATH.exists() else None)
        if path:
            b64 = base64.b64encode(path.read_bytes()).decode("utf-8")
    except Exception as e:
        print(f"⚠️ 無法讀取 Logo：{e}")

    if b64:
        return (
            f'<a href="/" target="_self" style="text-decoration:none;">'
            f'<img src="data:image/png;base64,{b64}" width="{width_px}" style="display:block;cursor:pointer;">'
            f'</a>'
        )
    return f'<div style="width:{width_px}px;height:40px;border:1px dashed var(--brand-navy);display:flex;align-items:center;justify-content:center;color:var(--brand-navy);font-weight:700;">LOGO</div>'

def render_header(logo_width_px: int = 180, show_tagline: bool = False) -> None:
    cols = st.columns([1.5, 1, 1, 1])
    with cols[0]:
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:10px;white-space:nowrap;">{_logo_img_b64(logo_width_px)}</div>',
            unsafe_allow_html=True,
        )
    with cols[1]:
        st.page_link("pages/blueprint.py", label="幸福傳承藍圖")
    with cols[2]:
        st.page_link("pages/dataroom.py", label="數位戰情室")
    with cols[3]:
        st.page_link("pages/4_contact.py", label="📞 聯絡我們")

    st.markdown("<hr class='yc-top-hr'>", unsafe_allow_html=True)

    if show_tagline:
        st.markdown(f"<div class='subtitle-tagline'>{TAGLINE}</div>", unsafe_allow_html=True)

def render_footer() -> None:
    st.markdown("---")
    st.markdown(
        "<div style='text-align:center;font-size:12px;color:#999;padding:10px 0;'>"
        "永傳家族辦公室 © 2025. All rights reserved. | "
        "<a href='mailto:123@gracefo.com' style='color:#999;text-decoration:none;'>聯絡我們</a>"
        "</div>",
        unsafe_allow_html=True,
    )
