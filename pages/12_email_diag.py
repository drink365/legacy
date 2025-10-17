import os, sys
import streamlit as st
from ui_shared import ensure_page_config, render_header, render_footer, save_doc, load_collection, get_user_id, send_email
ensure_page_config()
render_header()

import ssl, smtplib, traceback
from email.message import EmailMessage
st.subheader("📧 Email Diagnostics（僅測試用頁面）")
mode = st.selectbox("模式", ["自動偵測（優先 [smtp]）", "只用 [smtp]", "只用 [gmail]"])
subject = st.text_input("測試主旨", "【測試】永傳官網郵件診斷")
body = st.text_area("測試內文", "這是一封測試郵件，用來驗證 SMTP 設定是否正確。")
override_to = st.text_input("覆寫收件者（空白則用 secrets 的 to）", "")
if st.button("送出測試信", type="primary"):
    try:
        smtp_cfg = dict(st.secrets.get("smtp", {}))
        gmail_cfg = dict(st.secrets.get("gmail", {}))
        use_smtp = (mode != "只用 [gmail]") and smtp_cfg
        if use_smtp:
            host = smtp_cfg.get("host", "smtp.gmail.com")
            port = int(smtp_cfg.get("port", 587))
            user = smtp_cfg.get("user")
            pwd  = smtp_cfg.get("pass") or smtp_cfg.get("password")
            use_tls = bool(smtp_cfg.get("use_tls", True))
            to_str = override_to or smtp_cfg.get("to", user or "")
        else:
            host = "smtp.gmail.com"; port = 465; use_tls = False
            user = gmail_cfg.get("user")
            pwd  = gmail_cfg.get("app_password") or gmail_cfg.get("pass")
            to_str = override_to or gmail_cfg.get("to", user or "")
        if not (user and pwd and to_str):
            st.error("Secrets 設定不完整。"); st.stop()
        recips = [e.strip() for e in to_str.replace(";", ",").split(",") if e.strip()]
        msg = EmailMessage(); msg["Subject"]=subject; msg["From"]=user; msg["To"]=", ".join(recips); msg.set_content(body)
        st.write(f"使用主機：{host} / 埠：{port} / TLS：{use_tls} / 帳號：{user}")
        if use_tls and port == 587:
            with smtplib.SMTP(host, port, timeout=20) as s:
                s.ehlo(); s.starttls(context=ssl.create_default_context()); s.login(user, pwd); s.send_message(msg)
        else:
            with smtplib.SMTP_SSL(host, port, timeout=20) as s:
                s.login(user, pwd); s.send_message(msg)
        st.success("✅ 測試信已送出！請檢查收件匣（與垃圾信件匣）。")
    except Exception as e:
        st.error("❌ 寄送失敗")
        st.code("".join(traceback.format_exception_only(type(e), e)))
        st.code("".join(traceback.format_exc()))

render_footer()
