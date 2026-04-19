import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart, Text
from config import BOT_TOKEN, PRIVATE_CHANNEL_ID
from models import async_session, User, Plan
from crud import get_user, add_user
from payments import create_payment, check_payment
from sqlalchemy.future import select
import datetime

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def main_menu(lang="RU"):
    if lang == "RU":
        buttons = [[KeyboardButton("Оплатить")],[KeyboardButton("Правила")],[KeyboardButton("Контакты")],[KeyboardButton("Сменить язык")]]
    else:
        buttons = [[KeyboardButton("Pay")],[KeyboardButton("Rules")],[KeyboardButton("Support")],[KeyboardButton("Change Language")]]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def tariff_buttons(lang="RU"):
    if lang == "RU":
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton("VIP - 30 дней", callback_data="plan_vip")],
            [InlineKeyboardButton("VIP+ - 30 дней + общение", callback_data="plan_vip_plus")]
        ])
    else:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton("VIP - 30 days", callback_data="plan_vip")],
            [InlineKeyboardButton("VIP+ - 30 days + chat", callback_data="plan_vip_plus")]
        ])

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Русский", callback_data="lang_RU")],
        [InlineKeyboardButton("English", callback_data="lang_EN")]
    ])
    await message.answer("Выберите язык / Choose language:", reply_markup=markup)

@dp.callback_query(Text(startswith="lang_"))
async def lang_choice(call: types.CallbackQuery):
    lang = call.data.split("_")[1]
    user = await get_user(call.from_user.id)
    if not user:
        user = await add_user(call.from_user.id, call.from_user.username, lang)
    else:
        user.language = lang
        async with async_session() as session:
            session.add(user)
            await session.commit()
    text = "Привет! Выберите тариф:" if lang == "RU" else "Hi! Choose a plan:"
    await call.message.edit_text(text, reply_markup=tariff_buttons(lang))
    await call.answer()

@dp.callback_query(Text(startswith="plan_"))
async def plan_choice(call: types.CallbackQuery):
    plan_type = call.data.split("_")[1]
    user = await get_user(call.from_user.id)
    if plan_type == "vip":
        plan_name = "VIP"; price_stars = 100
    else:
        plan_name = "VIP+"; price_stars = 200
    async with async_session() as session:
        result_plan = await session.execute(select(Plan).where(Plan.name==plan_name))
        plan = result_plan.scalars().first()
        if not plan:
            plan = Plan(name=plan_name, stars_price=price_stars, duration_days=30)
            session.add(plan)
            await session.commit()
        user.plan_id = plan.plan_id
        await session.commit()
    payment = await create_payment(user.user_id, plan_name, price_stars)
    payment_text = f"Тариф: {plan_name}\nСумма: {price_stars} ⭐\nАдрес: {payment.wallet_address}\nСрок: 15 мин"
    await call.message.edit_text(payment_text)
    await call.answer("Инструкция создана ✅")

@dp.message()
async def main_menu_handler(message: types.Message):
    user = await get_user(message.from_user.id)
    lang = user.language if user else "RU"
    await message.answer("Главное меню:", reply_markup=main_menu(lang))

@dp.message(Text(startswith="!check"))
async def check_payment_cmd(message: types.Message):
    tx_hash = message.text.split()[1]
    ok = await check_payment(tx_hash)
    if ok:
        await message.answer("Платеж подтвержден ✅")
        try:
            invite_link = await bot.create_chat_invite_link(PRIVATE_CHANNEL_ID, member_limit=1, expire_date=datetime.datetime.utcnow() + datetime.timedelta(days=30))
            await bot.send_message(message.from_user.id, f"Ссылка на канал: {invite_link.invite_link}")
        except Exception as e:
            await message.answer(f"Ошибка выдачи доступа: {e}")
    else:
        await message.answer("Платеж не найден ❌")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
