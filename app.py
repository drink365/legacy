# app.py — 永傳家族辦公室｜首頁 v4.4J
# -*- coding: utf-8 -*-

import base64
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components
from ui_shared import ensure_page_config, render_header, render_footer

def _img_b64(src_path: str | Path) -> str | None:
    p = Path(src_path)
    try:
        if p.exists():
            return base64.b64encode(p.read_bytes()).decode("utf-8")
    except Exception as e:
        print(f"⚠️ 圖片讀取失敗：{p} ({e})")
    return None

# 1) 頁面設定與導覽
ensure_page_config(page_title="永傳家族辦公室｜與您攜手，擘劃永續傳承")
render_header(logo_width_px=180, show_tagline=False)

# 放大版副標語（24px）
st.markdown("<div class='subtitle-tagline'>專家洞見 × 智能科技 × 幸福傳承</div>", unsafe_allow_html=True)

# 2) 本頁專屬樣式（避免覆寫 .stPageLink；僅做內容區塊排版）
st.markdown("""
<style>
  :root{ --brand-navy:#091931; --brand-accent:#00A896; --brand-light:#F4F9FF; --ink:#111827; --muted:#4b5563; --card:#ffffff; --border:#e2e8f0; }
  .yc-wrap{ padding:8px 0 32px 0; }

  .yc-hero{ position:relative; background:var(--brand-navy); border-radius:12px; padding:60px 24px 50px; text-align:center; box-shadow:0 10px 30px rgba(9,25,49,.25); }
  .kicker{ display:inline-block; font-size:14px; padding:7px 14px; border-radius:4px; background:var(--brand-accent); color:#fff; font-weight:700; letter-spacing:.5px; margin-bottom:12px; }
  .yc-hero h1{ font-size:52px; line-height:1.15; margin:0 0 12px 0; color:#fff; font-weight:700; }
  .yc-hero p.sub{ font-size:20px; color:rgba(255,255,255,0.88); max-width:960px; margin:0 auto 20px; }

  .grid-3{ display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:24px; }
  .card{ background:var(--card); border:1px solid var(--border); border-radius:8px; padding:24px; box-shadow:0 2px 8px rgba(0,0,0,.04); transition:transform .2s, box-shadow .2s, border-color .2s; }
  .card:hover{ transform:translateY(-3px); box-shadow:0 8px 18px rgba(0,0,0,.08); border-color:#cbd5e1; }
  .card h4{ margin:0 0 10px; color:var(--brand-navy); font-size:20px; font-weight:700; }
  .card p{ margin:0; color:var(--muted); font-size:15px; line-height:1.7; }

  .yc-steps{ counter-reset: step; }
  .yc-step{ background:#fff; border:1px solid var(--border); border-radius:8px; padding:22px; position:relative; }
  .yc-step:before{ counter-increment: step; content: counter(step); position:absolute; left:22px; top:0; width:40px; height:40px; display:flex; align-items:center; justify-content:center; background: var(--brand-accent); color:#fff; border-radius:6px; font-weight:700; box-shadow:0 4px 12px rgba(0,168,150,.20); transform:translateY(-50%); font-size:20px; }
  .yc-step h4{ margin-top:20px; }

  .mentor-card{ display:grid; grid-template-columns:140px 1fr; align-items:center; gap:24px; background:#fff; border:1px solid var(--border); border-radius:12px; padding:24px; box-shadow:0 6px 16px rgba(0,0,0,.05); }
  .mentor-avatar{ width:140px; height:140px; border-radius:50%; object-fit:cover; border:4px solid #E5E7EB !important; box-shadow:0 4px 10px rgba(0,0,0,0.08); }
  .mentor-card h4{ margin:0 0 6px; font-size:24px; color:var(--brand-navy); font-weight:700; }
  .mentor-title{ font-size:16px; color:var(--brand-accent); font-weight:700; margin-bottom:10px; }
  .mentor-card p{ margin:0; font-size:16px; color:#374151; line-height:1.8; }

  .section{ margin:48px 0 16px; }
  .section h3{ font-size:36px; color:var(--brand-navy); margin:0 0 24px 0; text-align:center; font-weight:700; }

  /* Metrics：桌機四格；手機橫向滑動（不影響按鈕樣式） */
  .metrics-wrap{ margin-top:0; }
  .metrics-grid{ display:grid; grid-template-columns:repeat(4,minmax(180px,1fr)); gap:24px; }
  .metrics-item{ text-align:center; background:#fff; border:1px solid var(--border); border-radius:8px; padding:20px; }
  .metrics-item .big{ font-size:32px; font-weight:700; color:var(--brand-navy); }
  .metrics-item .sub{ font-size:14px; color:var(--muted); }
  @media (max-width: 768px){
    .metrics-grid{ display:flex; gap:16px; overflow-x:auto; padding-bottom:8px; -webkit-overflow-scrolling:touch; scroll-snap-type:x proximity; }
    .metrics-item{ min-width:220px; flex:0 0 auto; scroll-snap-align:start; }
    .yc-hero h1{ font-size:42px; }
    .mentor-card{ grid-template-columns:1fr; text-align:center; }
  }
</style>
""", unsafe_allow_html=True)

