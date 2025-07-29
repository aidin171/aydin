import g4f
import asyncio
import logging
import random
import json
import os
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes, CallbackQueryHandler

# تنظیمات لاگ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = "8319765501:AAEJ8_k-qas6VB6TYDdwOite1hQjaBlSs1w"

# فایل‌های ذخیره‌سازی
USERS_FILE = "users_data.json"
TASKS_FILE = "tasks_data.json"
SCORES_FILE = "scores_data.json"

# ذخیره داده‌های کاربران و کارها
users_data = {}
tasks_data = {}
scores_data = {}

# بارگذاری داده‌ها از فایل
def load_data():
    global users_data, tasks_data, scores_data
    try:
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                users_data = json.load(f)
        if os.path.exists(TASKS_FILE):
            with open(TASKS_FILE, 'r', encoding='utf-8') as f:
                tasks_data = json.load(f)
        if os.path.exists(SCORES_FILE):
            with open(SCORES_FILE, 'r', encoding='utf-8') as f:
                scores_data = json.load(f)
    except Exception as e:
        logger.error(f"خطا در بارگذاری داده‌ها: {e}")

# ذخیره داده‌ها در فایل
def save_data():
    try:
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(users_data, f, ensure_ascii=False, indent=2)
        with open(TASKS_FILE, 'w', encoding='utf-8') as f:
            json.dump(tasks_data, f, ensure_ascii=False, indent=2)
        with open(SCORES_FILE, 'w', encoding='utf-8') as f:
            json.dump(scores_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"خطا در ذخیره داده‌ها: {e}")

# اطلاعات ربات - بهتر شده
BOT_INFO = """
🤖 <b>بات هوشمند g4f</b> - نسخه کامل

✨ <b>قابلیت‌های پیشرفته:</b>
├ 🧠 چت هوشمند با هر موضوع
├ 🎭 چت با شخصیت‌های معروف
├ 💻 تولید کد برنامه‌نویسی
├ 🌍 ترجمه پیشرفته
├ 📚 خلاصه‌سازی متن
├ 🔍 بررسی املای فارسی
├ 📖 تولید داستان
├ 🧮 حل مسئله ریاضی
├ 📋 مدیریت کارها
├ 🎮 بازی‌های ذهنی
├ 💡 تولید ایده خلاقانه
├ 📊 تحلیل متن
├ 📱 محتوای شبکه‌های اجتماعی
├ 🔢 بازی‌های ریاضی
├ 🧩 بازی‌های کلمه‌ای
├ 🎲 بازی‌های تصادفی
├ 🎵 تولید موسیقی
├ 📈 تحلیل داده‌ها
├ 📝 نوشتن مقاله
└ 🔮 فال و طالع‌بینی

💡 <b>مزایای استفاده:</b>
• بدون نیاز به VPN
• بدون نیاز به کامپیوتر همیشه روشن
• بدون نیاز به پول یا API Key
• کاملاً رایگان و محلی

👨‍💻 <b>توسعه‌دهنده: آسانسور</b>
"""

# منوی زیبا
MAIN_MENU = [
    [InlineKeyboardButton("🧠 چت هوشمند", callback_data="chat_main")],
    [InlineKeyboardButton("🎭 شخصیت‌ها", callback_data="character_menu"),
     InlineKeyboardButton("💻 کد", callback_data="code_menu")],
    [InlineKeyboardButton("🌍 ترجمه", callback_data="translate_menu"),
     InlineKeyboardButton("📚 خلاصه", callback_data="summarize_menu")],
    [InlineKeyboardButton("📖 داستان", callback_data="story_menu"),
     InlineKeyboardButton("🧮 ریاضی", callback_data="math_menu")],
    [InlineKeyboardButton("📋 کارها", callback_data="tasks_menu"),
     InlineKeyboardButton("🎮 بازی", callback_data="game_menu")],
    [InlineKeyboardButton("💡 ایده", callback_data="idea_menu"),
     InlineKeyboardButton("🎨 تصویر", callback_data="imagine_menu")],
    [InlineKeyboardButton("📊 تحلیل", callback_data="analyze_menu"),
     InlineKeyboardButton("📱 شبکه‌ها", callback_data="social_menu")],
    [InlineKeyboardButton("🔮 فال", callback_data="fortune_menu"),
     InlineKeyboardButton("🎵 موسیقی", callback_data="music_menu")],
    [InlineKeyboardButton("📈 داده‌ها", callback_data="data_menu"),
     InlineKeyboardButton("📝 مقاله", callback_data="article_menu")],
    [InlineKeyboardButton("⚙️ تنظیمات", callback_data="settings_menu"),
     InlineKeyboardButton("❓ راهنما", callback_data="help")]
]

# منوهای فرعی
CHARACTER_MENU = [
    [InlineKeyboardButton("آینشتین", callback_data="character_einstein"),
     InlineKeyboardButton("نیوتن", callback_data="character_newton")],
    [InlineKeyboardButton("شکسپیر", callback_data="character_shakespeare"),
     InlineKeyboardButton("ماری کوری", callback_data="character_curie")],
    [InlineKeyboardButton("بازگشت ⬅️", callback_data="main_menu")]
]

