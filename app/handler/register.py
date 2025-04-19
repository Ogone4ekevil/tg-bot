from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import app.keybords as kb
from database import get_user, save_user

router = Router()

class Register(StatesGroup):
    age = State()
    number = State()

#Команда /register
@router.message(Command('register'))
async def register_age(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user = get_user(user_id)

    if user:
        await message.answer("Вы уже зарегистрированы!",
                             reply_markup=kb.main)
        await state.clear()
        return

    await message.answer('Введите ваш возраст')
    await state.set_state(Register.age)


#Добавление возраста
@router.message(Register.age)
async def register_get_age(message: Message, state: FSMContext):
    try:
        age = int(message.text)
    except ValueError:
        await message.answer("Возраст должен быть числом. Пожалуйста, введите возраст цифрами.")
        return
    
    if age < 16:
        await message.answer("К сожалению, вам должно быть не менее 16 лет для регистрации.\n\nПожалуйста, введите ваш возраст ещй раз.")
        return
    elif age > 100:
        await message.answer("Пожалуйста, введите более реалистичный возраст.\n\nПожалуйста, введите ваш возраст ещй раз.")
        return

    await state.update_data(age=age)
    await message.answer('Отправьте ваш номер телефона', reply_markup=kb.get_number)
    await state.set_state(Register.number)


#Добавление номера телефона через кнопку
@router.message(Register.number, F.contact)
async def register_number_contact(message: Message, state: FSMContext):
    phone_number = message.contact.phone_number
    await register_finish(message, state, phone_number)


#Добавление номера телефона через текст
@router.message(Register.number)
async def register_number_text(message: Message, state: FSMContext):
    if not (message.text.startswith('+') and message.text[1:].isdigit() and len(message.text) > 5) and not (message.text.isdigit() and len(message.text) > 5):
        await message.answer("Пожалуйста, введите корректный номер телефона, начиная с '+' или только цифры.")
        return

    phone_number = message.text
    await register_finish(message, state, phone_number)


async def register_finish(message: Message, state: FSMContext, phone_number: str):
    print(f"register_finish: phone_number = {phone_number}")
    data = await state.get_data()
    user_data = {
        'telegram_id': message.from_user.id,
        'username': message.from_user.username,
        'first_name': message.from_user.first_name,
        'last_name': message.from_user.last_name,
        'age': int(data['age']),
        'phone_number': phone_number
    }
    print(f"register_finish: user_data = {user_data}")

    save_user(user_data)

    await message.answer(
        f'Регистрация завершена!\n'
        f'Ваше имя: {user_data["first_name"]}\n'
        f'Ваш возраст: {user_data["age"]}\n'
        f'Номер: {phone_number}',
        reply_markup=kb.main
    )
    await state.clear()