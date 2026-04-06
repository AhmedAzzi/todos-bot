<div align="center">

# ✅ ToDo List Telegram Bot

### Your smart, bilingual task manager — right inside Telegram.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Telegram Bot API](https://img.shields.io/badge/Telegram_Bot_API-latest-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)](https://core.telegram.org/bots/api)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

---

*A feature-rich Telegram bot that helps you capture, organize, and complete your tasks — with full Arabic & English support.*

</div>

<br>

## 🎯 Overview

**ToDo List Bot** is a personal task management bot built for Telegram. It lets you quickly add tasks, attach details, mark them complete, or delete them — all through an intuitive inline keyboard interface. Whether you prefer **العربية** or **English**, the bot adapts to your language seamlessly.

<br>

## ✨ Features

| Feature | Description |
|---|---|
| 📝 **Task Management** | Create, view, complete, and delete tasks with a single tap |
| 📋 **Task Details** | Attach rich notes and details to any task |
| 🌐 **Bilingual Support** | Full Arabic (RTL) and English interface — switch anytime |
| ⌨️ **Inline Keyboards** | Beautiful inline buttons for fast, tap-based interaction |
| 🗂️ **Persistent Storage** | All tasks saved in SQLite — nothing gets lost on restart |
| 👥 **Multi-User** | Each user has their own isolated task list and language preference |
| 🚀 **Deploy-Ready** | Includes `Procfile` for one-click deployment to Heroku / Railway |

<br>

## 🤖 Bot Commands

| Command | Description |
|---|---|
| `/start` | Launch the bot and display the main menu |
| `/add` | Add a new task to your list |
| `/list` | View all your pending tasks |
| `/lang` | Switch between Arabic and English |
| `/help` | Show the help guide |

<br>

## 🛠️ Tech Stack

- **Language:** Python 3.10+
- **Framework:** [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) (async)
- **Database:** SQLite3 (zero-config, file-based)
- **Deployment:** Heroku / Railway via `Procfile`

<br>

## 🚀 Getting Started

### Prerequisites

- Python **3.10** or higher
- A Telegram Bot Token from [@BotFather](https://t.me/BotFather)

### 1. Clone the repository

```bash
git clone https://github.com/AhmedAzzi/todos-bot.git
cd todos-bot
```

### 2. Create & activate a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your bot token

Open `main.py` and replace the token string in the `main()` function with your own bot token:

```python
application = Application.builder().token('YOUR_BOT_TOKEN_HERE').build()
```

> [!TIP]
> For better security, use an environment variable instead of hardcoding the token:
> ```python
> import os
> application = Application.builder().token(os.getenv('BOT_TOKEN')).build()
> ```

### 5. Run the bot

```bash
python main.py
```

The bot will start polling for updates. Open Telegram, search for your bot, and send `/start`!

<br>

## 📁 Project Structure

```
todos-bot/
├── main.py              # Bot logic, handlers, and database operations
├── requirements.txt     # Python dependencies
├── Procfile             # Deployment configuration (Heroku / Railway)
├── todo.db              # SQLite database (auto-created on first run)
├── .gitignore           # Git ignore rules
└── README.md            # You are here!
```

<br>

## ☁️ Deployment

### Heroku

```bash
heroku create your-todo-bot
heroku config:set BOT_TOKEN=your_token_here
git push heroku main
heroku ps:scale worker=1
```

### Railway

1. Push your repo to GitHub
2. Connect it to [Railway](https://railway.app)
3. Add the `BOT_TOKEN` environment variable
4. Railway auto-detects the `Procfile` and deploys 🚀

<br>

## 🗄️ Database Schema

The bot uses two SQLite tables:

**`tasks`** — Stores all user tasks

| Column | Type | Description |
|---|---|---|
| `id` | INTEGER (PK) | Auto-incrementing task ID |
| `user_id` | INTEGER | Telegram user ID |
| `chat_id` | INTEGER | Telegram chat ID |
| `task` | TEXT | Task description |
| `details` | TEXT | Optional task details / notes |
| `status` | TEXT | `pending` or `completed` |
| `created_at` | TIMESTAMP | Creation timestamp |

**`user_settings`** — Stores per-user preferences

| Column | Type | Description |
|---|---|---|
| `user_id` | INTEGER (PK) | Telegram user ID |
| `language` | TEXT | `ar` or `en` |

<br>

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

<br>

## 👨‍💻 Author

**Ahmed Azzi**

- GitHub: [@AhmedAzzi](https://github.com/AhmedAzzi)

<br>

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

<br>

---

<div align="center">

**⭐ If you found this project useful, give it a star! ⭐**

Made with ❤️ by Ahmed Azzi

</div>
