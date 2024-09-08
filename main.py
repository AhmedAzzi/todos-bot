import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import telegram
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
import sqlite3
from datetime import datetime


def adapt_datetime(ts):
    return ts.isoformat()

def convert_datetime(s):
    return datetime.fromisoformat(s)

sqlite3.register_adapter(datetime, adapt_datetime)
sqlite3.register_converter("datetime", convert_datetime)



# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Database setup
def setup_database():
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
     user_id INTEGER,
     task TEXT,
     details TEXT,
     status TEXT,
     created_at TIMESTAMP)
    ''')
    conn.commit()
    conn.close()

# Command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Welcome to your ToDo list! Use /help to see available commands.')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Add a new task", callback_data='help_add')],
        [InlineKeyboardButton("List all tasks", callback_data='help_list')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Available commands:', reply_markup=reply_markup)

async def help_button_click(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'help_add':
        help_text = 'Use /add to add a new task. You will be prompted to enter the task on the next line.'
    elif query.data == 'help_list':
        help_text = 'Use /list to list all tasks.'

    await query.edit_message_text(help_text)

async def add_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    await update.message.reply_text('Please enter your task on the next line:')
    context.user_data['awaiting_task'] = True

async def receive_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if 'awaiting_task' in context.user_data and context.user_data['awaiting_task']:
        user_id = update.effective_user.id
        task = update.message.text

        conn = sqlite3.connect('todo.db', detect_types=sqlite3.PARSE_DECLTYPES)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tasks (user_id, task, status, created_at) VALUES (?, ?, ?, ?)',
                       (user_id, task, 'pending', datetime.now()))
        conn.commit()
        conn.close()

        del context.user_data['awaiting_task']
        await update.message.reply_text('A new entry has been added to your ToDo list')
    elif 'awaiting_details' in context.user_data:
        task_id = context.user_data['awaiting_details']
        details = update.message.text

        conn = sqlite3.connect('todo.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE tasks SET details = ? WHERE id = ?', (details, task_id))
        conn.commit()
        conn.close()

        del context.user_data['awaiting_details']
        await update.message.reply_text("Details have been added to your entry")

async def list_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, task, status FROM tasks WHERE user_id = ? AND status != "completed"', (user_id,))
    tasks = cursor.fetchall()
    conn.close()

    if not tasks:
        message_text = 'There is no entry in your ToDo list'
        reply_markup = None
    else:
        message_text = 'Your ToDo list:'
        keyboard = []
        for task in tasks:
            task_text = f"{task[1]} {'✅' if task[2] == 'completed' else ''}"
            keyboard.append([InlineKeyboardButton(task_text, callback_data=f'view_{task[0]}')])
            keyboard.append([
                InlineKeyboardButton("✅", callback_data=f'complete_{task[0]}'),
                InlineKeyboardButton("📝", callback_data=f'detail_{task[0]}'),
                InlineKeyboardButton("❌", callback_data=f'delete_{task[0]}')
            ])
        reply_markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query:
        # Check if the message content has changed
        if update.callback_query.message.text != message_text or update.callback_query.message.reply_markup != reply_markup:
            try:
                await update.callback_query.edit_message_text(message_text, reply_markup=reply_markup)
            except telegram.error.BadRequest as e:
                if str(e) != "Message is not modified":
                    raise
        else:
            # If the content hasn't changed, just answer the callback query
            await update.callback_query.answer()
    else:
        await update.message.reply_text(message_text, reply_markup=reply_markup)
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    action, task_id = query.data.split('_')
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()

    if action == 'complete':
        cursor.execute('UPDATE tasks SET status = "completed" WHERE id = ?', (task_id,))
        await query.edit_message_text(f"{query.message.text} ✅")
    elif action == 'delete':
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        await query.edit_message_text("Entry deleted from your ToDo list")
    elif action == 'detail':
        cursor.execute('SELECT details FROM tasks WHERE id = ?', (task_id,))
        details = cursor.fetchone()[0]
        await query.message.reply_text("Please enter additional details for this task:")
        context.user_data['awaiting_details'] = task_id
    elif action == 'view':
        cursor.execute('SELECT details FROM tasks WHERE id = ?', (task_id,))
        details = cursor.fetchone()[0]
        if details:
            await query.message.reply_text(f"Task details: {details}")
        else:
            await query.message.reply_text(f"No details")

    conn.commit()
    conn.close()

    # Refresh the task list
    await list_tasks(update, context)


def main() -> None:
    # Replace 'YOUR_BOT_TOKEN' with your actual bot token
    application = Application.builder().token('7334709119:AAGOeczOyD2BAjLMaIMIOEapbYe_rrH043Q').build()

    # Set up database
    setup_database()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("add", add_task))
    application.add_handler(CommandHandler("list", list_tasks))
    application.add_handler(CallbackQueryHandler(button_click))
    application.add_handler(CallbackQueryHandler(help_button_click))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive_task))

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()