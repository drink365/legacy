# 優化重點（2025-10-12）

- 套用溫暖親切的品牌主題（深海藍 × 明亮藍 × 金色 × 柔白）。
- 使用 `ui_shared.py` 集中管理 Header / Footer / Hero 與品牌色，Logo 以 Base64 顯示避免模糊。
- 新增 `.streamlit/config.toml`：一致色系、隱藏多餘 UI。
- `index.py` 與 `app.py` 以「商業策略平台」視角重寫文案。
- `pages/4_contact.py` 自動帶入共用頁首／頁尾。
- 仍可沿用既有模組；若需登入/授權，請在 `st.session_state["auth_user"]` 放入 `{ "name": "Grace", "end_date": "2026-12-31" }` 以顯示右上角狀態列。

## 郵件／Secrets 提示
若使用 `email_util.py` 寄信，請在部署環境設定下列變數：
- `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`, `MAIL_FROM`, `MAIL_TO_DEFAULT`