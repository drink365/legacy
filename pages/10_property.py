ensure_page_config('永傳數位家族辦公室')
import sys, os

from ui_shared import ensure_page_config, render_header, render_footer
ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
import streamlit as st
from ui_shared import render_header, render_footer, save_doc, load_collection, get_user_id, send_email
render_header()

st.subheader("🏛️ 資產與不動產")
st.write("- 與稅務模組協作，讓配置更有效率與彈性。")
st.page_link("pages/7_asset_map.py", label="開啟資產地圖 →", use_container_width=True)

render_footer()
