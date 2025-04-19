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
    if callback.data and callback.data.startswith('catalog_'):
        category_id = int(callback.data.split('_')[1])
        print(f"Выбрана категория: {category_id}")
        products = get_product_by_category(category_id)

        if products:
            for product in products:
                print(f"Обрабатываем продукт: {product[1]}")
                product_text = f"<b>{product[1]}</b>\n\n{product[2]}\nЦена: {product[3]} руб."
                product_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="В корзину", callback_data=f'add_to_cart_{product[0]}'), InlineKeyboardButton(text="Подробнее", callback_data=f'show_details_{product[0]}')]])
                try:
                    await callback.message.answer_photo(photo=product[4], caption=product_text, parse_mode="HTML", reply_markup=product_keyboard)
                except:
                    await callback.message.answer(text=product_text, parse_mode="HTML", reply_markup=product_keyboard)
        else:
            await callback.message.answer("В данный момент товаров нет.")
    else:
        await callback.message.answer("Неверный запрос.")
    await callback.answer()

@router.callback_query(F.data.startswith("show_details_"))
async def product_details(callback: CallbackQuery):
    if callback.data and callback.data.startswith('show_details_'):
        product_id = int(callback.data.split('_')[1])
        product = get_product_by_id(product_id)

        if product:
            product_text = f"<b>{product[1]}</b>\n\n{product[2]}\nЦена: {product[3]} руб."
            try:
                await callback.message.answer_photo(photo=product[4], caption=product_text, parse_mode="HTML")
            except:
                await callback.message.answer(text=product_text, parse_mode="HTML")
        else:
            await callback.message.answer("Товар не найден.")
    else:
        await callback.message.answer("Неверный запрос.")

    await callback.answer()