from aiogram import F, Router
from aiogram.types import Message, CallbackQuery

from database import add_to_cart, get_cart_items

router = Router()

@router.callback_query(F.data.startswith("add_to_cart_"))
async def add_to_cart(callback: CallbackQuery):
    print(f"add_to_cart: Вызван обработчик add_to_cart с callback_{callback.data}")
    try:
        product_id = int(callback.data.split('_')[1])
        user_id = callback.from_user.id
        print(f"add_to_cart: user_id = {user_id}, product_id = {product_id}")
        add_to_cart(user_id, product_id)
        await callback.answer(f"Товар {product_id} добавлен в корзину!")
    except Exception as e:
        print(f"add_to_cart: Ошибка при обработке callback_{e}")
        await callback.answer("Неверный запрос.")

@router.message(F.text == 'Корзина')
async def view_cart(message: Message):
    user_id = message.from_user.id
    cart_items = get_cart_items(user_id)
    if cart_items:
        cart_text = "<b>Ваша корзина:</b>\n\n"
        total_price = 0
        for item in cart_items:
            cart_text += f"{item[1]} - {item[3]} шт. - {item[2] * item[3]} руб.\n"
            total_price += item[2] * item[3]
        cart_text += f"\n<b>Итого: {total_price} руб.</b>"
        await message.answer(cart_text, parse_mode="HTML")
    else:
        await message.answer("Ваша корзина пуста.")