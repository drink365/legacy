ensure_page_config('永傳數位家族辦公室')
import sys, os

from ui_shared import ensure_page_config, render_header, render_footer
ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
import streamlit as st
from ui_shared import render_header, render_footer, save_doc, load_collection, get_user_id, send_email
render_header()

st.subheader("🏠 客戶專區")
st.page_link("pages/9_risk_check.py", label="先做個 1 分鐘初診 →", use_container_width=True)
st.page_link("pages/4_contact.py", label="預約傳承導師 →", use_container_width=True)

render_footer()
