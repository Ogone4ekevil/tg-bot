from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


catalog = KeyboardButton(text="Каталог")
contacts = KeyboardButton(text="Контакты")
about_us = KeyboardButton(text="О нас")

main = ReplyKeyboardMarkup(keyboard=[[catalog],
                                     [contacts]],
                            resize_keyboard=True,
                            input_field_placeholder='Выберите пункт меню...')

catalog_inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Суперфуды", callback_data='catalog_1')],
    [InlineKeyboardButton(text="Орехи и семечки", callback_data='catalog_2')],
    [InlineKeyboardButton(text="Мёд и масло", callback_data='catalog_3')],
    [InlineKeyboardButton(text="Смузи и соки", callback_data='catalog_4')],
    [InlineKeyboardButton(text="Полезные сладости", callback_data='catalog_5')]])

get_number = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отправить номер',
                                                           request_contact=True)]],
                                resize_keyboard=True)

def product_inline(product_id):
    buttons = [
        [InlineKeyboardButton(text="Подробнее", callback_data=f"show_details_{product_id}")],
        [InlineKeyboardButton(text="Добавить в корзину", callback_data=f"add_to_cart_product_{product_id}")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard