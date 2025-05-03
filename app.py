import streamlit as st

# 頁面設定
st.set_page_config(
    page_title="永傳家族傳承教練",
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
        content: "永傳家族辦公室";
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
    """,
    unsafe_allow_html=True,
)

# 讀取 URL 參數以決定分流
query_params = st.experimental_get_query_params()
mode = query_params.get("mode", [None])[0]

# 顯示麵包屑
if mode:
    label = "顧問版工具" if mode == "advisor" else "家族版工具"
    st.markdown(
        f"<div class='breadcrumb'>🏠 <a href='?'>首頁</a> &gt; {label}</div>",
        unsafe_allow_html=True,
    )

# 根據模式渲染主頁或對應模組
if not mode:
    # 首頁
    st.markdown("<h1 style='text-align:center;'>永傳家族傳承教練</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align:center; font-size:18px;'>傳承，不只是留資產，更是留心意。</p>",
        unsafe_allow_html=True,
    )
    # 分流按鈕
    col1, col2 = st.columns(2)
    with col1:
        if st.button("家族版工具", key="family_btn", help="家族版：快速釐清您的傳承重點", on_click=lambda: st.experimental_set_query_params(mode="family")):
            pass
    with col2:
        if st.button("顧問版工具", key="advisor_btn", help="顧問版：專業工具＋報告生成", on_click=lambda: st.experimental_set_query_params(mode="advisor")):
            pass

elif mode == "family":
    # 家族版主程式入口
    from client_home import main as client_main
    client_main()

elif mode == "advisor":
    # 顧問版主程式入口
    from advisor_home import main as advisor_main
    advisor_main()

# 底部溫暖落款
st.markdown(
    "<div style='text-align:center; margin-top:2em; font-size:12px; color:#777;'>期待與您一起，讓影響力永續傳承 ❤️</div>",
    unsafe_allow_html=True,
)
