# -*- coding: utf-8 -*-
from __future__ import annotations

import streamlit as st
import pandas as pd
import json
import sys, os
from typing import TypedDict, List, Literal

# 確保可以導入 ui_shared (假設文件結構正確)
try:
    ROOT = os.path.dirname(os.path.dirname(__file__))
    if ROOT not in sys.path:
        sys.path.insert(0, ROOT)
    from ui_shared import ensure_page_config, render_header, render_footer, load_collection, save_doc, get_user_id
except ImportError:
    # Fallback for local testing or if ui_shared is unavailable
    def ensure_page_config(*args, **kwargs): pass
    def render_header(*args, **kwargs): pass
    def render_footer(*args, **kwargs): pass
    def load_collection(name): return pd.DataFrame()
    def save_doc(name, data, doc_id=None): return True
    def get_user_id(): return 'mock_user_id'
    
ensure_page_config('7 asset map')
render_header()

# --- 類型定義 ---
class AssetInput(TypedDict):
    category: Literal["家業股權", "不動產", "流動資產", "保險價值", "其他"]
    description: str
    value: int # 單位：萬 (TWD)

# --- 常數/工具函數 ---
ASSET_COLLECTION = "asset_map_data"
BASE_UNIT = 10000 # 預設輸入單位為「萬」
CATEGORY_COLORS = {
    "家業股權": "#006666",
    "不動產": "#009999",
    "流動資產": "#33CCCC",
    "保險價值": "#FF8C00",
    "其他": "#CCCCCC",
}

def format_value_to_unit(value_in_wan: float, unit_name: str) -> str:
    """將金額從萬轉換為億或百萬並格式化"""
    if value_in_wan >= 10000: # 大於 1 億
        return f"{value_in_wan / 10000:,.2f} 億"
    return f"{value_in_wan:,.0f} 萬"

# --- 狀態與資料載入 ---
user_id = get_user_id()

if 'asset_map' not in st.session_state:
    # 嘗試從 Firestore 載入數據 (Public Data for Simplicity)
    df_data = load_collection(ASSET_COLLECTION)
    if not df_data.empty and user_id in df_data.index:
        try:
            st.session_state['asset_map'] = json.loads(df_data.loc[user_id, 'data_json'])
        except Exception:
            st.session_state['asset_map'] = []
    else:
        # 預設範例資料
        st.session_state['asset_map'] = [
            {"category": "家業股權", "description": "核心事業A持股", "value": 50000},
            {"category": "不動產", "description": "自宅及租賃物業", "value": 30000},
            {"category": "流動資產", "description": "投資組合及現金", "value": 15000},
            {"category": "保險價值", "description": "壽險/年金保單現值", "value": 5000},
        ]

# --- 頁面標題與說明 ---
st.subheader("🗺️ 資產地圖｜家族視覺化")
st.markdown("將家族資產、股權結構視覺化，形成一份清晰的**傳承全貌圖**，這是制定傳承藍圖的第一步。")
st.markdown("此工具讓您快速盤點並觀察資產配置比例（所有金額皆為**新臺幣萬元**為單位）。")

# --- 資產清單編輯器 ---
st.markdown("---")
st.markdown("### 1. 核心資產盤點 (單位：萬)")

assets: List[AssetInput] = st.session_state['asset_map']
if not isinstance(assets, list): # 檢查確保是列表
     assets = []

# 顯示資產清單並允許編輯/刪除
with st.container(border=True):
    st.markdown("#### 目前資產列表")
    col_desc, col_cat, col_val, col_del = st.columns([3, 2, 2, 1])
    
    # Header
    col_desc.markdown("**描述**")
    col_cat.markdown("**分類**")
    col_val.markdown("**價值 (萬)**")
    col_del.markdown("**刪除**")

    new_assets = []
    for i, asset in enumerate(assets):
        c_desc, c_cat, c_val, c_del = st.columns([3, 2, 2, 1])
        
        # 編輯現有項目 (使用 key 確保獨立性)
        asset['description'] = c_desc.text_input("描述", value=asset['description'], label_visibility="collapsed", key=f"desc_{i}")
        asset['category'] = c_cat.selectbox("分類", options=list(CATEGORY_COLORS.keys()), index=list(CATEGORY_COLORS.keys()).index(asset['category']), label_visibility="collapsed", key=f"cat_{i}")
        asset['value'] = c_val.number_input("價值", value=asset['value'], min_value=0, step=100, label_visibility="collapsed", key=f"val_{i}")
        
        # 刪除按鈕
        if c_del.button("🗑️", key=f"del_{i}", use_container_width=True):
            st.toast(f"已移除：{asset['description']}")
        else:
            new_assets.append(asset)
    
    st.session_state['asset_map'] = new_assets