CODE_MENU = [
    [InlineKeyboardButton("پایتون", callback_data="code_python"),
     InlineKeyboardButton("جاوااسکریپت", callback_data="code_javascript")],
    [InlineKeyboardButton("جاوا", callback_data="code_java"),
     InlineKeyboardButton("سی++", callback_data="code_cpp")],
    [InlineKeyboardButton("بازگشت ⬅️", callback_data="main_menu")]
]

GAME_MENU = [
    [InlineKeyboardButton("🔢 بازی ریاضی", callback_data="math_game")],
    [InlineKeyboardButton("🧩 بازی کلمه‌ای", callback_data="word_game")],
    [InlineKeyboardButton("🎲 بازی تصادفی", callback_data="dice_game")],
    [InlineKeyboardButton("🎯 حدس عدد", callback_data="guess_game")],
    [InlineKeyboardButton("🔤 آوایی", callback_data="phonetic_game")],
    [InlineKeyboardButton("بازگشت ⬅️", callback_data="main_menu")]
]

MATH_MENU = [
    [InlineKeyboardButton("🧮 حل مسئله", callback_data="math_solve")],
    [InlineKeyboardButton("🔢 تمرین ریاضی", callback_data="math_practice")],
    [InlineKeyboardButton("📊 آمار ریاضی", callback_data="math_stats")],
    [InlineKeyboardButton("بازگشت ⬅️", callback_data="main_menu")]
]

# ذخیره داده‌های کاربران
user_tasks = {}
user_contexts = {}
user_scores = {}  # برای ذخیره امتیازات بازی

# توابع کمکی با انیمیشن
async def send_animated_message(update: Update, text: str) -> object:
    """ارسال پیام با انیمیشن"""
    return await update.message.reply_text(f"✨ {text}")

async def send_searching_animation(update: Update) -> object:
    """ارسال انیمیشن جست و جو"""
    animations = ["🔍", "🔎", "🎯", "💡"]
    message = await update.message.reply_text("🔍 در حال جست و جو...")
    # می‌تونیم انیمیشن بیشتری اضافه کنیم
    return message

async def delete_message(message) -> None:
    """پاک کردن پیام با امنیت"""
    try:
        await message.delete()
    except Exception as e:
        logger.warning(f"خطا در پاک کردن پیام: {e}")

# دستورات اصلی با رابط کاربری بهتر
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """صفحه شروع با منوی زیبا"""
    user_id = str(update.effective_user.id)
    
    # ذخیره اطلاعات کاربر
    if user_id not in users_data :
        users_data[user_id] = {
            "first_name": update.effective_user.first_name,
            "last_name": update.effective_user.last_name,
            "username": update.effective_user.username,
            "join_date": datetime.now().isoformat()
        }
        save_data()
    
    keyboard = InlineKeyboardMarkup(MAIN_MENU)
    await update.message.reply_text(
        BOT_INFO, 
        parse_mode="HTML", 
        reply_markup=keyboard
    )

async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """نمایش منوی اصلی"""
    keyboard = InlineKeyboardMarkup(MAIN_MENU)
    if update.message:
        await update.message.reply_text("📋 <b>منوی اصلی</b>", parse_mode="HTML", reply_markup=keyboard)
    else:
        await update.callback_query.message.reply_text("📋 <b>منوی اصلی</b>", parse_mode="HTML", reply_markup=keyboard)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """مدیریت کلیک روی دکمه‌ها"""
    query = update.callback_query
    await query.answer()
    
    # منوهای اصلی
    if query.data == "main_menu":
        await show_menu(update, context)
    elif query.data == "chat_main":
        await query.message.reply_text("💬 چت هوشمند فعال شد! پیامتو بفرست.")
    elif query.data == "character_menu":
        keyboard = InlineKeyboardMarkup(CHARACTER_MENU)
        await query.edit_message_text("🎭 انتخاب شخصیت:", reply_markup=keyboard)
    elif query.data == "code_menu":
        keyboard = InlineKeyboardMarkup(CODE_MENU)
        await query.edit_message_text("💻 انتخاب زبان برنامه‌نویسی:", reply_markup=keyboard)
    elif query.data == "game_menu":
        keyboard = InlineKeyboardMarkup(GAME_MENU)
        await query.edit_message_text("🎮 انتخاب بازی:", reply_markup=keyboard)
    elif query.data == "math_menu":
        keyboard = InlineKeyboardMarkup(MATH_MENU)
        await query.edit_message_text("🧮 انتخاب بخش ریاضی:", reply_markup=keyboard)
    elif query.data.startswith("character_"):
        character_map = {
            "einstein": "آینشتین",
            "newton": "نیوتن", 
            "shakespeare": "شکسپیر",
            "curie": "ماری کوری"
        }
        char_name = character_map.get(query.data.split("_")[1], "شخصیت نامعلوم")
        await query.message.reply_text(f"🎭 چت با {char_name} فعال شد!\nپیامتو بفرست تا با اون چت کنی.")
    elif query.data.startswith("code_"):
        lang_map = {
            "python": "پایتون",
            "javascript": "جاوااسکریپت",
            "java": "جاوا",
            "cpp": "سی++"
        }
        lang_name = lang_map.get(query.data.split("_")[1], "زبان نامعلوم")
        await query.message.reply_text(f"💻 تولید کد {lang_name} فعال شد!\nتوضیحاتت رو بفرست.")
    elif query.data == "help":
        await help_command(query, context)
    elif query.data == "math_game":
        await math_game_start(query, context)
    elif query.data == "word_game":
        await word_game_start(query, context)
    elif query.data == "dice_game":
        await dice_game_start(query, context)
    elif query.data == "guess_game":
        await guess_game_start(query, context)
    elif query.data == "phonetic_game":
        await phonetic_game_start(query, context)
    # بقیه منوها...

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """راهنمای بهتر"""
    help_text = """
📚 <b>راهنمای استفاده از بات</b>

🎯 <b>روش کار با بات:</b>
• از دکمه‌های منو استفاده کن
• یا دستورات زیر رو بفرست

🎛️ <b>دستورات اصلی:</b>
/start - صفحه شروع با منو
/menu - نمایش منوی اصلی
/help - راهنمای استفاده

🎭 <b>دستورات تخصصی:</b>
/character [شخصیت] [پیام]
/code [زبان] [توضیح]
/translate [سبک] [زبان] [متن]
/summarize [متن]
/spell [متن]
/story [ژانر] [موضوع]
/math [مسئله]
/mathgame - بازی ریاضی
/wordgame - بازی کلمه‌ای
/dicegame - بازی تصادفی
/guessgame - حدس عدد
/phoneticgame - آوایی
/addtask [کار]
/tasks
/game
/idea [موضوع]
/analyze [متن]
/post [پلتفرم] [موضوع]
/imagine [توضیح]
/data [موضوع]
/article [موضوع]
/music [موضوع]
/fortune - فال

💡 <b>نکات مهم:</b>
• همه قابلیت‌ها رایگان هستن
• نیازی به VPN نداره
• نیازی به کامپیوتر همیشه روشن نداره
"""
    
    if isinstance(update, Update) and update.message:
        await update.message.reply_text(help_text, parse_mode="HTML")
    else:
        await update.callback_query.edit_message_text(help_text, parse_mode="HTML")

