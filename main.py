import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
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

# Language dictionary
LANGS = {
    'ar': {
        'welcome': 'مرحبًا بك في قائمة المهام! استخدم القائمة أدناه للتنقل.',
        'available_commands': 'الأوامر المتاحة:',
        'add_new_task': 'إضافة مهمة جديدة',
        'list_all_tasks': 'عرض جميع المهام',
        'help_add': 'استخدم زر "إضافة مهمة" لإضافة مهمة جديدة.',
        'help_list': 'استخدم زر "عرض المهام" لعرض جميع المهام.',
        'enter_task': 'الرجاء إدخال مهمتك:',
        'task_added': 'تمت إضافة مهمة جديدة إلى قائمة المهام الخاصة بك',
        'enter_details': 'الرجاء إدخال تفاصيل إضافية لهذه المهمة:',
        'details_added': 'تمت إضافة التفاصيل إلى مهمتك',
        'no_tasks': 'لا توجد مهام في قائمة المهام الخاصة بك',
        'your_todo_list': 'قائمة مهامك:',
        'task_completed': 'تم إكمال المهمة',
        'task_deleted': 'تم حذف المهمة من قائمة المهام الخاصة بك',
        'no_details': 'لا توجد تفاصيل',
        'task_details': 'تفاصيل المهمة: {}',
        'change_language': 'تغيير اللغة',
        'menu': {
            'add_task': 'إضافة مهمة',
            'list_tasks': 'عرض المهام',
            'change_language': 'تغيير اللغة',
            'help': 'المساعدة'
        },
        'help_menu': (
            "🤖 مرحباً بك في بوت قائمة المهام! هذا البوت من تطوير أحمد عزي. 👨‍💻\n\n"
            "يمكنك استخدام الأزرار أدناه لإدارة مهامك بسهولة وكفاءة.\n\n"
            "✅ 📝 **اضافة مهمة جديدة:**\n"
            "استخدم زر \"إضافة مهمة\" لإضافة مهمة جديدة. سيتم طلب منك إدخال المهمة.\n\n"
            "📋 **إضافة تفاصيل للمهمة:**\n"
            "لإضافة تفاصيل للمهمة، اضغط على زر \"📝\" (إضافة تفاصيل) بجانب المهمة.\n\n"
            "👁️ **عرض تفاصيل المهمة:**\n"
            "لمشاهدة تفاصيل المهمة، اضغط على المهمة نفسها في القائمة.\n\n"
            "🗒️ **عرض جميع المهام:**\n"
            "استخدم زر \"عرض المهام\" لعرض جميع المهام الخاصة بك. يمكنك تحديد كل مهمة لإكمالها، عرض التفاصيل، أو حذفها.\n\n"
            "🌐 **تغيير اللغة:**\n"
            "استخدم زر \"تغيير اللغة\" لتغيير لغة البوت.\n\n"
            "❓ **المساعدة:**\n"
            "استخدم زر \"المساعدة\" لعرض هذا الدليل مرة أخرى.\n\n"
            "شكراً لاستخدامك بوت قائمة المهام. نتمنى أن يساعدك في تنظيم مهامك بشكل أفضل! 💕"
        )
    },
    'en': {
        'welcome': 'Welcome to your ToDo list! Use the menu below to navigate.',
        'available_commands': 'Available commands:',
        'add_new_task': 'Add a new task',
        'list_all_tasks': 'List all tasks',
        'help_add': 'Use the "Add Task" button to add a new task.',
        'help_list': 'Use the "List Tasks" button to list all tasks.',
        'enter_task': 'Please enter your task:',
        'task_added': 'A new entry has been added to your ToDo list',
        'enter_details': 'Please enter additional details for this task:',
        'details_added': 'Details have been added to your entry',
        'no_tasks': 'There is no entry in your ToDo list',
        'your_todo_list': 'Your ToDo list:',
        'task_completed': 'Task completed',
        'task_deleted': 'Entry deleted from your ToDo list',
        'no_details': 'No details',
        'task_details': 'Task details: {}',
        'change_language': 'Change language',
        'menu': {
            'add_task': 'Add Task',
            'list_tasks': 'List Tasks',
            'change_language': 'Change Language',
            'help': 'Help'
        },
        'help_menu': (
            "🤖 Welcome to the ToDo List Bot! This bot was developed by Ahmed Ezzy. 👨‍💻\n\n"
            "You can use the buttons below to manage your tasks easily and efficiently.\n\n"
            "✅ 📝 **Add a New Task:**\n"
            "Use the \"Add Task\" button to add a new task. You will be prompted to enter the task.\n\n"
            "📋 **Add Details to a Task:**\n"
            "To add details to a task, click on the \"📝\" (Add Details) button next to the task.\n\n"
            "👁️ **View Task Details:**\n"
            "To view the details of a task, click on the task itself in the list.\n\n"
            "🗒️ **List All Tasks:**\n"
            "Use the \"List Tasks\" button to view all your tasks. You can select each task to complete it, view details, or delete it.\n\n"
            "🌐 **Change Language:**\n"
            "Use the \"Change Language\" button to switch the bot's language.\n\n"
            "❓ **Help:**\n"
            "Use the \"Help\" button to view this guide again.\n\n"
            "Thank you for using the ToDo List Bot. We hope it helps you organize your tasks better! 💕"
        )
    }
}

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
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_settings
    (user_id INTEGER PRIMARY KEY,
     language TEXT)
    ''')
    conn.commit()
    conn.close()

# Helper function to get user language
def get_user_language(user_id):
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('SELECT language FROM user_settings WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 'ar'  # Default to Arabic

# Create main menu
def create_main_menu(lang):
    keyboard = [
        [KeyboardButton(LANGS[lang]['menu']['add_task']), KeyboardButton(LANGS[lang]['menu']['list_tasks'])],
        [KeyboardButton(LANGS[lang]['menu']['change_language']), KeyboardButton(LANGS[lang]['menu']['help'])]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    menu = create_main_menu(lang)
    await update.message.reply_text(LANGS[lang]['welcome'], reply_markup=menu)

async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    menu = create_main_menu(lang)
    await update.message.reply_text(LANGS[lang]['available_commands'], reply_markup=menu)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    help_text = LANGS[lang]['help_menu']
    await update.message.reply_text(help_text)

async def add_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    await update.message.reply_text(LANGS[lang]['enter_task'])
    context.user_data['awaiting_task'] = True

async def list_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, task, status FROM tasks WHERE user_id = ? AND status != "completed"', (user_id,))
    tasks = cursor.fetchall()
    conn.close()

    if not tasks:
        message_text = LANGS[lang]['no_tasks']
        reply_markup = None
    else:
        message_text = LANGS[lang]['your_todo_list']
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

    await update.message.reply_text(message_text, reply_markup=reply_markup)

async def language_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("العربية", callback_data='lang_ar')],
        [InlineKeyboardButton("English", callback_data='lang_en')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Please select your language / يرجى اختيار لغتك", reply_markup=reply_markup)

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    lang = get_user_language(user_id)

    action, task_id = query.data.split('_')
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()

    if action == 'complete':
        cursor.execute('UPDATE tasks SET status = "completed" WHERE id = ?', (task_id,))
        await query.edit_message_text(f"{query.message.text} ✅")
    elif action == 'delete':
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        await query.edit_message_text(LANGS[lang]['task_deleted'])
    elif action == 'detail':
        cursor.execute('SELECT details FROM tasks WHERE id = ?', (task_id,))
        details = cursor.fetchone()[0]
        await query.message.reply_text(LANGS[lang]['enter_details'])
        context.user_data['awaiting_details'] = task_id
    elif action == 'view':
        cursor.execute('SELECT details FROM tasks WHERE id = ?', (task_id,))
        details = cursor.fetchone()[0]
        if details:
            await query.message.reply_text(LANGS[lang]['task_details'].format(details))
        else:
            await query.message.reply_text(LANGS[lang]['no_details'])

    conn.commit()
    conn.close()

    # Refresh the task list
    await list_tasks(update, context)

async def language_button_click(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    new_lang = query.data.split('_')[1]

    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR REPLACE INTO user_settings (user_id, language) VALUES (?, ?)', (user_id, new_lang))
    conn.commit()
    conn.close()

    menu = create_main_menu(new_lang)
    await query.edit_message_text(LANGS[new_lang]['welcome'])
    await query.message.reply_text(LANGS[new_lang]['available_commands'], reply_markup=menu)

async def receive_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    text = update.message.text

    if text == LANGS[lang]['menu']['add_task']:
        await add_task(update, context)
    elif text == LANGS[lang]['menu']['list_tasks']:
        await list_tasks(update, context)
    elif text == LANGS[lang]['menu']['change_language']:
        await language_menu(update, context)
    elif text == LANGS[lang]['menu']['help']:
        await help_command(update, context)
    elif 'awaiting_task' in context.user_data and context.user_data['awaiting_task']:
        task = text
        conn = sqlite3.connect('todo.db', detect_types=sqlite3.PARSE_DECLTYPES)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tasks (user_id, task, status, created_at) VALUES (?, ?, ?, ?)',
                       (user_id, task, 'pending', datetime.now()))
        conn.commit()
        conn.close()
        del context.user_data['awaiting_task']
        await update.message.reply_text(LANGS[lang]['task_added'])
    elif 'awaiting_details' in context.user_data:
        task_id = context.user_data['awaiting_details']
        details = text
        conn = sqlite3.connect('todo.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE tasks SET details = ? WHERE id = ?', (details, task_id))
        conn.commit()
        conn.close()
        del context.user_data['awaiting_details']
        await update.message.reply_text(LANGS[lang]['details_added'])

def main() -> None:
    application = Application.builder().token('7334709119:AAGOeczOyD2BAjLMaIMIOEapbYe_rrH043Q').build()

    # Set up database
    setup_database()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", menu_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("add", add_task))
    application.add_handler(CommandHandler("list", list_tasks))
    application.add_handler(CallbackQueryHandler(button_click, pattern='^(complete|delete|detail|view)_'))
    application.add_handler(CallbackQueryHandler(language_button_click, pattern='^lang_'))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive_task))

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
