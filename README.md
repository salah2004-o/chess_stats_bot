# ♟️ Chess Stats Bot | بوت إحصائيات الشطرنج

> **Real-time Chess Statistics Tracker for Telegram**  
> **متابع إحصائيات الشطرنج في الوقت الفعلي على تيليجرام**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![API](https://img.shields.io/badge/API-Chess.com-black)](https://www.chess.com)

---

<div dir="ltr">

## 🌟 Features

- 📊 **Live Chess.com Statistics** - Get real-time player stats from Chess.com
- 🏆 **Rating Tracking** - Monitor Blitz, Rapid, and Classical ratings
- 📈 **Performance Metrics** - Win rate, draw rate, loss rate analysis
- 🎯 **Player Search** - Search and compare players
- 📋 **Leaderboard** - Top players ranking
- 🔄 **Auto-Update** - Periodic statistics refresh

---

## 🛠️ Requirements

- Python 3.8+
- Telegram Bot Token
- Internet connection (for Chess.com API)

### Dependencies
```
pyTelegramBotAPI >= 4.0
requests >= 2.28.0
matplotlib >= 3.5.0
```

---

## 📦 Installation

```bash
git clone https://github.com/your-username/chess-stats-bot.git
cd chess-stats-bot

python -m venv venv
venv\Scripts\activate  # Windows

pip install -r requirements.txt

cp .env.example .env
# Edit TOKEN and ADMIN_ID
```

---

## 🚀 Usage

```bash
python main.py
```

---

## 🎮 Commands

| Command | Description |
|---------|-------------|
| `/start` | Start the bot |
| `/stats <username>` | Get player stats |
| `/compare <user1> <user2>` | Compare players |
| `/top` | Top 10 players |
| `/help` | Show help |

---

## 📊 Project Structure

```
chess_stats_bot/
├── main.py
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🐳 Docker

```bash
docker build -t chess-stats-bot .
docker run -d -e TOKEN=your_token chess-stats-bot
```

---

## 📝 License

MIT License

</div>

---

<div dir="rtl">

## 🌟 الميزات

- 📊 **إحصائيات مباشرة من Chess.com** - احصل على إحصائيات اللاعبين في الوقت الفعلي
- 🏆 **تتبع التصنيف** - راقب تصنيفات Blitz و Rapid و Classical
- 📈 **مقاييس الأداء** - تحليل نسبة الفوز والتعادل والخسارة
- 🎯 **بحث عن اللاعبين** - ابحث وقارن بين اللاعبين
- 📋 **لوحة الترتيب** - تصنيف أفضل اللاعبين
- 🔄 **التحديث التلقائي** - تحديث دوري للإحصائيات

---

## 🛠️ المتطلبات

- Python 3.8+
- Telegram Bot Token
- اتصال إنترنت (لـ Chess.com API)

### المكتبات المطلوبة
```
pyTelegramBotAPI >= 4.0
requests >= 2.28.0
matplotlib >= 3.5.0
```

---

## 📦 التثبيت

```bash
git clone https://github.com/your-username/chess-stats-bot.git
cd chess-stats-bot

python -m venv venv
venv\Scripts\activate  # Windows

pip install -r requirements.txt

cp .env.example .env
# عدّل TOKEN و ADMIN_ID
```

---

## 🚀 الاستخدام

```bash
python main.py
```

---

## 🎮 الأوامر

| الأمر | الوصف |
|------|-------|
| `/start` | بدء البوت |
| `/stats <username>` | إحصائيات اللاعب |
| `/compare <user1> <user2>` | مقارنة لاعبين |
| `/top` | أفضل 10 لاعبين |
| `/help` | المساعدة |

---

## 🗂️ هيكل المشروع

```
chess_stats_bot/
├── main.py
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🐳 Docker

```bash
docker build -t chess-stats-bot .
docker run -d -e TOKEN=your_token chess-stats-bot
```

---

## 📝 الترخيص

MIT License

</div>

---

**Last Updated**: 2026-09-01
