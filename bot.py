import g4f
import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes, CallbackQueryHandler

# تنظیمات لاگ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = "8319765501:AAEJ8_k-qas6VB6TYDdwOite1hQjaBlSs1w"

# اطلاعات ربات
BOT_INFO = """
🤖 بات هوشمند g4f - نسخه کامل

✨ قابلیت‌های پیشرفته:
• 🧠 چت هوشمند با هر موضوع
• 🎭 چت با شخصیت‌های معروف (/character)
• 💻 تولید کد برنامه‌نویسی (/code)
• 🌍 ترجمه پیشرفته (/translate)
• 📚 خلاصه‌سازی متن (/summarize)
• 🔍 بررسی املای فارسی (/spell)
• 📖 تولید داستان (/story)
• 🧮 حل مسئله ریاضی (/math)
• 📋 مدیریت کارها (/addtask, /tasks)
• 🎮 بازی‌های ذهنی (/game)
• 💡 تولید ایده خلاقانه (/idea)
• 📊 تحلیل متن (/analyze)
• 📱 محتوای شبکه‌های اجتماعی (/post)

💡 بدون نیاز به:
• VPN
• کامپیوتر همیشه روشن
• پول یا API Key

توسعه‌دهنده: آسانسور
"""

# ذخیره داده‌های کاربران
user_tasks = {}
user_contexts = {}

# توابع کمکی
async def send_searching_message(update: Update) -> object:
    """ارسال پیام جست و جو و برگرداندن آبجکت پیام"""
    return await update.message.reply_text("🔍 در حال جست و جو...")

async def delete_searching_message(searching_message) -> None:
    """پاک کردن پیام جست و جو"""
    try:
        await searching_message.delete()
    except Exception as e:
        logger.warning(f"خطا در پاک کردن پیام جست و جو: {e}")

# دستورات اصلی
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(BOT_INFO)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
📚 راهنمای استفاده از بات:

دستورات اصلی:
/start - اطلاعات ربات
/help - راهنمای استفاده
/info - اطلاعات کاربری

