
import asyncio
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 511491720

dp = Dispatcher()
waiting_for_request = set()

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💻 Наши услуги")],
        [KeyboardButton(text="📝 Оставить заявку")],
        [KeyboardButton(text="ℹ️ О студии")],
    ],
    resize_keyboard=True,
)

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "⚡ XTOW STUDIO\n\n"
        "Welcome to our digital studio.\n"
        "We build Telegram bots, websites and automation tools.\n\n"
        "Choose an option below to explore our services.",
        reply_markup=keyboard,
    )

@dp.message(F.text == "💻 Наши услуги")
async def services(message: Message):
    await message.answer(
        "💻 XTOW STUDIO SERVICES\n\n"
        "🤖 Telegram Bots\n"
        "Custom bots, menus and client request systems.\n\n"
        "🌐 Website Development\n"
        "Modern, responsive websites for your project.\n\n"
        "⚙️ Automation\n"
        "Tools that simplify repetitive tasks.\n\n"
        "Choose «Оставить заявку» to tell us about your project."
    )

@dp.message(F.text == "📝 Оставить заявку")
async def request(message: Message):
    waiting_for_request.add(message.from_user.id)
    await message.answer(
        "📝 Расскажите о вашем проекте одним сообщением.\n\n"
        "Укажите, что нужно разработать и какие функции вам нужны."
    )


@dp.message(F.text == "ℹ️ О студии")
async def about(message: Message):
    await message.answer(
        "⚡ XTOW STUDIO\n\n"
        "We create digital solutions for businesses and individuals.\n"
        "Our focus: clean design, useful features and reliable code."
    )


@dp.message(
    lambda message: message.from_user is not None
    and message.from_user.id in waiting_for_request
)
async def receive_request(message: Message):
    waiting_for_request.discard(message.from_user.id)

    user = message.from_user
    username = f"@{user.username}" if user.username else "не указан"
    text = message.text or "[не текстовое сообщение]"

    await bot.send_message(
        ADMIN_ID,
        "📩 Новая заявка в Xtow Studio\n\n"
        f"От: {user.full_name}\n"
        f"Username: {username}\n"
        f"Telegram ID: {user.id}\n\n"
        f"Описание проекта:\n{text}"
    )

    await message.answer(
        "✅ Заявка отправлена! Мы рассмотрим её."
    )


@dp.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        "Use the menu to explore services or describe your project."
    )

async def main():
    global bot

    if not TOKEN:
        raise RuntimeError(
            "BOT_TOKEN is not set. Configure your bot token first."
        )

    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