# چت عادی با بهبود
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """چت هوشمند با انیمیشن بهتر"""
    user_message = update.message.text
    user_id = str(update.effective_user.id)
    
    try:
        searching_message = await send_searching_animation(update)
        
        # استفاده از g4f با تنظیمات بهتر
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=[{"role": "user", "content": user_message}],
        )
        
        await delete_message(searching_message)
        
        # نمایش پاسخ با فرمت بهتر
        await update.message.reply_text(
            f"💬 <b>پاسخ من:</b>\n\n{response}", 
            parse_mode="HTML"
        )
        
    except Exception as e:
        logger.error(f"خطا در چت: {e}")
        try:
            await delete_message(searching_message)
        except:
            pass
        await update.message.reply_text("❌ مشکلی پیش اومد! دوباره تلاش کن.")

# چت با شخصیت‌های معروف - درست شده
async def character_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("مثال: /character einstein سلام دنیا")
        return
    character = context.args[0]
    message = " ".join(context.args[1:])
    try:
        searching_message = await send_searching_animation(update)
        prompt = f"تو {character} هستی. به سوال من با دانش و سبک این شخصیت جواب بده: {message}"
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=[{"role": "user", "content": prompt}],
        )
        await delete_message(searching_message)
        # درست کردن خط شکسته
        result_text = f"🎭 به عنوان {character}:\n{response}"
        await update.message.reply_text(result_text, parse_mode="HTML")
    except Exception as e:
        logger.error(f"خطا در چت با شخصیت: {e}")
        try:
            await delete_message(searching_message)
        except:
            pass
        await update.message.reply_text("❌ مشکلی پیش اومد!")

# تولید کد برنامه‌نویسی - درست شده
async def code_generator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("مثال: /code python تابع فیبوناچی")
        return
    request = " ".join(context.args)
    try:
        searching_message = await send_searching_animation(update)
        prompt = f"فقط کد رو بنویس، بدون توضیح. {request}"
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=[{"role": "user", "content": prompt}],
        )
        await delete_message(searching_message)
        # درست کردن خط شکسته
        result_text = f"💻 کد درخواستی:\n```\n{response}\n```"
        await update.message.reply_text(result_text, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"خطا در تولید کد: {e}")
        try:
            await delete_message(searching_message)
        except:
            pass
        await update.message.reply_text("❌ مشکلی پیش اومد!")

# ترجمه پیشرفته
async def advanced_translate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 3:
        await update.message.reply_text("مثال: /translate formal english سلام دنیا")
        return
    style = context.args[0]
    target_lang = context.args[1]
    text = " ".join(context.args[2:])
    try:
        searching_message = await send_searching_animation(update)
        prompt = f"این متن رو به سبک {style} به {target_lang} ترجمه کن: {text}"
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=[{"role": "user", "content": prompt}],
        )
        await delete_message(searching_message)
        # اضافه کردن قابلیت جدید: تلفظ
        pronunciation_prompt = f"تلفظ این ترجمه چیه؟ {response[:50]}"
        pronunciation_response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=[{"role": "user", "content": pronunciation_prompt}],
        )
        result_text = f"🌍 ترجمه ({style} به {target_lang}):\n{response}\n\n📢 تلفظ: {pronunciation_response}"
        await update.message.reply_text(result_text, parse_mode="HTML")
    except Exception as e:
        logger.error(f"خطا در ترجمه: {e}")
        try:
            await delete_message(searching_message)
        except:
            pass
        await update.message.reply_text("❌ مشکلی پیش اومد!")

