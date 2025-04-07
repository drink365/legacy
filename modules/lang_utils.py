def get_text(key):
    lang = st.session_state.get("app_language", "zh-TW")
    return TRANSLATIONS.get(lang, TRANSLATIONS["zh-TW"]).get(key, key)

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
    },
}
