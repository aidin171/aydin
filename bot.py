import g4f
import asyncio
import logging
import random
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes

# تنظیمات لاگ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = "8319765501:AAEJ8_k-qas6VB6TYDdwOite1hQjaBlSs1w"

# اطلاعات ربات
BOT_INFO = """
🤖 <b>بات هوشمند g4f</b>

✨ <b>قابلیت‌های موجود:</b>
• 🧠 چت هوشمند با هر موضوع
• 🌍 ترجمه پیشرفته (/translate)
• 📚 خلاصه‌سازی متن (/summarize)
• 🧮 حل مسئله ریاضی (/math)
• 🎮 بازی حدس عدد (/guessgame)
• 📝 نوشتن مقاله (/article)
• 🔮 فال و طالع‌بینی (/fortune)
• 💡 دریافت پرامپت (/prompt)

💡 <b>نکات مهم:</b>
• بدون نیاز به VPN
• بدون نیاز به کامپیوتر همیشه روشن
• بدون نیاز به پول یا API Key

👨‍💻 <b>توسعه‌دهنده: آیدین موسوی</b>
"""

# ذخیره داده‌های کاربران
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
    await update.message.reply_text(BOT_INFO, parse_mode="HTML")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
📚 <b>راهنمای استفاده از بات</b>

🎯 <b>دستورات موجود:</b>
/start - اطلاعات ربات
/help - راهنمای استفاده
/translate [سبک] [زبان] [متن] - ترجمه پیشرفته
/summarize [متن] - خلاصه‌سازی
/math [مسئله] - حل ریاضی
/guessgame - بازی حدس عدد
/article [موضوع] - نوشتن مقاله
/fortune - فال و طالع‌بینی
/prompt [موضوع] - دریافت پرامپت

