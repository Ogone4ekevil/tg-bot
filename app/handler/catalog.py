from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

import app.keybords as kb
from database import get_product_by_category, get_product_by_id

router = Router()

@router.message(F.text == 'Каталог')
async def catalog(message: Message):
    await message.answer("Выберите категорию товара", reply_markup=kb.catalog_inline)


@router.message(Command('catalog'))
async def cmd_catalog(message: Message):
    await message.answer("Выберите категорию товара", reply_markup=kb.catalog_inline)


@router.callback_query(F.data.startswith("catalog_"))
async def show_products(callback: CallbackQuery):
    print(f"Вызван хэндлер show_product с callback_{callback.data}")
    try:
        if callback.data and callback.data.startswith('catalog_'):
            category_id = int(callback.data.split('_')[1])
            print(f"Выбрана категория: {category_id}")
            products = get_product_by_category(category_id)

            if products:
                for product in products:
                    print(f"Обрабатываем продукт: {product[1]}")
                    product_text = f"<b>{product[1]}</b>\n\n{product[2]}\nЦена: {product[3]} руб."
                    # Используем kb.product_inline для создания клавиатуры
                    product_keyboard = kb.product_inline(product[0])
                    try:
                        await callback.message.answer_photo(photo=product[4], caption=product_text, parse_mode="HTML", reply_markup=product_keyboard)
                    except Exception as e:
                        print(f"Ошибка при отправке фото: {e}")
                        await callback.message.answer(text=product_text, parse_mode="HTML", reply_markup=product_keyboard)
                    await callback.answer()  # Добавили answer
                return  # Явный выход из цикла
            else:
                await callback.message.answer("В данный момент товаров нет.")
                await callback.answer()  # Добавили answer
                return  # Явный выход из функции

        else:
            await callback.message.answer("Неверный запрос.")
            await callback.answer()  # Добавили answer
            return  # Явный выход из функции
    except Exception as e:
        print(f"Ошибка в show_products: {e}")
        await callback.answer("Произошла ошибка.")  # Отправляем сообщение об ошибке пользователю


@router.callback_query(F.data.startswith("show_details_"))
async def product_details(callback: CallbackQuery):
    try:
        if callback.data and callback.data.startswith('show_details_'):
            product_id = int(callback.data.split('_')[1])
            product = get_product_by_id(product_id)

            if product:
                product_text = f"<b>{product[1]}</b>\n\n{product[2]}\nЦена: {product[3]} руб."
                try:
                    await callback.message.answer_photo(photo=product[4], caption=product_text, parse_mode="HTML")
                except Exception as e:
                    print(f"Ошибка при отправке фото: {e}")
                    await callback.message.answer(text=product_text, parse_mode="HTML")
            else:
                await callback.message.answer("Товар не найден.")

        else:
            await callback.message.answer("Неверный запрос.")
    except Exception as e:
        print(f"Ошибка в product_details: {e}")
        await callback.answer("Произошла ошибка.")
    finally:
        await callback.answer()