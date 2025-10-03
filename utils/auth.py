# utils/auth.py
from datetime import datetime, date
import hashlib
from dataclasses import dataclass

# 簡易授權名單（可替換為外部檔案/Secret）
AUTHORIZED_USERS = {
    "admin": {
        "name": "管理者", "password": "xxx", "role": "admin",
        "start_date": "2025-01-01", "end_date": "2026-12-31"
    },
    "grace": {
        "name": "Grace", "password": "xxx", "role": "vip",
        "start_date": "2025-01-01", "end_date": "2026-12-31"
    },
    "user1": {
        "name": "使用者一", "password": "xxx", "role": "member",
        "start_date": "2025-05-01", "end_date": "2025-10-31"
    }
}

@dataclass
class UserSession:
    username: str
    name: str
    role: str
    start_date: date
    end_date: date

def parse_date(s: str) -> date:
    return datetime.strptime(s, "%Y-%m-%d").date()

def verify_user(username: str, password: str):
    user = AUTHORIZED_USERS.get(username)
    if not user: 
        return None, "查無此用戶"
    if password != user["password"]:
        return None, "密碼錯誤"
    sd = parse_date(user["start_date"]); ed = parse_date(user["end_date"])
    today = datetime.now().date()
    if not (sd <= today <= ed):
        return None, f"帳號已不在有效期間（{sd}～{ed}）"
    session = UserSession(username=username, name=user["name"], role=user["role"], start_date=sd, end_date=ed)
    return session, None

def topbar_html(user: UserSession) -> str:
    return f'''
    <div class="topbar"> 
      <span>😀</span>
      <span class="name">{user.name}</span>
      <span class="expiry">｜有效期限：{user.end_date}</span>
    </div>
    '''
