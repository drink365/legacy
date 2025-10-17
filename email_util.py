# -*- coding: utf-8 -*-
from __future__ import annotations
import os, smtplib, ssl
from typing import Iterable, List, Optional, Tuple, Union

try:
    import streamlit as st
except Exception:
    st = None

try:
    import tomllib as _toml  # py3.11+
except Exception:
    try:
        import toml as _toml  # type: ignore
    except Exception:
        _toml = None

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.utils import formataddr, make_msgid
from email import encoders

Addr = Union[str, Iterable[str]]

def _normalize_recipients(x: Optional[Addr]) -> List[str]:
    if not x:
        return []
    if isinstance(x, str):
        return [x]
    return [a for a in x if a]

def _from_secrets() -> Optional[dict]:
    if st is None:
        return None
    try:
        if "smtp" in st.secrets:
            return dict(st.secrets["smtp"])
    except Exception:
        pass
    return None

def _from_streamlit_secrets_env() -> Optional[dict]:
    raw = os.environ.get("STREAMLIT_SECRETS")
    if not raw or _toml is None:
        return None
    try:
        data = _toml.loads(raw)
        if isinstance(data, dict) and "smtp" in data:
            return dict(data["smtp"])
    except Exception:
        return None
    return None

def _from_env_vars() -> Optional[dict]:
    host = os.getenv("SMTP_HOST")
    if not host:
        return None
    return {
        "host": host,
        "port": int(os.getenv("SMTP_PORT", "587")),
        "user": os.getenv("SMTP_USER"),
        "pass": os.getenv("SMTP_PASS"),
        "use_tls": os.getenv("SMTP_USE_TLS", "true").lower() == "true",
    }

def load_smtp_cfg() -> dict:
    for loader in (_from_secrets, _from_streamlit_secrets_env, _from_env_vars):
        cfg = loader()
        if cfg:
            cfg["host"] = cfg.get("host") or cfg.get("HOST")
            cfg["port"] = int(cfg.get("port") or cfg.get("PORT") or 587)
            cfg["user"] = cfg.get("user") or cfg.get("USER")
            cfg["pass"] = cfg.get("pass") or cfg.get("PASSWORD") or cfg.get("PASS")
            use_tls = cfg.get("use_tls", cfg.get("USE_TLS", True))
            cfg["use_tls"] = bool(str(use_tls).lower() in ("1","true","yes","y","on"))
            if not (cfg["host"] and cfg["user"] and cfg["pass"]):
                continue
            return cfg
    raise RuntimeError("SMTP 設定未載入：請設定 st.secrets['smtp']、STREAMLIT_SECRETS 或 SMTP_* 環境變數。")

def send_email(
    to: Addr, subject: str, html: str, text: Optional[str]=None, *,
    cc: Optional[Addr]=None, bcc: Optional[Addr]=None, reply_to: Optional[str]=None,
    from_name: str="Grace Family Office", from_email: Optional[str]=None,
    attachments: Optional[List[Tuple[str, bytes, str]]]=None
) -> Tuple[bool, Optional[str]]:
    try:
        cfg = load_smtp_cfg()
    except Exception as e:
        return False, f"SMTP 設定載入失敗: {e}"

    to_list = _normalize_recipients(to)
    cc_list = _normalize_recipients(cc)
    bcc_list = _normalize_recipients(bcc)
    all_rcpts = [*to_list, *cc_list, *bcc_list]
    if not all_rcpts:
        return False, "缺少收件人"

    sender_email = from_email or cfg["user"]
    display_from = formataddr((from_name, sender_email))

    msg = MIMEMultipart("alternative")
    msg["From"] = display_from
    msg["To"] = ", ".join(to_list)
    if cc_list:
        msg["Cc"] = ", ".join(cc_list)
    msg["Subject"] = subject
    msg["Message-ID"] = make_msgid()
    if reply_to:
        msg["Reply-To"] = reply_to

    if not text:
        text = (html.replace("<br>", "\n")
                    .replace("<br/>", "\n")
                    .replace("<br />", "\n")
                    .replace("<p>", "\n")
                    .replace("</p>", "\n"))
    msg.attach(MIMEText(text, "plain", "utf-8"))
    msg.attach(MIMEText(html, "html", "utf-8"))

    if attachments:
        for filename, data, mime in attachments:
            maintype, _, subtype = (mime.partition("/") if "/" in mime else ("application","/","octet-stream"))
            part = MIMEBase(maintype, subtype)
            part.set_payload(data)
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f'attachment; filename="{filename}"')
            msg.attach(part)

    try:
        if cfg["use_tls"]:
            context = ssl.create_default_context()
            with smtplib.SMTP(cfg["host"], cfg["port"]) as server:
                server.ehlo()
                server.starttls(context=context)
                server.ehlo()
                server.login(cfg["user"], cfg["pass"])
                server.sendmail(sender_email, all_rcpts, msg.as_string())
        else:
            with smtplib.SMTP_SSL(cfg["host"], cfg["port"]) as server:
                server.login(cfg["user"], cfg["pass"])
                server.sendmail(sender_email, all_rcpts, msg.as_string())
        return True, None
    except Exception as e:
        return False, f"SMTP 寄送失敗: {e}"