# خلاصه‌سازی متن
async def summarize_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("مثال: /summarize متنی که می‌خوای خلاصه بشه")
        return
    text = " ".join(context.args)
    try:
        searching_message = await send_searching_animation(update)
        prompt = f"متن رو به صورت خلاصه و مفید خلاصه کن: {text}"
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=[{"role": "user", "content": prompt}],
        )
        await delete_message(searching_message)
        # اضافه کردن قابلیت جدید: کلمات کلیدی
        keywords_prompt = f"۵ کلمه کلیدی این خلاصه چیه؟ {response[:100]}"
        keywords_response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=[{"role": "user", "content": keywords_prompt}],
        )
        result_text = f"📚 خلاصه:\n{response}\n\n🔑 کلمات کلیدی: {keywords_response}"
        await update.message.reply_text(result_text, parse_mode="HTML")
    except Exception as e:
        logger.error(f"خطا در خلاصه‌سازی: {e}")
        try:
            await delete_message(searching_message)
        except:
            pass
        await update.message.reply_text("❌ مشکلی پیش اومد!")

# بررسی املای فارسی
async def spell_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("مثال: /spell متن با اشکال املایی")
        return
    text = " ".join(context.args)
    try:
        searching_message = await send_searching_animation(update)
        prompt = f"فقط متن اصلاح شده رو بنویس، بدون توضیح اضافی: {text}"
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=[{"role": "user", "content": prompt}],
        )
        await delete_message(searching_message)
        # اضافه کردن قابلیت جدید: توضیح اشتباهات
        error_prompt = f"چه اشتباهاتی در متن اولیه بود؟ {text[:50]}"
        error_response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=[{"role": "user", "content": error_prompt}],
        )
        result_text = f"🔍 اصلاح شده:\n{response}\n\n📝 توضیح اشتباهات: {error_response}"
        await update.message.reply_text(result_text, parse_mode="HTML")
    except Exception as e:
        logger.error(f"خطا در بررسی املایی: {e}")
        try:
            await delete_message(searching_message)
        except:
            pass
        await update.message.reply_text("❌ مشکلی پیش اومد!")

# تولید داستان
async def story_generator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    genre = context.args[0] if context.args else "عمومی"
    topic = " ".join(context.args[1:]) if len(context.args) > 1 else "ماجراجویی"
    try:
        searching_message = await send_searching_animation(update)
        prompt = f"یه داستان کوتاه و جذاب در ژانر {genre} درباره {topic} بنویس"
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=[{"role": "user", "content": prompt}],
        )
        await delete_message(searching_message)
        # اضافه کردن قابلیت جدید: سوال درباره داستان
        question_prompt = f"یه سوال جالب درباره این داستان بپرس: {response[:100]}"
        question_response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=[{"role": "user", "content": question_prompt}],
        )
        result_text = f"📖 داستان ({genre} - {topic}):\n{response}\n\n❓ سوال: {question_response}"
        await update.message.reply_text(result_text, parse_mode="HTML")
    except Exception as e:
        logger.error(f"خطا در تولید داستان: {e}")
        try:
            await delete_message(searching_message)
        except:
            pass
        await update.message.reply_text("❌ مشکلی پیش اومد!")

# حل مسئله ریاضی
async def math_solver(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("مثال: /math 2+2=?")
        return
    problem = " ".join(context.args)
    try:
        searching_message = await send_searching_animation(update)
        prompt = f"تو یه استاد ریاضی هستی. مسئله رو حل کن و راه حل رو توضیح بده: {problem}"
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=[{"role": "user", "content": prompt}],
        )
        await delete_message(searching_message)
        # اضافه کردن قابلیت جدید: مثال مشابه
        example_prompt = f"یه مسئله ریاضی مشابه این حل کن: {problem[:30]}"
        example_response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=[{"role": "user", "content": example_prompt}],
        )
        result_text = f"🧮 حل مسئله:\n{response}\n\n🔢 مثال مشابه: {example_response}"
        await update.message.reply_text(result_text, parse_mode="HTML")
    except Exception as e:
        logger.error(f"خطا در حل مسئله: {e}")
        try:
            await delete_message(searching_message)
        except:
            pass
        await update.message.reply_text("❌ مشکلی پیش اومد!")

