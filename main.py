import telebot
import requests
import sqlite3
import os
from datetime import datetime
from telebot import types

# ==============================
# الإعدادات - Settings
# ==============================
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"  # ضع توكن البوت هنا  
ADMIN_ID = 0000000 # YOUR ID  
CHANNEL_ID = "@python_1I" 
bot = telebot.TeleBot(TOKEN)

BASE_URL = "https://api.chess.com/pub/player"
HEADERS = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}

# ==============================
# Database Logic (إصلاح تلقائي للأعمدة)
# ==============================
def init_db():
    conn = sqlite3.connect('chess_bot.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY)''')
    
    # التحقق من وجود الأعمدة وإضافتها إذا نقصت
    c.execute("PRAGMA table_info(users)")
    cols = [column[1] for column in c.fetchall()]
    if 'username' not in cols:
        c.execute("ALTER TABLE users ADD COLUMN username TEXT")
    if 'full_name' not in cols:
        c.execute("ALTER TABLE users ADD COLUMN full_name TEXT")
    
    conn.commit()
    conn.close()

def add_user(user_id, username, full_name):
    conn = sqlite3.connect('chess_bot.db')
    c = conn.cursor()
    c.execute("""INSERT OR REPLACE INTO users (user_id, username, full_name) 
                 VALUES (?, ?, ?)""", (user_id, username, full_name))
    conn.commit()
    conn.close()

def get_all_users_details():
    conn = sqlite3.connect('chess_bot.db')
    c = conn.cursor()
    c.execute("SELECT user_id, username, full_name FROM users")
    users = c.fetchall()
    conn.close()
    return users

init_db()
user_lang = {}

# ==============================
# Helpers
# ==============================
def is_subscribed(user_id):
    if user_id == ADMIN_ID: return True
    try:
        status = bot.get_chat_member(CHANNEL_ID, user_id).status
        return status in ['member', 'administrator', 'creator']
    except: return False

def clean_username(text: str) -> str:
    return text.strip().split("/")[-1].lower()

def fetch_player_data(username: str):
    try:
        p_res = requests.get(f"{BASE_URL}/{username}", headers=HEADERS, timeout=10)
        if p_res.status_code != 200: return None
        s_res = requests.get(f"{BASE_URL}/{username}/stats", headers=HEADERS, timeout=10)
        return {
            "profile": p_res.json(),
            "stats": s_res.json(),
            "username": username
        }
    except: return None

def format_all_stats(data, lang="ar"):
    s = data["stats"]
    u = data["username"].upper()
    
    # الترجمة
    txt = {
        "en": ["Rating", "Best", "Win", "Loss", "Draw", "Total Games"],
        "ar": ["التقييم", "أفضل تقييم", "فوز", "خسارة", "تعادل", "إجمالي المباريات"]
    }[lang]

    res = [f"♟ *PLAYER:* `{u}`", "━━━━━━━━━━━━━━"]

    # الفئات التي سنستخرج إحصائياتها
    cats = {
        "chess_blitz": "⚡ Blitz | بلايتز",
        "chess_rapid": "🕒 Rapid | رابيد",
        "chess_bullet": "🔫 Bullet | بوليت"
    }

    for key, label in cats.items():
        if key in s:
            item = s[key]
            last = item.get('last', {}).get('rating', 'N/A')
            best = item.get('best', {}).get('rating', 'N/A')
            record = item.get('record', {})
            w, l, d = record.get('win', 0), record.get('loss', 0), record.get('draw', 0)
            total = w + l + d
            
            res.append(f"*{label}*")
            res.append(f"├ {txt[0]}: `{last}`")
            res.append(f"├ {txt[1]}: `{best}`")
            res.append(f"└ {txt[2]}: `{w}` | {txt[3]}: `{l}` | {txt[4]}: `{d}`")
            res.append(f"  ({txt[5]}: `{total}`)\n")
    
    # إضافة إحصائيات الألغاز (Puzzles)
    if "tactics" in s:
        puz = s["tactics"].get("highest", {}).get("rating", "N/A")
        res.append(f"🧩 *Puzzles:* `{puz}`")

    return "\n".join(res)

# ==============================
# Handlers
# ==============================

@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.from_user.id != ADMIN_ID: return
    users = get_all_users_details()
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("إذاعة 📢", callback_data="broadcast"))
    markup.add(types.InlineKeyboardButton("قائمة المستخدمين 📄", callback_data="export_users"))
    bot.send_message(message.chat.id, f"🛠 *لوحة التحكم*\nالمستخدمين: `{len(users)}`", parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def queries(call):
    if call.data == "export_users":
        users = get_all_users_details()
        with open("users.txt", "w", encoding="utf-8") as f:
            for u_id, u_name, f_name in users:
                f.write(f"ID: {u_id} | @{u_name} | {f_name}\n")
        bot.send_document(call.message.chat.id, open("users.txt", "rb"))
        os.remove("users.txt")
    elif call.data == "broadcast":
        msg = bot.send_message(call.message.chat.id, "أرسل رسالة الإذاعة:")
        bot.register_next_step_handler(msg, lambda m: [bot.send_message(u[0], m.text) for u in get_all_users_details()])
    elif call.data == "check_sub":
        if is_subscribed(call.from_user.id):
            bot.delete_message(call.message.chat.id, call.message.message_id)
            start(call.message)

@bot.message_handler(commands=['start'])
def start(message):
    add_user(message.chat.id, message.from_user.username, message.from_user.first_name)
    if not is_subscribed(message.chat.id):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("انضم للقناة 📢", url=f"https://t.me/{CHANNEL_ID[1:]}"))
        markup.add(types.InlineKeyboardButton("تأكيد الاشتراك ✅", callback_data="check_sub"))
        bot.send_message(message.chat.id, "⚠️ اشترك بالقناة أولاً لاستخدام البوت.", reply_markup=markup)
        return
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("English 🇺🇸", "العربية 🇸🇦")
    bot.send_message(message.chat.id, "👋 اختر لغتك:", reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def handle(message):
    if not is_subscribed(message.chat.id): return
    if message.text in ["English 🇺🇸", "العربية 🇸🇦"]:
        user_lang[message.chat.id] = "en" if "English" in message.text else "ar"
        bot.reply_to(message, "✅ أرسل اليوزرنيم الآن:")
        return

    lang = user_lang.get(message.chat.id, "ar")
    data = fetch_player_data(clean_username(message.text))
    if not data:
        bot.reply_to(message, "❌ المستخدم غير موجود.")
        return

    caption = format_all_stats(data, lang)
    avatar = data["profile"].get("avatar")
    
    if avatar:
        bot.send_photo(message.chat.id, avatar, caption=caption, parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id, caption, parse_mode="Markdown")

print("Bot is running...")
bot.infinity_polling()