دستورات تخصصی:
/character [شخصیت] [پیام] - چت با شخصیت معروف
/code [زبان] [توضیح] - تولید کد
/translate [سبک] [زبان] [متن] - ترجمه پیشرفته
/summarize [متن] - خلاصه‌سازی
/spell [متن] - بررسی املایی
/story [ژانر] [موضوع] - تولید داستان
/math [مسئله] - حل ریاضی
/addtask [کار] - اضافه کردن کار
/tasks - نمایش کارها
/game - بازی ذهنی
/idea [موضوع] - تولید ایده
/analyze [متن] - تحلیل متن
/post [پلتفرم] [موضوع] - محتوای اجتماعی
"""
    await update.message.reply_text(help_text)

# چت عادی با بهبود
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    
    try:
        searching_message = await send_searching_message(update)
        
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=[{"role": "user", "content": user_message}],
        )
        
        await delete_searching_message(searching_message)
        await update.message.reply_text(response)
        
    except Exception as e:
        logger.error(f"خطا در چت: {e}")
        try:
            await delete_searching_message(searching_message)
        except:
            pass
        await update.message.reply_text("❌ مشکلی پیش اومد! دوباره تلاش کن.")

# چت با شخصیت‌های معروف
async def character_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("مثال: /character einstein سلام دنیا")
        return
    
    character = context.args[0]
    message = " ".join(context.args[1:])
    
    try:
        searching_message = await send_searching_message(update)
        
        prompt = f"تو {character} هستی. به سوال من با دانش و سبک این شخصیت جواب بده: {message}"
        
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=[{"role": "user", "content": prompt}],
        )
        
        await delete_searching_message(searching_message)
        await update.message.reply_text(f"🎭 به عنوان {character}:\n\n{response}")
        
    except Exception as e:
        logger.error(f"خطا در چت با شخصیت: {e}")
        try:
            await delete_searching_message(searching_message)
        except:
            pass
        await update.message.reply_text("❌ مشکلی پیش اومد!")

# تولید کد برنامه‌نویسی
async def code_generator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("مثال: /code python تابع فیبوناچی")
        return
    
    request = " ".join(context.args)
    
    try:
        searching_message = await send_searching_message(update)
        
        prompt = f"فقط کد رو بنویس، بدون توضیح. {request}"
        
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=[{"role": "user", "content": prompt}],
        )
        
        await delete_searching_message(searching_message)
        await update.message.reply_text(f"💻 کد درخواستی:\n```\n{response}\n```", parse_mode="Markdown")
        
    except Exception as e:
        logger.error(f"خطا در تولید کد: {e}")
        try:
            await delete_searching_message(searching_message)
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
        searching_message = await send_searching_message(update)
        
        prompt = f"این متن رو به سبک {style} به {target_lang} ترجمه کن: {text}"
        
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=[{"role": "user", "content": prompt}],
        )
        
        await delete_searching_message(searching_message)
        await update.message.reply_text(f"🌍 ترجمه ({style} به {target_lang}):\n{response}")
        
    except Exception as e:
        logger.error(f"خطا در ترجمه: {e}")
        try:
            await delete_searching_message(searching_message)
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
        searching_message = await send_searching_message(update)
        
        prompt = f"متن رو به صورت خلاصه و مفید خلاصه کن: {text}"
        
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=[{"role": "user", "content": prompt}],
        )
        
        await delete_searching_message(searching_message)
        await update.message.reply_text(f"📚 خلاصه:\n{response}")
        
    except Exception as e:
        logger.error(f"خطا در خلاصه‌سازی: {e}")
        try:
            await delete_searching_message(searching_message)
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
        searching_message = await send_searching_message(update)
        
        prompt = f"فقط متن اصلاح شده رو بنویس، بدون توضیح اضافی: {text}"
        
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=[{"role": "user", "content": prompt}],
        )
        
        await delete_searching_message(searching_message)
        await update.message.reply_text(f"🔍 اصلاح شده:\n{response}")
        
    except Exception as e:
        logger.error(f"خطا در بررسی املایی: {e}")
        try:
            await delete_searching_message(searching_message)
        except:
            pass
        await update.message.reply_text("❌ مشکلی پیش اومد!")

# تولید داستان
async def story_generator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    genre = context.args[0] if context.args else "عمومی"
    topic = " ".join(context.args[1:]) if len(context.args) > 1 else "ماجراجویی"
    
    try:
        searching_message = await send_searching_message(update)
        
        prompt = f"یه داستان کوتاه و جذاب در ژانر {genre} درباره {topic} بنویس"
        
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=[{"role": "user", "content": prompt}],
        )
        
        await delete_searching_message(searching_message)
        await update.message.reply_text(f"📖 داستان ({genre} - {topic}):\n{response}")
        
    except Exception as e:
        logger.error(f"خطا در تولید داستان: {e}")
        try:
            await delete_searching_message(searching_message)
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
        searching_message = await send_searching_message(update)
        
        prompt = f"تو یه استاد ریاضی هستی. مسئله رو حل کن و راه حل رو توضیح بده: {problem}"
        
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=[{"role": "user", "content": prompt}],
        )
        
        await delete_searching_message(searching_message)
        await update.message.reply_text(f"🧮 حل مسئله:\n{response}")
        
    except Exception as e:
        logger.error(f"خطا در حل مسئله: {e}")
        try:
            await delete_searching_message(searching_message)
        except:
            pass
        await update.message.reply_text("❌ مشکلی پیش اومد!")

# مدیریت کارها
async def add_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    task = " ".join(context.args)
    
    if not task:
        await update.message.reply_text("مثال: /addtask خرید نان")
        return
    
    if user_id not in user_tasks:
        user_tasks[user_id] = []
    
    user_tasks[user_id].append(task)
    await update.message.reply_text(f"✅ کار اضافه شد: {task}")

async def list_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id in user_tasks and user_tasks[user_id]:
        tasks = "\n".join([f"{i+1}. {task}" for i, task in enumerate(user_tasks[user_id])])
        await update.message.reply_text(f"📋 لیست کارها:\n{tasks}")
    else:
        await update.message.reply_text("کاری نداری! 😊")

# بازی‌های ذهنی
async def word_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        searching_message = await send_searching_message(update)
        
        prompt = "یه معما ساده و جالب بگو. فقط سوال رو بپرس، جواب رو نگو."
        
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=[{"role": "user", "content": prompt}],
        )
        
        await delete_searching_message(searching_message)
        await update.message.reply_text(f"🎮 معما:\n{response}")
        
    except Exception as e:
        logger.error(f"خطا در تولید معما: {e}")
        try:
            await delete_searching_message(searching_message)
        except:
            pass
        await update.message.reply_text("❌ مشکلی پیش اومد!")

# تولید ایده خلاقانه
async def idea_generator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topic = " ".join(context.args) if context.args else "کسب‌وکار"
    
    try:
        searching_message = await send_searching_message(update)
        
        prompt = f"۵ ایده خلاقانه درباره {topic} بده"
        
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=[{"role": "user", "content": prompt}],
        )
        
        await delete_searching_message(searching_message)
        await update.message.reply_text(f"💡 ایده‌های {topic}:\n{response}")
        
    except Exception as e:
        logger.error(f"خطا در تولید ایده: {e}")
        try:
            await delete_searching_message(searching_message)
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
        searching_message = await send_searching_message(update)
        
        prompt = f"این متن رو از نظر احساسات، سبک نوشتار و کلمات کلیدی تحلیل کن: {text}"
        
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=[{"role": "user", "content": prompt}],
        )
        
        await delete_searching_message(searching_message)
        await update.message.reply_text(f"📊 تحلیل متن:\n{response}")
        
    except Exception as e:
        logger.error(f"خطا در تحلیل متن: {e}")
        try:
            await delete_searching_message(searching_message)
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
        searching_message = await send_searching_message(update)
        
        prompt = f"یه پست جذاب برای {platform} درباره {topic} بنویس"
        
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=[{"role": "user", "content": prompt}],
        )
        
        await delete_searching_message(searching_message)
        await update.message.reply_text(f"📱 پست برای {platform}:\n{response}")
        
    except Exception as e:
        logger.error(f"خطا در تولید محتوای اجتماعی: {e}")
        try:
            await delete_searching_message(searching_message)
        except:
            pass
        await update.message.reply_text("❌ مشکلی پیش اومد!")

def main():
    print("🚀 بات کامل با همه قابلیت‌ها شروع به کار کرد!")
    print("💡 بدون نیاز به VPN یا کامپیوتر همیشه روشن")
    
    try:
        app = Application.builder().token(BOT_TOKEN).build()
        
        # دستورات اصلی
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("help", help_command))
        app.add_handler(CommandHandler("character", character_chat))
        app.add_handler(CommandHandler("code", code_generator))
        app.add_handler(CommandHandler("translate", advanced_translate))
        app.add_handler(CommandHandler("summarize", summarize_text))
        app.add_handler(CommandHandler("spell", spell_check))
        app.add_handler(CommandHandler("story", story_generator))
        app.add_handler(CommandHandler("math", math_solver))
        app.add_handler(CommandHandler("addtask", add_task))
        app.add_handler(CommandHandler("tasks", list_tasks))
        app.add_handler(CommandHandler("game", word_game))
        app.add_handler(CommandHandler("idea", idea_generator))
        app.add_handler(CommandHandler("analyze", text_analyzer))
        app.add_handler(CommandHandler("post", social_content))
        
        # پیام‌های عادی
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
        
        print("✅ بات کاملاً آماده‌ست!")
        app.run_polling()
        
    except Exception as e:
        logger.error(f"خطا در راه‌اندازی بات: {e}")
        print(f"❌ خطا: {e}")

if __name__ == '__main__':
    main()