# بازی ریاضی
async def math_game_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # سوالات ریاضی تصادفی
    operations = ['+', '-', '*']
    op = random.choice(operations)
    a = random.randint(1, 20)
    b = random.randint(1, 20)
    
    if op == '+':
        answer = a + b
        question = f"{a} + {b} = ?"
    elif op == '-':
        if a < b:
            a, b = b, a
        answer = a - b
        question = f"{a} - {b} = ?"
    else:
        answer = a * b
        question = f"{a} × {b} = ?"
    
    # ذخیره جواب در context برای چک کردن بعداً
    context.user_data['math_answer'] = answer
    context.user_data['math_question'] = question
    
    if isinstance(update, Update):
        await update.message.reply_text(f"🔢 سوال ریاضی:\n{question}\n\nپاسختو بفرست!")
    else:
        await update.edit_message_text(f"🔢 سوال ریاضی:\n{question}\n\nپاسختو بفرست!")

# چک کردن پاسخ بازی ریاضی
async def check_math_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'math_answer' in context.user_data:
        try:
            user_answer = int(update.message.text)
            correct_answer = context.user_data['math_answer']
            question = context.user_data['math_question']
            
            if user_answer == correct_answer:
                # اضافه کردن امتیاز
                user_id = str(update.effective_user.id)
                if user_id not in scores_data:
                    scores_data[user_id] = {"math": 0, "total": 0}
                scores_data[user_id]["math"] += 10
                scores_data[user_id]["total"] += 10
                save_data()
                
                await update.message.reply_text(
                    f"🎉 درسته! جواب {correct_answer} هست.\n\n"
                    f"✅ ۱۰ امتیاز گرفتی!\n"
                    f"امتیاز ریاضی: {scores_data[user_id]['math']}\n"
                    f"امتیاز کل: {scores_data[user_id]['total']}"
                )
            else:
                await update.message.reply_text(f"❌ اشتباه! جواب درست {correct_answer} هست.\nسوال: {question}")
            
            # پاک کردن داده‌ها
            del context.user_data['math_answer']
            del context.user_data['math_question']
            
        except ValueError:
            await update.message.reply_text("لطفاً یه عدد بفرست!")
    else:
        # اگه کسی فقط یه عدد می‌فرسته، بهش چت کن
        await chat(update, context)

# بازی کلمه‌ای
async def word_game_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    games = [
        "معما: چیزی که هر شب می‌آید ولی هر صبح می‌رود چیست؟ (پاسخ: خواب)",
        "کلمه‌بازی: کلمه‌ای پیدا کن که با 'ک' شروع شه و با 'ر' تموم شه (مثال: کتاب، کمر)",
        "لغز: سفیده ولی می‌دونه، وقتی صحبت می‌کنه دم می‌کشه (پاسخ: گوش)",
        "دنبال کلمه بگرد: کلمه‌ای ۵ حرفی که حرف دومش 'ا' هست",
        "ضد کلمه: ضد 'بزرگ' چیه؟"
    ]
    
    game = random.choice(games)
    if isinstance(update, Update):
        await update.message.reply_text(f"🧩 بازی کلمه‌ای:\n{game}\n\nپاسختو بفرست!")
    else:
        await update.edit_message_text(f"🧩 بازی کلمه‌ای:\n{game}\n\nپاسختو بفرست!")

# بازی تصادفی
async def dice_game_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # تاس ۶ وجهی
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    total = dice1 + dice2
    
    # بازی حدس عدد
    target = random.randint(2, 12)
    
    result_text = (
        f"🎲 بازی تصادفی:\n"
        f"تاس ۱: {dice1}\n"
        f"تاس ۲: {dice2}\n"
        f"جمع: {total}\n"
        f"هدف: عدد {target}\n\n"
        f"{'🎉 برنده شدی!' if total == target else '😅 شانس بعدی!'}"
    )
    
    if isinstance(update, Update):
        await update.message.reply_text(result_text)
    else:
        await update.edit_message_text(result_text)

# بازی حدس عدد
async def guess_game_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # عدد تصادفی بین 1 تا 100
    secret_number = random.randint(1, 100)
    context.user_data['secret_number'] = secret_number
    context.user_data['guess_attempts'] = 0
    
    if isinstance(update, Update):
        await update.message.reply_text("🎯 بازی حدس عدد:\nعددی بین 1 تا 100 حدس بزن!\n\nپاسختو بفرست!")
    else:
        await update.edit_message_text("🎯 بازی حدس عدد:\nعددی بین 1 تا 100 حدس بزن!\n\nپاسختو بفرست!")

# چک کردن حدس عدد
async def check_guess_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'secret_number' in context.user_data:
        try:
            user_guess = int(update.message.text)
            secret_number = context.user_data['secret_number']
            attempts = context.user_data.get('guess_attempts', 0) + 1
            context.user_data['guess_attempts'] = attempts
            
            if user_guess == secret_number:
                # امتیاز بر اساس تعداد تلاش‌ها
                score = max(50 - (attempts * 5), 10)
                
                user_id = str(update.effective_user.id)
                if user_id not in scores_data:
                    scores_data[user_id] = {"guess": 0, "total": 0}
                scores_data[user_id]["guess"] += score
                scores_data[user_id]["total"] += score
                save_data()
                
                await update.message.reply_text(
                    f"🎉 تبریک! عدد {secret_number} بود.\n"
                    f"تعداد تلاش‌ها: {attempts}\n"
                    f"امتیاز: {score}\n"
                    f"امتیاز حدس: {scores_data[user_id]['guess']}\n"
                    f"امتیاز کل: {scores_data[user_id]['total']}"
                )
                
                # پاک کردن داده‌ها
                del context.user_data['secret_number']
                del context.user_data['guess_attempts']
                
            elif user_guess < secret_number:
                await update.message.reply_text(f"🔼 عدد بزرگتره! تلاش {attempts}")
            else:
                await update.message.reply_text(f"🔽 عدد کوچیکتره! تلاش {attempts}")
                
        except ValueError:
            await update.message.reply_text("لطفاً یه عدد بین 1 تا 100 بفرست!")
    else:
        await chat(update, context)

