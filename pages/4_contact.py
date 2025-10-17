# pages/4_contact.py — 聯絡我們（必填＋SMTP寄信＋提示固定在送出鍵下方＋成功後清空）
# -*- coding: utf-8 -*-
from ui_shared import ensure_page_config, render_header, render_footer
import streamlit as st
import re, smtplib, ssl
from email.mime.text import MIMEText
from email.utils import formataddr

# ---------- 基本頁面 ----------
ensure_page_config(page_title="永傳家族辦公室｜聯絡我們")
render_header(logo_width_px=180, show_tagline=False)

st.markdown("## 聯絡我們")
st.write("留下您的需求與聯絡方式，我們將盡快與您安排一對一諮詢。")

# ---------- 常數 ----------
TOPIC_OPTIONS = [
    "（請選擇）",
    "家族傳承藍圖設計",
    "股權與現金流規劃",
    "跨境財稅／信託架構",
    "超大額保單配置",
    "其他（請在下方說明）",
]

# ---------- 若上一輪要求重置，需在建立元件「之前」清理 state ----------
if st.session_state.get("cf_reset"):
    for k in ("cf_name", "cf_email", "cf_phone", "cf_topic", "cf_msg"):
        if k in st.session_state:
            del st.session_state[k]
    st.session_state["cf_reset"] = False

# 預設值
st.session_state.setdefault("cf_name", "")
st.session_state.setdefault("cf_email", "")
st.session_state.setdefault("cf_phone", "")
st.session_state.setdefault("cf_topic", TOPIC_OPTIONS[0])
st.session_state.setdefault("cf_msg", "")

# ---------- 寄信工具（優先 587/STARTTLS，失敗退到 465/SSL） ----------
def send_email(subject: str, html_body: str, to_addr: str):
    smtp = st.secrets["smtp"]
    host = smtp.get("host", "")
    port = int(smtp.get("port", 587))
    user = smtp.get("user", "")
    pwd  = smtp.get("pass", "")
    use_tls = bool(smtp.get("use_tls", True))
    from_name = "永傳家族辦公室"
    from_addr = user  # 提升投遞成功率：From = 登入帳號

    msg = MIMEText(html_body, "html", "utf-8")
    msg["Subject"] = subject
    msg["From"] = formataddr((from_name, from_addr))
    msg["To"] = to_addr

    if use_tls and port == 587:
        try:
            server = smtplib.SMTP(host, 587, timeout=20)
            server.ehlo()
            server.starttls(context=ssl.create_default_context())
            server.ehlo()
            server.login(user, pwd)
            server.sendmail(from_addr, [to_addr], msg.as_string())
            server.quit()
            return "587/STARTTLS"
        except Exception as e_starttls:
            try:
                with smtplib.SMTP_SSL(host, 465, context=ssl.create_default_context(), timeout=20) as server:
                    server.login(user, pwd)
                    server.sendmail(from_addr, [to_addr], msg.as_string())
                return "465/SSL"
            except Exception as e_ssl:
                raise RuntimeError(f"SMTP 送信失敗；587錯誤：{e_starttls}；465錯誤：{e_ssl}")
    # 非 587 或未開 TLS：直接 465/SSL
    with smtplib.SMTP_SSL(host, 465, context=ssl.create_default_context(), timeout=20) as server:
        server.login(user, pwd)
        server.sendmail(from_addr, [to_addr], msg.as_string())
    return "465/SSL"

# ---------- 表單 ----------
with st.form("contact_form", clear_on_submit=False):
    name  = st.text_input("您的姓名 *", key="cf_name")
    email = st.text_input("Email *", key="cf_email")
    phone = st.text_input("連絡電話 *", key="cf_phone")
    topic = st.selectbox("想了解的主題 *", TOPIC_OPTIONS, key="cf_topic")
    msg   = st.text_area("您的情況或問題（請簡述） *", height=150, key="cf_msg")

    # 送出鍵下方的提示容器（固定位置）
    feedback = st.empty()

    submitted = st.form_submit_button("送出")

    if submitted:
        # 驗證
        missing = []
        if not name.strip(): missing.append("姓名")
        if not email.strip():
            missing.append("Email")
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            feedback.error("請輸入有效的 Email 格式。"); st.stop()
        if not phone.strip():
            missing.append("連絡電話")
        elif not re.match(r"^[0-9+\-\s()]{6,20}$", phone):
            feedback.error("請輸入有效的電話格式（可包含數字、+、-、空格）。"); st.stop()
        if topic == "（請選擇）": missing.append("想了解的主題")
        if not msg.strip(): missing.append("您的情況或問題")

        if missing:
            feedback.error("請填寫以下必填欄位：" + "、".join(missing))
            st.stop()

        # 信件內容
        admin_to = st.secrets["smtp"].get("to", "")
        admin_recipients = [a.strip() for a in admin_to.split(",") if a.strip()]

        admin_html = f"""
        <h3>【新聯絡表單】永傳家族辦公室</h3>
        <p><b>姓名：</b>{name}</p>
        <p><b>Email：</b>{email}</p>
        <p><b>電話：</b>{phone}</p>
        <p><b>主題：</b>{topic}</p>
        <p><b>訊息：</b><br/>{msg.replace('\n','<br/>')}</p>
        """
        user_html = f"""
        <p>{name} 您好，感謝您聯絡永傳家族辦公室。</p>
        <p>我們已收到您的需求，顧問將於 1～2 個工作日內與您聯繫。</p>
        <hr/>
        <p><b>您送出的資訊</b></p>
        <p><b>主題：</b>{topic}<br/>
           <b>內容：</b><br/>{msg.replace('\n','<br/>')}</p>
        <p>若需立即安排，歡迎直接回覆此信。</p>
        """

        try:
            for rcpt in admin_recipients or [st.secrets["smtp"]["user"]]:
                send_email("【永傳】新聯絡表單通知", admin_html, rcpt)
            send_email("我們已收到您的聯絡資訊｜永傳家族辦公室", user_html, email)

            # 不在此輪顯示成功，改用 flash 讓「下一輪、同一位置」顯示
            st.session_state["cf_flash"] = ("success", "感謝您！表單已送出，我們已寄出確認信件，顧問將盡快與您聯繫。")
            st.session_state["cf_reset"] = True
            st.rerun()

        except Exception as e:
            # 送信失敗，立即在同一位置顯示錯誤（不 rerun）
            feedback.error("表單已送出，但寄信時發生問題，請稍後再試或直接來信。")
            st.caption(f"(技術訊息：{e})")

# ★ 在表單區塊之後，立刻渲染快取的提示（確保畫面位置在送出鍵正下方）
post_form_feedback = st.empty()
if "cf_flash" in st.session_state:
    level, message = st.session_state.pop("cf_flash")
    if level == "success":
        post_form_feedback.success(message)
    elif level == "error":
        post_form_feedback.error(message)

# ---------- 頁尾 ----------
st.markdown("---")
st.markdown("### 你也可以：")
c1, c2 = st.columns(2)
with c1:
    st.page_link("pages/blueprint.py", label="💎 了解永續傳承藍圖")
with c2:
    st.page_link("pages/dataroom.py", label="📊 查看數位戰情室")

render_footer()
