ensure_page_config('永傳數位家族辦公室')
import sys, os

from ui_shared import ensure_page_config, render_header, render_footer
ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
import streamlit as st
from ui_shared import render_header, render_footer, save_doc, load_collection, get_user_id, send_email
render_header()

st.subheader("🛠️ 數位戰情室（管理）")
if not st.session_state.get("admin_ok"):
    pwd = st.text_input("管理密碼", type="password")
    if st.button("登入"):
        if pwd == "admin123":
            st.session_state["admin_ok"] = True
            st.rerun()
        else:
            st.error("密碼錯誤")
    raise SystemExit

tab1, tab2 = st.tabs(["潛在客戶 (B2C)", "顧問申請 (B2B)"])
with tab1:
    df = load_collection("lead_assessments")
    if not df.empty:
        st.metric("總潛在客戶數", len(df))
        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False).encode("utf-8-sig")
        st.download_button("下載潛在客戶 CSV", data=csv, file_name="leads.csv", mime="text/csv")
    else:
        st.info("尚無資料")
with tab2:
    df = load_collection("advisors_applications")
    if not df.empty:
        st.metric("總申請顧問數", len(df))
        st.dataframe(df, use_container_width=True)
        csv2 = df.to_csv(index=False).encode("utf-8-sig")
        st.download_button("下載顧問申請 CSV", data=csv2, file_name="advisors.csv", mime="text/csv")
    else:
        st.info("尚無資料")

render_footer()
