from aiogram import F, Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command


router = Router()

#Команда /contacts
@router.message(Command('contacts'))
async def cmd_contact(message: Message):
    contact_text = "<b>Свяжитесь с нами:</b>\n\n" \
                   "Телефон: +7 (927) 843-24-03\n" \
                   "Email: support@BioMarket.ru\n\n" \
                   "Напиши нам в Telegram:"
    contact_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Написать в Telegram", url="https://t.me/BioMarket_test")]])
    await message.answer(contact_text, reply_markup=contact_keyboard, parse_mode="HTML")

#Команда /contacts
@router.message(F.text == 'Контакты')
async def cmd_contact(message: Message):
    contact_text = "<b>Свяжитесь с нами:</b>\n\n" \
                   "Телефон: +7 (927) 843-24-03\n" \
                   "Email: support@BioMarket.ru\n\n" \
                   "Напиши нам в Telegram:"
    contact_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Написать в Telegram", url="https://t.me/BioMarket_test")]])
    await message.answer(contact_text, reply_markup=contact_keyboard, parse_mode="HTML")