# keyboards.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💬 چت هوشمند"), KeyboardButton(text="📚 آموزش کد")],
        [KeyboardButton(text="📄 خلاصه"), KeyboardButton(text="🌐 ترجمه")],
        [KeyboardButton(text="➗ ریاضی"), KeyboardButton(text="🎲 بازی")],
        [KeyboardButton(text="🍀 فال"), KeyboardButton(text="📝 مقاله")],
        [KeyboardButton(text="🎯 پرامت"), KeyboardButton(text="ℹ️ راهنما")]
    ],
    resize_keyboard=True
)