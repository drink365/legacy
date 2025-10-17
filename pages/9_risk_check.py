# -*- coding: utf-8 -*-
import streamlit as st
# 假設 ui_shared 檔案包含 ensure_page_config, render_header, render_footer, save_doc, get_user_id
from ui_shared import ensure_page_config, render_header, render_footer, save_doc, get_user_id
import pandas as pd

ensure_page_config()
render_header()

st.subheader("✅ 傳承風險初診：您的幸福藍圖起點")
st.caption("這不是冰冷的測驗，而是幫您快速盤點現況的起點。我們只問必要的關鍵題，方便之後的顧問更**精準、溫暖**地與您對話。")

# Mapping for user-friendly display and data IDs
RISK_MAP = {
    "總資產級距*": {"label": "家產規模與複雜度", "options": ["5000 萬以下","5000 萬–2 億","2–5 億","5 億以上"], "id": "a1"},
    "海外資產配置*": {"label": "跨境風險", "options": ["無","單一國家","多個國家"], "id": "a2"},
    "法律/信託架構程度*": {"label": "法律架構成熟度", "options": ["尚未規劃","僅遺囑","保險信託","家族信託/閉鎖性公司"], "id": "a3"},
    "家族共識程度*": {"label": "家風與共識風險", "options": ["尚未開始","有對話","已有憲章/明確接班"], "id": "a4"},
}

with st.form("risk_form"):
    st.markdown("### **聯絡資訊（方便接收報告與顧問聯繫）**")
    c1, c2 = st.columns(2)
    with c1:
        contact_name = st.text_input("您的稱謂（選填）", placeholder="例：黃先生/林小姐")
        contact_email = st.text_input("Email (建議填寫，以便接收報告)", placeholder="example@email.com")
    with c2:
        contact_phone = st.text_input("聯絡電話（選填）", placeholder="09XX-XXX-XXX")
        contact_company = st.text_input("企業/單位名稱（選填）", placeholder="例：永傳科技股份有限公司")

    st.markdown("### **傳承現狀評估**")
    a1 = st.selectbox(RISK_MAP["總資產級距*"]["label"], RISK_MAP["總資產級距*"]["options"])
    a2 = st.selectbox(RISK_MAP["海外資產配置*"]["label"], RISK_MAP["海外資產配置*"]["options"])
    a3 = st.selectbox(RISK_MAP["法律/信託架構程度*"]["label"], RISK_MAP["法律/信託架構程度*"]["options"])
    a4 = st.selectbox(RISK_MAP["家族共識程度*"]["label"], RISK_MAP["家族共識程度*"]["options"])
    
    submit = st.form_submit_button("產生我的初診摘要", type="primary")

if submit:
    # 1. Prepare data for session state and lead storage
    risk_data = {
        "name": contact_name,
        "email": contact_email,
        "phone": contact_phone,
        "company": contact_company,
        "a1": a1,
        "a2": a2,
        "a3": a3,
        "a4": a4,
    }
    
    # 2. Save data as a lead (assuming save_doc utility exists in ui_shared)
    try:
        # Assuming st.session_state.app_id is available
        app_id = st.session_state.get('app_id', 'default_app_id') 
        user_id = get_user_id(st.session_state)
        # Use a timestamped document ID for uniqueness
        doc_id = f"diag_{user_id}_{pd.Timestamp.now().strftime('%Y%m%d%H%M%S')}"
        
        # Save data to public leads collection
        save_doc(
            collection_path=f"artifacts/{app_id}/public/data/lead_assessments",
            doc_id=doc_id,
            data=risk_data,
            is_public=True
        )
        st.session_state["diag_doc_id"] = doc_id # Store doc_id for later reference
        st.success("評估已提交，正在生成專屬報告...")
    except Exception as e:
        # In case Firestore is not fully configured, still allow report generation
        st.warning(f"資料儲存失敗，報告仍可繼續生成。錯誤碼：{e}")

    # 3. Store in session state and switch page
    st.session_state["risk_data"] = risk_data
    st.switch_page("pages/diagnostic_report.py")

render_footer()
