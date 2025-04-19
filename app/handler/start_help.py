from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart

import app.keybords as kb
from database import get_user

router = Router()

#Команда /start
@router.message(CommandStart())
async def cmd_start(message: Message):
    user_id = message.from_user.id
    user = get_user(user_id)

    if user:
        welcome_text = f"Добро пожаловать, {user[3]}! Рад снова видеть тебя.\n" \
                    f"Воспользуйся командой /help, чтобы узнать больше о моих возможностях."
        await message.answer(welcome_text, reply_markup=kb.main)
    else:
        welcome_text = f"Добро пожаловать! Я бот магазина полезного питания. Здесь ты можешь найти натуральные и полезные продукты для здорового образа жизни.\n\n" \
                    f"Пожалуйста, зарегистрируйтесь с помощью команды /register, чтобы полуячать персональные предложения.\n" \
                    f"Воспользуйся командой /help, чтобы узнать больше о моих возможностях."
        await message.answer(welcome_text)



#Команда /help
@router.message(Command('help'))
async def cmd_help(message: Message):
    help_text = """
    <b>Список доступных команд:</b>
    /start - Начать работу с ботом.
    /help - Получить справку по командам.
    /register - Зарегестрироваться в системе (для получения персональных предложений).
    /catalog - Просмотреть каталог товаров.
    /contacts - Связаться с оператором.
    """
    await message.answer(help_text, parse_mode="HTML")