# 3) Hero
st.markdown("""
<div class="yc-wrap">
  <section class="yc-hero">
    <div class="kicker">擘劃家族永續願景，從容掌控未來</div>
    <h1>永傳世代的財富與智慧</h1>
    <p class="sub">
      讓未來更清晰、更可控——永傳家族辦公室，以跨領域的精準專業，將家族的財富、事業、精神，
      轉化為一張清晰、可執行的「永續傳承藍圖」。
    </p>
  </section>
</div>
""", unsafe_allow_html=True)

# 中段 CTA（字寬、僅文字範圍淡底；樣式取自 ui_shared.py 的 .stPageLink）
cta_col1, cta_col2, _ = st.columns([1,1,2])
with cta_col1:
    st.page_link("pages/4_contact.py", label="🤝 啟動您的專屬傳承規劃")  # 不帶 use_container_width
with cta_col2:
    st.page_link("pages/blueprint.py", label="💎 了解永續傳承藍圖")      # 不帶 use_container_width

# 4) Metrics（手機可橫滑；第一格文字已調整）
st.markdown("""
<div class="yc-wrap metrics-wrap">
  <div class="metrics-grid">
    <div class="metrics-item"><div class="big">30+年</div><div class="sub">財稅 × 企業經營 × 投資實戰經驗</div></div>
    <div class="metrics-item"><div class="big">公益影響</div><div class="sub">發起「百場公益演講」行動</div></div>
    <div class="metrics-item"><div class="big">頂尖團隊</div><div class="sub">會計師、律師、財稅顧問專業聯合</div></div>
    <div class="metrics-item"><div class="big">高落地率</div><div class="sub">方案執行成效穩定、落實到位</div></div>
  </div>
</div>
""", unsafe_allow_html=True)

