from aiogram import Router, F
from aiogram.types import CallbackQuery
from database import get_product_by_id

router = Router()

async def add_to_cart(user_id: int, product_id: int, cart: dict):
    """Функция для добавления товара в корзину пользователя."""
    product = get_product_by_id(product_id)
    if product:
        product_id, name, description, price, img_url = product
        product_data = {
            'product_id': product_id,
            'name': name,
            'quantity': 1,
            'price': price
        }

        if user_id in cart:
            # Проверяем, есть ли товар уже в корзине
            existing_product = next((item for item in cart[user_id] if item['product_id'] == product_id), None)
            if existing_product:
                # Если товар уже есть, увеличиваем его количество
                existing_product['quantity'] += 1
            else:
                # Если товара нет, добавляем его в корзину
                cart[user_id].append(product_data)
        else:
            # Если корзины для пользователя еще нет, создаем ее и добавляем товар
            cart[user_id] = [product_data]

        print(f"Товар {name} добавлен в корзину пользователя {user_id}")
    else:
        print(f"Товар с ID {product_id} не найден")

@router.callback_query(F.data.startswith("add_to_cart_"))
async def add_product_to_cart(callback: CallbackQuery):
    product_id = int(callback.data.split("_")[3])
    user_id = callback.from_user.id
    from main import cart #Импортируем cart здесь, чтобы избежать циклического импорта

    await add_to_cart(user_id, product_id, cart)
    await callback.answer("Товар добавлен в корзину!")