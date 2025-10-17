
import streamlit as st
from layout import base_css, header, footer

st.set_page_config(page_title="永傳家族傳承生態系｜雙入口", page_icon="💎", layout="wide", initial_sidebar_state="collapsed")

base_css()
header("index", active_key="")

st.markdown("""
<section class="yc-container" style="padding:48px 24px;">
  <h1 class="yc-title" style="font-size:40px;">一場對話，讓傳承更被理解</h1>
  <p style="font-size:18px; color:#374151; max-width:760px;">
    專家洞見 × 智能科技 × 幸福傳承。請選擇您的身分，進入對應的服務入口。
  </p>
  <div style="display:grid; grid-template-columns: 1fr 1fr; gap:22px; margin-top:22px;">
    <a class="yc-card" href="/?r=b2c&p=home_b2c" style="text-decoration:none; color:inherit;">
      <div class="yc-chip">我是家族</div>
      <h2 class="yc-sub" style="font-size:26px; margin:6px 0;">幸福傳承數位藍圖</h2>
      <p>把複雜的傳承，變成看得懂、做得到、能長久的路徑。</p>
    </a>
    <a class="yc-card" href="/?r=b2b&p=home_b2b" style="text-decoration:none; color:inherit;">
      <div class="yc-chip">我是顧問</div>
      <h2 class="yc-sub" style="font-size:26px; margin:6px 0;">數位戰情室顧問計畫</h2>
      <p>讓專業被科技賦能，讓智慧被看見。</p>
    </a>
  </div>
</section>
""", unsafe_allow_html=True)

footer()
