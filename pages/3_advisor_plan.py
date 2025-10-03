# pages/3_advisor_plan.py
import streamlit as st

st.set_page_config(page_title="顧問專用方案", page_icon="🧑‍💼", layout="wide")

st.markdown("### 🧑‍💼 顧問專用方案（B2B）")
st.caption("讓顧問從商品銷售，升級為傳承策略導師。")

c1, c2 = st.columns([1.2, 1])
with c1:
    st.markdown("#### 你將獲得")
    st.markdown(
        "- **提案生成器**：輸入條件 → 一鍵產出提案與對比表\n"
        "- **顧問語庫**：情境話術、引導問題、金句模板\n"
        "- **客戶視圖**：資產傳承圖、風險雷達、稅務摘要\n"
        "- **PDF 輸出**：可下載、可列印、可演示\n"
        "- **品牌化**：放上你的名字與聯絡資訊"
    )
    st.markdown("#### 商業模式（建議）")
    st.markdown(
        "- **入門**：免費展示版（限功能｜導入名單）\n"
        "- **專業**：月訂閱，解鎖全模組與PDF\n"
        "- **企業**：團隊授權＋進階模組（API / 隱私空間）"
    )
with c2:
    st.markdown("#### 成交優勢")
    st.success("用策略引導，而非商品堆疊。3 分鐘建立專業信任，30 分鐘收斂可行解。")
    st.markdown("#### 下一步")
    st.info("若需要我協助串接你的商品參數、公司模板與匯出版面，我可以直接幫你整理。")
