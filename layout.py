
import streamlit as st
from typing import List, Tuple

PRIMARY = "#145DA0"
SECONDARY = "#2E8BC0"
GOLD = "#F9A826"
BG = "#F7FAFC"
INK = "#1F2937"

B2C_NAV = [("home_b2c", "首頁"), ("blueprint", "我的藍圖"), ("mentor", "導師陪伴"), ("contact", "對話邀約")]
B2B_NAV = [("home_b2b", "首頁"), ("warroom", "我的戰情室"), ("sim", "模擬器"), ("crm", "客戶儀表板"), ("academy", "導師學院")]

def base_css():
    st.markdown(f"""
    <style>
      #MainMenu{{visibility:hidden}} footer{{visibility:hidden}} header{{visibility:hidden}}
      .stApp {{ background:{BG}; }}
      .block-container {{ padding-top:0 !important; padding-left:0; padding-right:0; }}
      html, body, [class*="css"] {{ font-family: -apple-system, BlinkMacSystemFont, "Noto Sans TC", "Segoe UI", Roboto, "Helvetica Neue", Arial, "PingFang TC", "Heiti TC", sans-serif; }}
      .yc-header {{ position:sticky; top:0; z-index:999; background:#fff; border-bottom:1px solid #eef2f7; }}
      .yc-container {{ max-width: 1180px; margin: 0 auto; padding: 12px 24px; }}
      .yc-brand {{ color:{PRIMARY}; font-weight:900; font-size: 18px; white-space:nowrap; }}
      .yc-nav a {{ color:#6b7280; text-decoration:none; font-weight:600; margin: 0 10px; }}
      .yc-nav a.active, .yc-nav a:hover {{ color:{PRIMARY}; }}
      .yc-cta {{ background:{PRIMARY}; color:#fff; padding:8px 14px; border-radius:12px; font-weight:800; text-decoration:none; }}
      .yc-cta:hover {{ background:#0f4a80; }}
      .yc-footer {{ background:#111827; color:#fff; padding:28px 0; margin-top:40px; }}
      .yc-footer a {{ color:#fff; text-decoration: underline; }}
      .yc-card {{ background:#fff; border:1px solid #e5e7eb; border-radius:16px; padding:18px; }}
      .yc-title {{ color:{PRIMARY}; font-weight:900; }}
      .yc-sub {{ color:{SECONDARY}; font-weight:800; }}
      .yc-chip {{ display:inline-block; padding:6px 10px; border-radius:999px; background:#e8f1fb; color:{PRIMARY}; font-weight:700; }}
      .btn-primary{{ background:{PRIMARY}; color:#fff; padding:10px 16px; border-radius:12px; font-weight:800; text-decoration:none;}}
      .btn-primary:hover{{ background:#0f4a80; }}
    </style>
    """, unsafe_allow_html=True)

def header(role: str, active_key: str):
    st.markdown('<div class="yc-header">', unsafe_allow_html=True)
    st.markdown('<div class="yc-container" style="display:flex; align-items:center; justify-content:space-between;">', unsafe_allow_html=True)
    st.markdown('<div class="yc-brand">永傳家族傳承生態系</div>', unsafe_allow_html=True)

    if role == "b2c":
        nav = B2C_NAV
        prefix = "/?r=b2c&p="
        cta = "/?r=b2c&p=contact"
    elif role == "b2b":
        nav = B2B_NAV
        prefix = "/?r=b2b&p="
        cta = "/?r=b2b&p=crm"
    else:
        nav = []
        prefix = "/"
        cta = "/?r=b2c&p=contact"

    if nav:
        nav_html = '<div class="yc-nav" style="display:flex; align-items:center; gap:8px;">'
        for key, label in nav:
            href = f"{prefix}{key}"
            cls = "active" if key == active_key else ""
            nav_html += f'<a class="{cls}" href="{href}">{label}</a>'
        nav_html += '</div>'
        st.markdown(nav_html, unsafe_allow_html=True)
    else:
        st.markdown('<div></div>', unsafe_allow_html=True)

    st.markdown(f'<a class="yc-cta" href="{cta}">對話邀約</a>', unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)

def footer():
    st.markdown(
        """
        <div class="yc-footer">
          <div class="yc-container" style="text-align:center;">
            <div>《影響力》傳承策略平台｜永傳家族辦公室</div>
            <div><a href="https://gracefo.com" target="_blank" rel="noopener">https://gracefo.com</a></div>
            <div>聯絡信箱：<a href="mailto:123@gracefo.com">123@gracefo.com</a></div>
            <div style="opacity:.75; font-size:12px; margin-top:6px;">© 2025 永傳家族傳承導師 All rights reserved.</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True
    )
