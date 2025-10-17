# pages/advisor_home.py — 顧問夥伴計畫（與全站一致的美術與體驗）
# -*- coding: utf-8 -*-
import streamlit as st
from ui_shared import ensure_page_config, render_header, render_footer

# 統一設定（使用站內樣式與字寬淡底按鈕）
ensure_page_config(page_title="顧問夥伴計畫｜永傳家族辦公室")
render_header(logo_width_px=180, show_tagline=False)

# ===== Hero =====
st.markdown("""
<div style="
  background:#0B2545; color:#fff; border-radius:12px;
  padding:36px 24px; box-shadow:0 10px 30px rgba(9,25,49,.25);
">
  <div style="display:flex; flex-direction:column; gap:8px; align-items:center; text-align:center;">
    <div style="font-size:14px; font-weight:800; letter-spacing:.6px; padding:6px 12px;
                background:#00A896; color:#fff; border-radius:4px; display:inline-block;">
      顧問 × 數據 × 長期陪伴
    </div>
    <div style="font-size:36px; font-weight:800; line-height:1.2; margin-top:6px;">
      顧問夥伴計畫：把你的專業放大 10 倍的「數位戰情室」
    </div>
    <div style="max-width:920px; color:rgba(255,255,255,.85); font-size:16px; line-height:1.8;">
      我們相信，工具不會取代顧問；工具讓顧問的判斷更精準、溝通更有效、服務更持久。
      永傳以「家族傳承藍圖」為核心，以「數位戰情室」為引擎，讓你的專業被看見、被信任、被持續採用。
    </div>
    <div style="display:flex; gap:12px; flex-wrap:wrap; margin-top:12px;">
""", unsafe_allow_html=True)
# 站內一致的「字寬淡底」按鈕
st.page_link("pages/4_contact.py", label="📩 申請成為合作顧問")
st.page_link("pages/dataroom.py", label="📊 了解數位戰情室")
st.page_link("pages/blueprint.py", label="💎 查看傳承藍圖")
st.markdown("</div></div></div>", unsafe_allow_html=True)

st.markdown("")  # 間距

# ===== 區塊：我們放大的 4 件事 =====
st.markdown("### 我們幫你把哪些價值放大？")
col1, col2, col3, col4 = st.columns(4)
cards = [
    ("🎯 精準診斷", "#1a4d99", "以結構化盤點工具，快速聚焦 20% 決策重點，縮短溝通學習曲線。"),
    ("📐 可執行的藍圖", "#004c4c", "把顧問建議轉為「節點與清單」，能交付律師/會計師直接落地。"),
    ("📈 數據模擬", "#8a5800", "長期視角試算股權、稅負、現金流，幫你用數字說服決策者。"),
    ("🔁 長期陪伴", "#4d4d4d", "年度複盤＋版本管理，讓顧問關係由一次服務升級為長期顧問。"),
]
for col, (title, color, text) in zip([col1, col2, col3, col4], cards):
    with col:
        st.markdown(f"""
        <div style="background:#fff;border-top:5px solid {color};
            padding:16px;border-radius:12px;box-shadow:0 4px 12px rgba(0,0,0,.08); height:100%;">
          <div style="font-weight:800;font-size:18px;color:{color};margin-bottom:6px;">{title}</div>
          <div style="color:#555; font-size:14px; line-height:1.7;">{text}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ===== 區塊：合作模式（三步） =====
st.markdown("### 合作模式：三步就位")
step1, step2, step3 = st.columns(3)
with step1:
    st.markdown("""
    **① 啟動與啟蒙**  
    - 共同定義你的服務邏輯與客群  
    - 建立顧問帳號與標準作業（SOP）  
    - 提供戰情室快速入門教學
    """)
with step2:
    st.markdown("""
    **② 客案佈署**  
    - 將既有專案上線：建立資產地圖、節點、文檔  
    - 設定試算模板與報表視圖  
    - 對接你既有律師/會計師夥伴
    """)
with step3:
    st.markdown("""
    **③ 長期複盤**  
    - 季度／年度複盤與版本管理  
    - 變動節點追蹤（股權、稅法、現金流）  
    - 客戶續約與追加服務設計
    """)

st.markdown("---")

# ===== 區塊：顧問能獲得什麼？ =====
st.markdown("### 顧問夥伴能具體獲得什麼？")
g1, g2 = st.columns(2)
with g1:
    st.markdown("""
    **✨ 業務面**  
    - 更可視的交付成果（不是報表，而是「可執行藍圖」）  
    - 更高的成案率與續約率（以結果與里程碑為中心）  
    - 正式對外共同品牌露出（案例／白皮書共創）
    """)
with g2:
    st.markdown("""
    **🛠️ 作業面**  
    - 客製化模組：診斷問卷、試算、報告模板  
    - 安全協作：與客戶/律師/會計師在同一空間協作  
    - 版本管理：任何調整都有記錄、可追溯
    """)

st.markdown("---")

# ===== 區塊：適合對象 =====
st.markdown("### 適合的顧問夥伴")
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("**家族辦公室 / 私行顧問**  \n需要長期、精準、可視化的交付與複盤節奏。")
with c2:
    st.markdown("**律師 / 會計師 / 稅顧**  \n希望把專業輸出轉為「可執行工作包」，提升溝通效率。")
with c3:
    st.markdown("**保險與資產顧問**  \n要以整體藍圖帶出合理配置，建立策略性與專屬性。")

st.markdown("---")

# ===== CTA =====
st.markdown("### 準備好把你的專業放大了嗎？")
cta_col, _ = st.columns([2,1])
with cta_col:
    st.page_link("pages/4_contact.py", label="🤝 申請合作／洽談細節")
    st.caption("留下聯絡資訊與簡要背景，我們將安排顧問經理與你對接。")

# ===== FAQ =====
st.markdown("---")
st.markdown("### 常見問題（FAQ）")
with st.expander("Q1. 你們會與我原有的合作夥伴（律師、會計師）衝突嗎？"):
    st.write("不會。我們扮演的是「藍圖與節點的總管家」，協助整合各方專業，讓落地更順暢。")
with st.expander("Q2. 是否需要學很複雜的新工具？"):
    st.write("不需要。我們提供入門清單、短訓與範本；你先用既有方法工作，逐步導入模組即可。")
with st.expander("Q3. 顧問收益如何計算？"):
    st.write("依據專案型與長期顧問型的不同，我們會提供透明的收益分潤與續約設計。細節於一對一洽談說明。")
with st.expander("Q4. 客戶資料的安全性？"):
    st.write("採最小化資料原則與權限管理；依需求可提供獨立伺服器與加密儲存。")

# ===== Footer =====
render_footer()
