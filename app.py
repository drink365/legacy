import streamlit as st

# 頁面設定
st.set_page_config(
    page_title="《影響力》 | 高資產家庭的傳承策略入口",
    page_icon="🌿",
    layout="wide",
)

# 隱藏 Streamlit 默認選單與側邊欄，保留品牌影響力在 footer
st.markdown(
    """
    <style>
      #MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
      footer:after {
        content: "《影響力》";
        display: block;
        color: #BBB;
        padding: 5px;
        font-size: 12px;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# 品牌色設定
BRAND_COLOR = "#2C5F2D"  # 深綠色

# 自訂按鈕與麵包屑樣式
st.markdown(
    f"""
    <style>
      .big-button {{
          background-color: {BRAND_COLOR};
          color: white;
          font-size: 24px;
          padding: 1em 2em;
          border-radius: 10px;
          margin: 0.5em;
          border: none;
      }}
      .big-button:hover {{
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
      }}
      .breadcrumb {{
          font-size: 14px;
          color: #555;
          margin-bottom: 1em;
      }}
      .footer-container a {{
          color: gray;
          text-decoration: none;
          margin: 0 1em;
      }}
      .footer-container a.primary-link {{
          color: {BRAND_COLOR};
          text-decoration: underline;
      }}
      .footer-container a.primary-link:hover {{
          color: #1A3B1A;
      }}
    </style>
    """,
    unsafe_allow_html=True,
)

# 讀取 URL 參數以決定分流
query_params = st.query_params
mode = query_params.get("mode", [None])[0]

# 顯示麵包屑
if mode:
    label = "顧問版工具" if mode == "advisor" else "家族版工具"
    st.markdown(
        f"<div class='breadcrumb'>🏠 <a href='?'>首頁</a> &gt; {label}</div>",
        unsafe_allow_html=True,
    )

# 主頁或模組入口
if not mode:
    # 首頁 Logo 與說明
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.image("logo.png", use_container_width=True)
        st.markdown(
            """
            <div style='text-align:center; margin-top:20px;'>
              <h1>《影響力》 | 高資產家庭的傳承策略入口</h1>
              <p style='font-size:18px; color:#555;'>在這裡，我們陪伴您釐清家族傳承重點，打造專屬的永續傳承方案。</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    # 分流按鈕
    st.markdown("<div style='text-align:center; margin-top:30px;'>", unsafe_allow_html=True)
    if st.button("家族版工具", key="family_btn", help="家族版：快速釐清您的傳承重點", on_click=lambda: st.experimental_set_query_params(mode="family")):
        pass
    st.write(" ")
    if st.button("顧問版工具", key="advisor_btn", help="顧問版：專業工具＋報告生成", on_click=lambda: st.experimental_set_query_params(mode="advisor")):
        pass
    st.markdown("</div>", unsafe_allow_html=True)

elif mode == "family":
    from client_home import main as client_main
    client_main()

elif mode == "advisor":
    from advisor_home import main as advisor_main
    advisor_main()

# 溫暖落款
st.markdown(
    """
    <div style='text-align:center; margin-top:2em; font-size:12px; color:#777;'>
      期待與您一起，讓《影響力》永續傳承 ❤️
    </div>
    """,
    unsafe_allow_html=True,
)

# --- 聯絡資訊 ---
st.markdown("---")
st.markdown(
    """
    <div class='footer-container' style='display:flex; justify-content:center; align-items:center; font-size:14px; color:gray; margin-top:10px;'>
      <a href='?' class='primary-link'>《影響力》傳承策略平台</a>
      <a href='https://gracefo.com' target='_blank'>永傳家族辦公室</a>
      <a href='mailto:123@gracefo.com'>123@gracefo.com</a>
    </div>
    """,
    unsafe_allow_html=True,
)