# 5) 首席傳承顧問（版本 C：溫暖故事版，含「勞動部、經濟部」）
grace_b64 = _img_b64(Path(__file__).parent / "assets" / "grace_huang.jpg")
grace_img = (f'data:image/jpeg;base64,{grace_b64}' if grace_b64 else "https://via.placeholder.com/150x150.png?text=Grace")
st.markdown(f"""
<div class="section">
  <h3>您的首席傳承顧問</h3>
  <div class="mentor-card">
    <img class="mentor-avatar" src="{grace_img}" alt="黃榮如 Grace Huang">
    <div>
      <h4>黃榮如 Grace Huang</h4>
      <div class="mentor-title">家族傳承策略導師｜永傳家族辦公室 創辦人</div>
      <p>
        美國海歸碩士、美國會計師執照（CPA）。曾任投資銀行主管、上市公司高管與創業投資者，
        2019 年創立永傳家族辦公室，整合會計師、律師與財稅顧問，
        為高資產家族設計跨世代的永續傳承藍圖。
        她也將多年經驗化為行動，受邀於勞動部、經濟部與多家金融機構及社團授課，
        並於 2025 年發起「百場公益演講」行動，推動財商教育與幸福傳承理念。
      </p>
      <small style="color:#4b5563;font-size:13px;margin-top:6px;display:block;">
        專長：跨境財稅規劃、家族憲章與股權傳承、超大額保單配置、家族現金流模型
      </small>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# 6) 三大核心價值
st.markdown("""<div class="section"><h3>從複雜到清晰：您將獲得的確定性</h3></div>""", unsafe_allow_html=True)
st.markdown("""
<div class="grid-3">
  <div class="card"><h4>決策優化，告別資訊焦慮</h4>
    <p><b>精準聚焦：</b>將龐雜的財稅、法律資訊，濃縮為決策者只需關注的 20% 核心重點。</p></div>
  <div class="card"><h4>家族共識，確保目標一致</h4>
    <p><b>行動藍圖：</b>提供一張所有人都理解的「永續傳承藍圖」，加速溝通、實現高效決策。</p></div>
  <div class="card"><h4>結構穩固，排除隱藏風險</h4>
    <p><b>立即執行：</b>優先處理核心資產的金流與股權結構，確保關鍵節點滴水不漏。</p></div>
</div>
""", unsafe_allow_html=True)

# 7) 三步旅程
st.markdown("""<div class="section"><h3>您的傳承啟程：我們承諾的三個步驟</h3></div>""", unsafe_allow_html=True)
st.markdown("""
<div class="grid-3 yc-steps">
  <div class="yc-step"><h4>① 高階盤點：精準鎖定核心議題</h4>
    <p>透過結構化對話，快速識別家族財富、企業股權與繼承意願的關鍵痛點，形成專業初診報告。</p></div>
  <div class="yc-step"><h4>② 藍圖架構：整合多方專業資源</h4>
    <p>整合法務、會計與財策資源，架構信託、保險、稅務最佳方案，轉化為行動清單。</p></div>
  <div class="yc-step"><h4>③ 執行到位：確保方案落地有聲</h4>
    <p>全程陪伴文件簽署、金流佈局與家族憲章的實施；每年進行審視與優化，確保永續性。</p></div>
</div>
""", unsafe_allow_html=True)

# 8) 見證
st.markdown("""<div class="section"><h3>真實見證：高資產家族的共同選擇</h3></div>""", unsafe_allow_html=True)
st.markdown("""
<div class="testi-grid">
  <div class="testi"><p>「永傳的價值，在於將我們擔憂的複雜風險，轉化為清晰的法律與稅務架構。這份確定性，無價。」</p><div class="by">— 上市電子業 創辦人 / 王董事長</div></div>
  <div class="testi"><p>「藍圖一出，二代接班的焦慮感瞬間消失。我們從此知道，每一步都是被專業計算過的。」</p><div class="by">— 傳產製造業 二代 / 陳總經理</div></div>
  <div class="testi"><p>「他們是真正的總管家，將我們原有的會計師、律師資源，高效整合，執行力極強。」</p><div class="by">— 不動產投資家族 / 李先生</div></div>
</div>
""", unsafe_allow_html=True)

# 9) Lead Magnet（白皮書｜底部多空一行）
st.markdown("""<div class="section"><h3>從容啟航，把握傳承先機</h3></div>""", unsafe_allow_html=True)
st.markdown("""
<div style="display:flex;flex-direction:column;align-items:center;text-align:center;background:#091931;border:none;border-radius:12px;padding:32px 24px;gap:12px; margin-bottom:32px;">
  <h4 style="margin:0;color:#fff;font-size:26px;font-weight:700;">下載《高資產家族傳承風險評估白皮書》</h4>
  <p style="max-width:800px;color:rgba(255,255,255,0.85);margin:0;font-size:16px;">
    掌握影響未來 30 年的 7 大潛在風險與應對策略，由國際認證顧問團隊專業編撰。
  </p>
</div>
""", unsafe_allow_html=True)

# 文字型 CTA（同樣字寬淡底）
lm_col1, lm_col2, _ = st.columns([1,1,2])
with lm_col1:
    st.page_link("pages/4_contact.py", label="📥 立即領取專業白皮書")
with lm_col2:
    st.page_link("pages/4_contact.py", label="📞 優先預約顧問一對一諮詢")

# 10) FAQ
st.markdown("""<div class="section"><h3>常見問題：您關心的專業細節</h3></div>""", unsafe_allow_html=True)
with st.expander("Q1. 首次諮詢需要準備哪些資料？", expanded=False):
    st.write("您只需帶著您的核心疑問和對家族未來傳承的願景。我們將透過結構化對話，高效鎖定首要目標。")
with st.expander("Q2. 傳承藍圖的執行可行性如何？", expanded=False):
    st.write("我們的藍圖以「執行到位」為核心。它不是理論報告，而是可直接交付專業團隊執行的任務清單。")
with st.expander("Q3. 永傳與我既有的專業團隊如何協作？", expanded=False):
    st.write("永傳扮演「家族總管家」角色，統合律師、會計師與銀行資源，確保規劃與執行在同一戰略下高效運作。")
with st.expander("Q4. 服務收費標準與流程？", expanded=False):
    st.write("我們秉持專業與透明，將在初步盤點後，依議題複雜度提供精準、分階段的報價方案。")

# 頁尾
render_footer()