# بازی آوایی
async def phonetic_game_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    words = [
        ("سلام", "s(a)l(a)m"),
        ("خوبی", "kh(o)b(i)"),
        ("دوست", "d(o)st"),
        ("کتاب", "k(e)t(a)b"),
        ("مدرسه", "m(a)d(a)rs(e)")
    ]
    
    word, phonetic = random.choice(words)
    context.user_data['phonetic_answer'] = phonetic
    context.user_data['phonetic_word'] = word
    
    if isinstance(update, Update):
        await update.message.reply_text(
            f"🔤 بازی آوایی:\n"
            f"آوای کلمه '{word}' چیه؟\n"
            f"مثال: s(a)l(a)m\n\n"
            f"پاسختو بفرست!"
        )
    else:
        await update.edit_message_text(
            f"🔤 بازی آوایی:\n"
            f"آوای کلمه '{word}' چیه؟\n"
            f"مثال: s(a)l(a)m\n\n"
            f"پاسختو بفرست!"
        )

# چک کردن پاسخ آوایی
async def check_phonetic_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'phonetic_answer' in context.user_data:
        user_answer = update.message.text.strip()
        correct_answer = context.user_data['phonetic_answer']
        word = context.user_data['phonetic_word']
        
        if user_answer.lower() == correct_answer.lower():
            # امتیاز
            user_id = str(update.effective_user.id)
            if user_id not in scores_data:
                scores_data[user_id] = {"phonetic": 0, "total": 0}
            scores_data[user_id]["phonetic"] += 15
            scores_data[user_id]["total"] += 15
            save_data()
            
            await update.message.reply_text(
                f"🎉 درسته! آوای '{word}' {correct_answer} هست.\n\n"
                f"✅ ۱۵ امتیاز گرفتی!\n"
                f"امتیاز آوایی: {scores_data[user_id]['phonetic']}\n"
                f"امتیاز کل: {scores_data[user_id]['total']}"
            )
        else:
            await update.message.reply_text(
                f"❌ اشتباه! آوای '{word}' {correct_answer} هست.\n"
                f"پاسخ شما: {user_answer}"
            )
        
        # پاک کردن داده‌ها
        del context.user_data['phonetic_answer']
        del context.user_data['phonetic_word']
    else:
        await chat(update, context)

# مدیریت کارها
async def add_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    task = " ".join(context.args)
    if not task:
        await update.message.reply_text("مثال: /addtask خرید نان")
        return
    if user_id not in tasks_data:
        tasks_data[user_id] = []
    
    task_data = {
        "task": task,
        "date": datetime.now().isoformat(),
        "completed": False
    }
    
    tasks_data[user_id].append(task_data)
    save_data()
    
    await update.message.reply_text(f"✅ کار اضافه شد: {task}")

async def list_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if user_id in tasks_data and tasks_data[user_id]:
        tasks_list = ""
        for i, task_data in enumerate(tasks_data[user_id], 1):
            status = "✅" if task_data["completed"] else "⏳"
            tasks_list += f"{status} {i}. {task_data['task']}\n"
        await update.message.reply_text(f"📋 <b>لیست کارهای شما:</b>\n\n{tasks_list}", parse_mode="HTML")
    else:
        await update.message.reply_text("😊 <b>کاری نداری!</b> استراحت کن!", parse_mode="HTML")

# تولید ایده خلاقانه
async def idea_generator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topic = " ".join(context.args) if context.args else "کسب‌وکار"
    try:
        searching_message = await send_searching_animation(update)
        prompt = f"۵ ایده خلاقانه درباره {topic} بده"
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=[{"role": "user", "content": prompt}],
        )
        await delete_message(searching_message)
        # اضافه کردن قابلیت جدید: اولویت‌بندی ایده‌ها
        priority_prompt = f"این ایده‌ها رو از نظر عملی بودن اولویت‌بندی کن: {topic}"
        priority_response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=[{"role": "user", "content": priority_prompt}],
        )
        result_text = f"💡 ایده‌های {topic}:\n{response}\n\n📊 اولویت‌بندی: {priority_response}"
        await update.message.reply_text(result_text, parse_mode="HTML")
    except Exception as e:
        logger.error(f"خطا در تولید ایده: {e}")
        try:
            await delete_message(searching_message)
        except:
            pass
        await update.message.reply_text("❌ مشکلی پیش اومد!")

