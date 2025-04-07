import streamlit as st

# 翻譯字典
TRANSLATIONS = {
    "zh-TW": {
        "impact_title": "影響力",
        "impact_subtitle": "高資產家庭的傳承策略平台",
        "impact_tagline": "讓每一分資源，都成為你影響力的延伸",
        "choose_user_type": "請選擇您的身份",
        "for_advisors": "顧問入口",
        "for_clients": "客戶入口",
        "platform_footer": "傳承策略平台",
    },
    "en": {
        "impact_title": "Legacy Impact",
        "impact_subtitle": "A Strategic Legacy Platform for Affluent Families",
        "impact_tagline": "Turn every resource into an extension of your impact",
        "choose_user_type": "Choose your role",
        "for_advisors": "Advisor Portal",
        "for_clients": "Client Portal",
        "platform_footer": "Legacy Strategy Platform",
    },
    "zh-CN": {
        "impact_title": "影响力",
        "impact_subtitle": "高净值家庭的传承策略平台",
        "impact_tagline": "让每一分钱，都成为你影响力的延伸",
        "choose_user_type": "请选择您的身份",
        "for_advisors": "顾问入口",
        "for_clients": "客户入口",
        "platform_footer": "传承策略平台",
    }
}

# 設定語言
def set_language():
    if "app_language" not in st.session_state:
        st.session_state.app_language = "zh-TW"

    lang = st.sidebar.selectbox(
        "🌐 語言 / Language / 语言",
        options=["繁體中文", "English", "简体中文"],
        index=["繁體中文", "English", "简体中文"].index(get_lang_name(st.session_state.app_language))
    )

    lang_code = {
        "繁體中文": "zh-TW",
        "English": "en",
        "简体中文": "zh-CN"
    }[lang]

    if st.session_state.app_language != lang_code:
        st.session_state.app_language = lang_code
        st.rerun()

def get_text(key):
    lang = st.session_state.get("app_language", "zh-TW")
    return TRANSLATIONS.get(lang, TRANSLATIONS["zh-TW"]).get(key, key)

def get_lang_name(code):
    return {
        "zh-TW": "繁體中文",
        "en": "English",
        "zh-CN": "简体中文"
    }.get(code, "繁體中文")
