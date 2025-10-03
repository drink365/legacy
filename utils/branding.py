# utils/branding.py
APP_TITLE = "《影響力》傳承策略平台"
APP_KICKER = "INFLUENCE LEGACY PLATFORM"
APP_TAGLINE = "AI 驅動的傳承策略平台｜財務 × 稅務 × 保險 × 對話設計"
FOOTER = "《影響力》傳承策略平台｜永傳家族傳承導師"
LOGO_PATH = "assets/logo.png"

HIDE_DEFAULT_UI = '''
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .block-container {padding-top: 2rem; padding-bottom: 3rem;}
        .hero h1 {font-size: 3rem; line-height: 1.15; margin: 0 0 0.6rem 0;}
        .hero p.lead {font-size: 1.35rem; opacity: 0.95; margin: 0.2rem 0 0.8rem 0;}
        .pill {display:inline-block; padding: 6px 12px; border-radius: 999px; border:1px solid #eaeaea; font-size:0.9rem; margin-right:8px}
        .kicker {letter-spacing:.08em; text-transform:uppercase; font-weight:700; font-size:.85rem; opacity:.8}
        .section-title {font-size:1.25rem; margin: 0 0 .6rem 0; font-weight:700}
        .value-card {padding:18px;border:1px solid #eee;border-radius:16px;box-shadow:0 2px 10px rgba(0,0,0,.03);}
        .muted {opacity:.9}
        .cta {font-size:1.05rem}
        .topbar {display:flex; align-items:center; gap:.6rem; justify-content:flex-end}
        .topbar .name {font-weight:600}
        .topbar .expiry {opacity:.8; font-size:.9rem}
    </style>
'''

BRAND_COLORS = '''
    <style>
      :root {
          --brand-red: #C8102E;
          --brand-gold: #B68B2C;
          --brand-dark: #3A3A3A;
      }
      .stButton>button {
          background-color: var(--brand-red);
          color: #fff;
          border-radius: 10px;
          border: none;
          padding: 0.65rem 1.2rem;
          font-weight: 700;
      }
      .stButton>button:hover { background-color: var(--brand-gold); color:#fff; }
      h1, h2, h3, h4 { color: var(--brand-dark); }
      .value-card { border-color: rgba(200,16,46,.15); }
      .pill { border-color: rgba(182,139,44,.4); }
    </style>
'''
