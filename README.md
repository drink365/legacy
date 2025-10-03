# 《影響力》傳承策略平台（展示版）

- Home：TED 風首頁（定位清楚｜三大成果｜CTA）
- Login：側邊登入，登入後右上角顯示 😀 使用者與有效期限
- Pages：
  - `pages/1_insurance_planner.py` 保單策略模擬器（含 PDF 匯出）
  - `pages/2_estate_tax.py` 遺產稅試算與壓縮（示意）
  - `pages/3_advisor_plan.py` 顧問專用方案（商業模式建議）

## 部署
1. 將專案上傳至 GitHub（包含本目錄所有檔案）。
2. 若使用 Streamlit Cloud，新增本 repo 即可自動部署。
3. 如需 PDF 匯出為真正 PDF，請確保 `requirements.txt` 中的 `reportlab` 已安裝成功。

## 調整授權名單
在 `utils/auth.py` 中調整 `AUTHORIZED_USERS` 帳號、密碼與有效日期。