# تحلیل متن
async def text_analyzer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("مثال: /analyze متنی که می‌خوای تحلیل بشه")
        return
    text = " ".join(context.args)
    try:
        searching_message = await send_searching_animation(update)
        prompt = f"این متن رو از نظر احساسات، سبک نوشتار و کلمات کلیدی تحلیل کن: {text}"
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=[{"role": "user", "content": prompt}],
        )
        await delete_message(searching_message)
        # اضافه کردن قابلیت جدید: پیشنهاد بهبود
        improvement_prompt = f"چطور می‌تونم این متن رو بهتر کنم؟ {text[:50]}"
        improvement_response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=[{"role": "user", "content": improvement_prompt}],
        )
        result_text = f"📊 تحلیل متن:\n{response}\n\n🔧 پیشنهاد بهبود: {improvement_response}"
        await update.message.reply_text(result_text, parse_mode="HTML")
    except Exception as e:
        logger.error(f"خطا در تحلیل متن: {e}")
        try:
            await delete_message(searching_message)
        except:
            pass
        await update.message.reply_text("❌ مشکلی پیش اومد!")

# محتوای شبکه‌های اجتماعی
async def social_content(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("مثال: /post instagram چگونه برنامه‌نویس شویم؟")
        return
    platform = context.args[0]
    topic = " ".join(context.args[1:])
    try:
        searching_message = await send_searching_animation(update)
        prompt = f"یه پست جذاب برای {platform} درباره {topic} بنویس"
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=[{"role": "user", "content": prompt}],
        )
        await delete_message(searching_message)
        # اضافه کردن قابلیت جدید: هشتگ
        hashtag_prompt = f"۵ هشتگ مناسب برای این پست چیه؟ {topic[:30]}"
        hashtag_response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=[{"role": "user", "content": hashtag_prompt}],
        )
        result_text = f"📱 پست برای {platform}:\n{response}\n\n🏷️ هشتگ‌ها: {hashtag_response}"
        await update.message.reply_text(result_text, parse_mode="HTML")
    except Exception as e:
        logger.error(f"خطا در تولید محتوای اجتماعی: {e}")
        try:
            await delete_message(searching_message)
        except:
            pass
        await update.message.reply_text("❌ مشکلی پیش اومد!")