# 新增資產表單
with st.expander("➕ 新增一筆資產"):
    with st.form("add_asset_form", clear_on_submit=True):
        col_new_desc, col_new_cat, col_new_val = st.columns([3, 2, 2])
        new_desc = col_new_desc.text_input("描述 (例：信義區房產 / 活期存款)", placeholder="資產名稱/標的", max_chars=100)
        new_cat = col_new_cat.selectbox("資產分類", options=list(CATEGORY_COLORS.keys()))
        new_val = col_new_val.number_input("價值 (萬)", min_value=1, step=100)
        
        submitted = st.form_submit_button("💾 新增資產", type="primary")
        if submitted:
            if new_desc and new_val:
                st.session_state['asset_map'].append({
                    "category": new_cat,
                    "description": new_desc,
                    "value": new_val,
                })
                st.toast(f"已新增資產：{new_desc}")
                st.rerun()
            else:
                st.error("請填寫資產描述和價值！")


# --- 視覺化與總結 ---
st.markdown("---")
st.markdown("### 2. 資產分配視覺化")

if not st.session_state['asset_map']:
    st.info("請先新增資產以生成資產地圖。")
else:
    # 數據處理
    df_assets = pd.DataFrame(st.session_state['asset_map'])
    
    # 總計資產
    total_value_wan = df_assets['value'].sum()
    total_value_display = format_value_to_unit(total_value_wan, "萬")

    st.metric(
        label="總資產價值 (約)", 
        value=total_value_display, 
        delta=f"總計 {total_value_wan:,.0f} 萬"
    )

    # 分類彙總
    df_grouped = df_assets.groupby('category')['value'].sum().reset_index()
    df_grouped.columns = ['Category', 'Value']
    df_grouped['Percentage'] = (df_grouped['Value'] / total_value_wan) * 100
    
    # 顯示餅圖
    st.markdown("#### 資產類別佔比")
    color_map = {cat: COLOR for cat, COLOR in CATEGORY_COLORS.items() if cat in df_grouped['Category'].tolist()}
    
    st.bar_chart(
        data=df_grouped,
        x='Category',
        y='Value',
        color='Category',
        color_discrete_map=color_map,
        height=300
    )
    
    st.markdown("#### 分類明細")
    df_grouped_display = df_grouped.copy()
    df_grouped_display['Percentage'] = df_grouped_display['Percentage'].map('{:.1f}%'.format)
    df_grouped_display['Value'] = df_grouped_display['Value'].map(lambda x: format_value_to_unit(x, "萬"))
    df_grouped_display.columns = ['資產類別', '總價值', '佔比']
    st.dataframe(df_grouped_display, use_container_width=True, hide_index=True)
    
    # --- 儲存與下一動 ---
    st.markdown("---")
    st.markdown("### 3. 保存地圖數據並下一步")

    # 儲存到 Firestore
    @st.cache_data(show_spinner=False)
    def save_asset_map(assets: List[AssetInput], user_id: str):
        """將資產地圖資料儲存到 Firestore"""
        data_to_save = {
            "user_id": user_id,
            "total_value_wan": total_value_wan,
            "data_json": json.dumps(assets, ensure_ascii=False),
            "timestamp": pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
        }
        return save_doc(ASSET_COLLECTION, data_to_save, doc_id=user_id)

    if st.button("💾 確認並儲存資產地圖", type="primary"):
        save_asset_map(st.session_state['asset_map'], user_id)
        st.success(f"資產地圖已儲存！總資產約為 {total_value_display}。")
        st.page_link("pages/9_risk_check.py", label="下一步：進行傳承風險初診 →", use_container_width=True)

# 頁尾
render_footer()
