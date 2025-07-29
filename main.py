# main.py
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
import asyncio
import os

# ماژول‌های داخلی
from config import TOKEN
from keyboards import main_menu
from modules.helpers import register_all_handlers

# ایجاد بات و دیسپچر
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "✨ به بات هوش مصنوعی ARTI خوش آمدی! ✨\n\n"
        "من یک ربات پیشرفته هستم که توسط **آیدین موسوی** ساخته شدم و می‌تونم بهت توی موارد زیر کمک کنم:\n\n"
        "💬 چت هوشمند — با GPT-4 و Claude\n"
        "📚 آموزش کدنویسی — پایتون، HTML، JS و...\n"
        "📄 خلاصه‌سازی — متن، لینک، PDF\n"
        "🌐 ترجمه — به انگلیسی، عربی، ترکی و...\n"
        "➗ حل مسائل ریاضی — گام به گام\n"
        "🎲 بازی — حدس عدد\n"
        "🍀 فال — روزانه و عاشقانه\n"
        "📝 نوشتن مقاله — در هر موضوعی\n"
        "🎯 دریافت پرامت — برای تولید تصویر یا متن\n"
        "ℹ️ راهنما — نحوه استفاده از بات\n\n"
        "همه‌ی قابلیت‌ها کاملاً فعال و بدون باگ هستند.\n"
        "فقط کافیه یک گزینه رو انتخاب کنی و شروع کنی!\n\n"
        "🧡 تم بات: نارنجی\n"
        "👨‍💻 سازنده: آیدین موسوی",
        reply_markup=main_menu
    )

# پاسخ به سوالات درباره سازنده
@dp.message(F.text.func(lambda text: any(q in text.lower() for q in ["سازنده", "تویی؟", "کی ساختت", "تو چی", "نام تو", "ساخته شدی", "شخصیت", "ساخته"])))
async def about_creator(message: types.Message):
    await message.answer("🤖 من توسط **آیدین موسوی** طراحی و ساخته شدم.\nاو توسعه‌دهنده‌ی این هوش مصنوعیه! 🧠🧡")

async def main():
    # ثبت همه هندلرها
    register_all_handlers(dp)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())