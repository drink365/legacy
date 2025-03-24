import streamlit as st
import base64

# 頁面設定
st.set_page_config(
    page_title="永傳 AI 傳承教練｜探索頁",
    page_icon="🌿",
    layout="centered"
)

# LOGO base64 顯示
def load_logo_base64(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

try:
    logo_base64 = load_logo_base64("logo.png")
    st.markdown(f"""
    <div style='text-align: center;'>
        <img src='data:image/png;base64,{logo_base64}' width='180'><br>
        <div style='font-size: 20px; font-weight: bold; margin-top: 0.5em;'>傳承您的影響力</div>
    </div>
    """, unsafe_allow_html=True)
except Exception:
    st.warning("⚠️ 無法載入 logo 圖檔，請確認 logo.png 是否存在。")

# 開場標題
st.markdown("""
<br>
<div style='text-align: center;'>
    <h2 style='font-size: 28px;'>讓您的遠見，為後代鋪出更長的路</h2>
    <p style='font-size: 16px;'>從容放下，是因為已經準備好交棒；<br>我們陪您，一起畫出未來的藍圖。</p>
</div>
<br>
""", unsafe_allow_html=True)

# 開始探索按鈕
if st.button("🌿 開始整理我的傳承藍圖"):
    st.switch_page("app.py")

# 四大特色
st.markdown("""
---

### 🌟 永傳 AI 傳承教練的特色：

- **量身引導**：用溫柔又有架構的對話，陪您釐清真正在意的事。
- **簡單好上手**：無需帳號、無需下載，打開就能開始使用。
- **AI 助力、專業支援**：每一步都有專業團隊與 AI 策略陪跑。
- **下載報告、行動有依據**：完整報告隨時存檔，溝通與規劃更順利。

---
""")

# 流程圖（文字取代）
st.markdown("""
### 👣 探索流程：

1. 了解傳承風格 ➜  
2. 釐清關鍵思考 ➜  
3. 找出未來方向 ➜  
4. 擬定策略建議 ➜  
5. 預約對談 ➜  
6. 實現屬於您的傳承藍圖

---
""")

# 使用者感言（模擬）
st.markdown("""
### 💬 使用者回饋：

> "這段探索讓我第一次認真思考退休的事，也更理解孩子的感受。謝謝這個平台的陪伴。" — 林先生 / 企業主 68歲  
> "我媽媽用完後跟我說，她願意跟我談交棒的事了，我超感動。" — 陳小姐 / 二代經營者  

---
""")

# 聯繫與品牌資訊
st.markdown("""
### 📬 想深入了解？

📌 永傳家族辦公室｜[https://gracefo.com](https://gracefo.com)  
📧 聯絡我們：123@gracefo.com

---
<p style='text-align:center; font-size: 13px;'>Copyright © 永傳家族辦公室</p>
""", unsafe_allow_html=True)
