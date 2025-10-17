# -*- coding: utf-8 -*-
import streamlit as st
from ui_shared import ensure_page_config, render_header, render_footer

# ---------------- 基本設定 ----------------
ensure_page_config(title="傳承初診摘要報告｜永傳家族辦公室")
render_header()

st.subheader("📋 傳承初診摘要報告")
st.caption("以下為依您的作答所生成的初步分析。本報告僅供參考，正式規劃仍需由專業顧問深度審視。")

# 從 Session State 讀取初診資料（由 9_risk_check.py 寫入）
data = st.session_state.get("risk_data")

if not data:
    st.warning("請先前往「傳承風險初診」完成填寫，再回到此頁查看報告。")
else:
    # ---------------- 計分模型：準備度 - 複雜度 ----------------
    # 複雜度（complexity）：資產規模 & 跨境程度 → 分數越高代表越複雜、越具潛在風險
    complexity = 0
    # 資產規模：越大越複雜（0~2）
    if data["a1"] in ["2–5 億", "5 億以上"]:
        complexity += 2
    # 國際複雜度：多國 > 單一國家 > 無（0~2）
    if data["a2"] == "多個國家":
        complexity += 2
    elif data["a2"] == "單一國家":
        complexity += 1

    # 準備度（readiness）：治理/架構成熟 + 家族共識成熟 → 分數越高代表越安全
    m_map = {"尚未規劃": 0, "僅遺囑": 1, "保險信託": 2, "家族信託/閉鎖性公司": 3}
    c_map = {"尚未開始": 0, "有對話": 1, "已有憲章/明確接班": 2}

    m_score = m_map.get(data["a3"], 0) * 2  # 架構權重較高（0~6）
    c_score = c_map.get(data["a4"], 0) * 1  # 共識權重（0~2）
    readiness = m_score + c_score          # 準備度總分（0~8）

    # 最終安全分（越高越安全）：準備度 - 複雜度（範圍 0~8）
    score_raw = readiness - complexity
    score = max(0, min(8, score_raw))

    # ---------------- 風險分級（越高分越安全） ----------------
    if score >= 6:
        risk_level = "低風險（✅ 綠燈區）"
        advice = (
            "做得很好！您的治理與家族共識具備一定基礎，建議持續每年複盤，"
            "並在法規或家族/企業重大事件發生時，滾動微調藍圖。"
        )
        style = "success"
        bg, bd, fg = "#ecfdf5", "#10b981", "#10b981"
    elif score >= 3:
        risk_level = "中風險（⚠️ 黃燈區）"
        advice = (
            "您已有起步，但仍存在可補強的關鍵環節（如信託細節、接班權責、股權現金流配置）。"
            "建議安排顧問針對缺口做結構化優化，以免外部變動時承受不必要的風險。"
        )
        style = "info"
        bg, bd, fg = "#fffbeb", "#f59e0b", "#b45309"
    else:
        risk_level = "高風險（🚨 紅燈區）"
        advice = (
            "目前複雜度相對高或治理成熟度不足。建議盡快安排深度諮詢，"
            "優先處理跨境/凍結風險、遺贈稅暴露與家族共識建立，先搭好基本防護。"
        )
        style = "error"
        bg, bd, fg = "#fee2e2", "#ef4444", "#b91c1c"

    # ---------------- 您的作答摘要 ----------------
    st.markdown("---")
    st.markdown("### 您的現況盤點")

    st.markdown(
        f"""
| 項目 | 您的回答 |
| :--- | :--- |
| 總資產級距 | **{data['a1']}** |
| 海外資產配置 | **{data['a2']}** |
| 法律/信託架構程度 | **{data['a3']}** |
| 家族共識程度 | **{data['a4']}** |
""")

    # ---------------- 分數拆解顯示 ----------------
    st.markdown(
        f"""
<div style="
  display:flex; gap:12px; flex-wrap:wrap; margin: 8px 0 4px 0;">
  <div style="padding:8px 12px; border:1px solid #e5e7eb; border-radius:10px;">
    複雜度 <strong>{complexity}</strong>（資產/跨境）
  </div>
  <div style="padding:8px 12px; border:1px solid #e5e7eb; border-radius:10px;">
    準備度 <strong>{readiness}</strong>（治理/共識）
  </div>
  <div style="padding:8px 12px; border:1px solid #e5e7eb; border-radius:10px;">
    安全分 <strong>{score}</strong>（上限 8）
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    # ---------------- 診斷結果區塊 ----------------
    st.markdown("---")
    st.markdown("### 診斷結果：傳承風險等級")

    st.markdown(
        f"""
<div style='
  padding: 20px;
  border-radius: 12px;
  background-color: {bg};
  border: 2px solid {bd};
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
  margin-bottom: 20px;'>
  <div style='font-size: 24px; font-weight: 800; color: {fg};'>
    {risk_level}（安全分：{score}）
  </div>
  <div style='font-size:16px; margin-top:10px; line-height:1.7; color:#333;'>
    {advice}
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    # ---------------- 下一步建議 ----------------
    st.markdown("---")
    st.markdown("### 永傳建議的下一步")
    st.markdown(
        """
透過「專家洞見 × 智能科技」，我們將協助您建立一份**可落地、可持續**的傳承藍圖：
1. **視覺化全貌**：彙整資產、股權與家族關係，形成一張清晰的**傳承地圖**。  
2. **情境模擬**：對贈與、信託、保單等方案進行**稅負與現金流**量化比較。  
3. **文件審閱**：由國際律師、會計師與顧問團隊協作，確保合規且有效。  
"""
    )

    st.markdown("<div style='margin-top:24px; text-align:center;'>", unsafe_allow_html=True)
    st.page_link("pages/4_contact.py", label="✉️ 預約專屬顧問深度諮詢", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

render_footer()