# ساخت تصویر با توصیف
async def imagine(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ساخت تصویر با توصیف هنری"""
    if not context.args:
        await update.message.reply_text("🎨 مثال: /imagine یه گربه شیرین با کلاه جادویی")
        return
    
    description = " ".join(context.args)
    
    try:
        searching_message = await send_searching_animation(update)
        
        prompt = f"تو یه هنرمند بصری هستی. یه توصیف هنری زیبا از این صحنه بنویس: {description}"
        
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=[{"role": "user", "content": prompt}],
        )
        
        await delete_message(searching_message)
        
        # نمایش تصویر با فرمت زیبا
        await update.message.reply_text(
            f"🎨 <b>تصور هنری من از:</b> <i>{description}</i>\n\n"
            f"✨ {response}\n\n"
            f"💡 <i>نکته: این یه توصیف هنریه، نه تصویر واقعی</i>",
            parse_mode="HTML"
        )
        
    except Exception as e:
        logger.error(f"خطا در تصور تصویر: {e}")
        try:
            await delete_message(searching_message)
        except:
            pass
        await update.message.reply_text("❌ مشکلی پیش اومد!")

# تحلیل داده‌ها
async def data_analyzer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """تحلیل داده‌ها"""
    if not context.args:
        await update.message.reply_text("📈 مثال: /data تحلیل فروش ماهانه")
        return
    
    description = " ".join(context.args)
    
    try:
        searching_message = await send_searching_animation(update)
        
        prompt = f"روش‌های تحلیل داده برای {description} بگو"
        
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=[{"role": "user", "content": prompt}],
        )
        
        await delete_message(searching_message)
        
        await update.message.reply_text(
            f"📈 <b>تحلیل داده برای:</b> <i>{description}</i>\n\n"
            f"📊 {response}",
            parse_mode="HTML"
        )
        
    except Exception as e:
        logger.error(f"خطا در تحلیل داده: {e}")
        try:
            await delete_message(searching_message)
        except:
            pass
        await update.message.reply_text("❌ مشکلی پیش اومد!")

# نوشتن مقاله
async def article_writer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """نوشتن مقاله"""
    if not context.args:
        await update.message.reply_text("📝 مثال: /article فواید تمرین ورزشی")
        return
    
    topic = " ".join(context.args)
    
    try:
        searching_message = await send_searching_animation(update)
        
        prompt = f"یه مقاله 300 کلمه‌ای درباره {topic} بنویس"
        
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=[{"role": "user", "content": prompt}],
        )
        
        await delete_message(searching_message)
        
        await update.message.reply_text(
            f"📝 <b>مقاله درباره:</b> <i>{topic}</i>\n\n"
            f"{response}",
            parse_mode="HTML"
        )
        
    except Exception as e:
        logger.error(f"خطا در نوشتن مقاله: {e}")
        try:
            await delete_message(searching_message)
        except:
            pass
        await update.message.reply_text("❌ مشکلی پیش اومد!")

# تولید موسیقی (توصیف موسیقی)
async def music_generator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """تولید توصیف موسیقی"""
    if not context.args:
        await update.message.reply_text("🎵 مثال: /music موسیقی آرامش‌بخش برای مطالعه")
        return
    
    description = " ".join(context.args)
    
    try:
        searching_message = await send_searching_animation(update)
        
        prompt = f"یه توصیف موسیقی زیبا برای این موضوع بنویس: {description}"
        
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=[{"role": "user", "content": prompt}],
        )
        
        await delete_message(searching_message)
        
        await update.message.reply_text(
            f"🎵 <b>توصیف موسیقی برای:</b> <i>{description}</i>\n\n"
            f"🎼 {response}",
            parse_mode="HTML"
        )
        
    except Exception as e:
        logger.error(f"خطا در تولید موسیقی: {e}")
        try:
            await delete_message(searching_message)
        except:
            pass
        await update.message.reply_text("❌ مشکلی پیش اومد!")

# فال و طالع‌بینی
async def fortune_teller(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """فال و طالع‌بینی"""
    try:
        searching_message = await send_searching_animation(update)
        
        prompt = "یه فال جالب و انگیزشی بگو. فقط فال رو بگو، توضیح اضافی نده."
        
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=[{"role": "user", "content": prompt}],
        )
        
        await delete_message(searching_message)
        
        await update.message.reply_text(
            f"🔮 <b>فال امروز شما:</b>\n\n"
            f"✨ {response}",
            parse_mode="HTML"
        )
        
    except Exception as e:
        logger.error(f"خطا در فال: {e}")
        try:
            await delete_message(searching_message)
        except:
            pass
        await update.message.reply_text("❌ مشکلی پیش اومد!")

# تنظیمات کاربر
async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """تنظیمات کاربر"""
    user_id = str(update.effective_user.id)
    
    if user_id in users_data:
        user_info = users_data[user_id]
        # آمار امتیازات
        user_scores = scores_data.get(user_id, {})
        
        settings_text = f"""
⚙️ <b>تنظیمات شما:</b>

👤 <b>اطلاعات کاربری:</b>
نام: {user_info.get('first_name', 'نامشخص')}
نام کاربری: @{user_info.get('username', 'نامشخص')}
تاریخ عضویت: {user_info.get('join_date', 'نامشخص')[:10]}

📊 <b>آمار استفاده:</b>
تعداد کارها: {len(tasks_data.get(user_id, []))}
امتیاز کل: {user_scores.get('total', 0)}
امتیاز ریاضی: {user_scores.get('math', 0)}
امتیاز حدس: {user_scores.get('guess', 0)}
امتیاز آوایی: {user_scores.get('phonetic', 0)}
"""
    else:
        settings_text = "⚙️ <b>تنظیمات شما</b>\n(اطلاعات کاربری یافت نشد)"
    
    await update.message.reply_text(settings_text, parse_mode="HTML")

def main():
    """تابع اصلی با مدیریت بهتر خطاها"""
    print("🚀 بات کامل با رابط کاربری زیبا شروع به کار کرد!")
    print("✨ بدون نیاز به VPN یا کامپیوتر همیشه روشن")
    
    # بارگذاری داده‌ها
    load_data()
    
    try:
        app = Application.builder().token(BOT_TOKEN).build()
        
        # دستورات اصلی
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("menu", show_menu))
        app.add_handler(CommandHandler("help", help_command))
        app.add_handler(CommandHandler("character", character_chat))
        app.add_handler(CommandHandler("code", code_generator))
        app.add_handler(CommandHandler("translate", advanced_translate))
        app.add_handler(CommandHandler("summarize", summarize_text))
        app.add_handler(CommandHandler("spell", spell_check))
        app.add_handler(CommandHandler("story", story_generator))
        app.add_handler(CommandHandler("math", math_solver))
        app.add_handler(CommandHandler("mathgame", math_game_start))
        app.add_handler(CommandHandler("wordgame", word_game_start))
        app.add_handler(CommandHandler("dicegame", dice_game_start))
        app.add_handler(CommandHandler("guessgame", guess_game_start))
        app.add_handler(CommandHandler("phoneticgame", phonetic_game_start))
        app.add_handler(CommandHandler("addtask", add_task))
        app.add_handler(CommandHandler("tasks", list_tasks))
        app.add_handler(CommandHandler("idea", idea_generator))
        app.add_handler(CommandHandler("analyze", text_analyzer))
        app.add_handler(CommandHandler("post", social_content))
        app.add_handler(CommandHandler("imagine", imagine))
        app.add_handler(CommandHandler("data", data_analyzer))
        app.add_handler(CommandHandler("article", article_writer))
        app.add_handler(CommandHandler("music", music_generator))
        app.add_handler(CommandHandler("fortune", fortune_teller))
        app.add_handler(CommandHandler("settings", settings))
        
        # هندلر دکمه‌ها
        app.add_handler(CallbackQueryHandler(button_handler))
        
        # پیام‌های عادی
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_math_answer))
        # هندلرهای دیگر برای بازی‌ها
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_guess_number))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_phonetic_answer))
        
        print("✅ بات کاملاً آماده‌ست!")
        app.run_polling()
        
    except Exception as e:
        logger.error(f"خطا در راه‌اندازی بات: {e}")
        print(f"❌ خطا: {e}")

if __name__ == '__main__':
    main()