💡 <b>نکات:</b>
• برای چت عادی کافیه پیام بفرستی
• بات به سوالات قبلی هم جواب می‌ده
• همه قابلیت‌ها رایگان هستن
"""
    await update.message.reply_text(help_text, parse_mode="HTML")

# چت عادی با بهبود
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user_id = str(update.effective_user.id)
    
    try:
        searching_message = await send_searching_message(update)
        
        # مدیریت متناسب با پیام "سازنده‌ات کیه؟"
        if "سازنده" in user_message and ("کی" in user_message or "?" in user_message or "؟" in user_message):
            await delete_searching_message(searching_message)
            await update.message.reply_text("👨‍💻 سازنده من آیدین موسوی هست. یه برنامه‌نویس حرفه‌ای که من رو ساخته!")
            return
            
        # ساخت متن با توجه به مکالمه قبلی
        full_prompt = user_message
        if user_id in user_contexts:
            full_prompt = f"سوال قبلی: {user_contexts[user_id]}\nسوال فعلی: {user_message}"
        
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=[{"role": "user", "content": full_prompt}],
        )
        
        # ذخیره جواب برای استفاده بعدی
        user_contexts[user_id] = f"سوال: {user_message}\nجواب: {response}"
        
        await delete_searching_message(searching_message)
        await update.message.reply_text(response)
        
    except Exception as e:
        logger.error(f"خطا در چت: {e}")
        try:
            await delete_searching_message(searching_message)
        except:
            pass
        await update.message.reply_text("❌ مشکلی پیش اومد! دوباره تلاش کن.")

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

# بازی حدس عدد
async def guess_game_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # عدد تصادفی بین 1 تا 100
    secret_number = random.randint(1, 100)
    context.user_data['secret_number'] = secret_number
    context.user_data['guess_attempts'] = 0
    
    await update.message.reply_text("🎯 بازی حدس عدد:\nعددی بین 1 تا 100 حدس بزن!\n\nپاسختو بفرست!")

# چک کردن حدس عدد
async def check_guess_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # بررسی اینکه آیا کاربر در بازی حدس عدد هست یا نه
    if 'secret_number' in context.user_data:
        try:
            user_guess = int(update.message.text)
            secret_number = context.user_data['secret_number']
            attempts = context.user_data.get('guess_attempts', 0) + 1
            context.user_data['guess_attempts'] = attempts
            
            if user_guess == secret_number:
                await update.message.reply_text(
                    f"🎉 تبریک! عدد {secret_number} بود.\n"
                    f"تعداد تلاش‌ها: {attempts}"
                )
                # پاک کردن داده‌های بازی
                del context.user_data['secret_number']
                del context.user_data['guess_attempts']
                
            elif user_guess < secret_number:
                await update.message.reply_text(f"🔼 عدد بزرگتره! تلاش {attempts}")
            else:
                await update.message.reply_text(f"🔽 عدد کوچیکتره! تلاش {attempts}")
                
        except ValueError:
            await update.message.reply_text("لطفاً یه عدد بین 1 تا 100 بفرست!")
    else:
        # اگه در بازی نیست، بهش چت کن
        await chat(update, context)

# نوشتن مقاله
async def article_writer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("مثال: /article فواید تمرین ورزشی")
        return
    
    topic = " ".join(context.args)
    
    try:
        searching_message = await send_searching_message(update)
        
        prompt = f"یه مقاله 300 کلمه‌ای درباره {topic} بنویس"
        
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=[{"role": "user", "content": prompt}],
        )
        
        await delete_searching_message(searching_message)
        
        await update.message.reply_text(
            f"📝 <b>مقاله درباره:</b> <i>{topic}</i>\n\n"
            f"{response}",
            parse_mode="HTML"
        )
        
    except Exception as e:
        logger.error(f"خطا در نوشتن مقاله: {e}")
        try:
            await delete_searching_message(searching_message)
        except:
            pass
        await update.message.reply_text("❌ مشکلی پیش اومد!")

# فال و طالع‌بینی
async def fortune_teller(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        searching_message = await send_searching_message(update)
        
        prompt = "یه فال جالب و انگیزشی بگو. فقط فال رو بگو، توضیح اضافی نده."
        
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=[{"role": "user", "content": prompt}],
        )
        
        await delete_searching_message(searching_message)
        
        await update.message.reply_text(
            f"🔮 <b>فال امروز شما:</b>\n\n"
            f"✨ {response}",
            parse_mode="HTML"
        )
        
    except Exception as e:
        logger.error(f"خطا در فال: {e}")
        try:
            await delete_searching_message(searching_message)
        except:
            pass
        await update.message.reply_text("❌ مشکلی پیش اومد!")

# دریافت پرامپت
async def get_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("مثال: /prompt یه تصویر از گربه")
        return
    
    description = " ".join(context.args)
    
    try:
        searching_message = await send_searching_message(update)
        
        prompt = f"برای ایجاد یه تصویر با هوش مصنوعی، یه پرامپت عالی برای '{description}' بساز"
        
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=[{"role": "user", "content": prompt}],
        )
        
        await delete_searching_message(searching_message)
        
        await update.message.reply_text(
            f"🎯 <b>پرامپت برای:</b> <i>{description}</i>\n\n"
            f"```\n{response}\n```",
            parse_mode="HTML"
        )
        
    except Exception as e:
        logger.error(f"خطا در ایجاد پرامپت: {e}")
        try:
            await delete_searching_message(searching_message)
        except:
            pass
        await update.message.reply_text("❌ مشکلی پیش اومد!")

def main():
    print("🚀 بات شروع به کار کرد!")
    print("💡 بدون نیاز به VPN یا کامپیوتر همیشه روشن")
    
    try:
        app = Application.builder().token(BOT_TOKEN).build()
        
        # دستورات اصلی
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("help", help_command))
        app.add_handler(CommandHandler("translate", advanced_translate))
        app.add_handler(CommandHandler("summarize", summarize_text))
        app.add_handler(CommandHandler("math", math_solver))
        app.add_handler(CommandHandler("guessgame", guess_game_start))
        app.add_handler(CommandHandler("article", article_writer))
        app.add_handler(CommandHandler("fortune", fortune_teller))
        app.add_handler(CommandHandler("prompt", get_prompt))
        
        # پیام‌های عادی و چک کردن حدس عدد
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_guess_number))
        
        print("✅ بات کاملاً آماده‌ست!")
        app.run_polling()
    except Exception as e:
        logger.error(f"خطا در راه‌اندازی بات: {e}")
        print(f"❌ خطا: {e}")

if __name__ == '__main__':
    main()
