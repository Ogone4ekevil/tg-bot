import sqlite3
from datetime import datetime

import test_data

DATABASE_NAME = "BioMarket.db"

def create_db():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            img_url TEXT,
            FOREIGN KEY (category_id) REFERENCES categories (id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER NOT NULL UNIQUE,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            age INTEGER,
            phone_number TEXT,
            registration_date DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cart_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 1,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
    """)

    conn.commit()
    conn.close()

def get_categories():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    query = "SELECT id, name FROM categories"
    print(f"Запрос в БД: {query}")

    cursor.execute(query)
    categories = cursor.fetchall()

    print(f"Результат запроса: {categories}")

    conn.close()
    return categories

def get_product_by_category(category_id):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    query = "SELECT id, name, description, price, img_url FROM products WHERE category_id = ?"  # Запрос
    print(f"Запрос в БД: {query}, category_id={category_id}") # Выводим запрос и значение category_id

    cursor.execute(query, (category_id,))
    products = cursor.fetchall()

    print(f"Результат запроса: {products}") # Выводим результат запроса

    conn.close()
    return products

def save_user(user_data):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users (telegram_id, username, first_name, last_name, age, phone_number)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        user_data['telegram_id'],
        user_data['username'],
        user_data['first_name'],
        user_data['last_name'],
        user_data['age'],
        user_data['phone_number']
    ))

    conn.commit()
    conn.close()

def get_user(telegram_id):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
    user = cursor.fetchone()

    conn.close()
    return user

def get_product_by_id(product_id):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, description, price, img_url FROM products WHERE id = ?", (product_id,))
    product = cursor.fetchone()

    conn.close()
    return product

def fill_db_with_test_data():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    print("Начинаем заполнять базы данных данным...")

    # Заполняем таблицу categories
    for category in test_data.test_categories:
        cursor.execute("SELECT name FROM categories WHERE name = ?", (category[0],))
        if cursor.fetchone() is None:
            print(f"Добавляем категорию: {category}")
            cursor.execute("INSERT INTO categories (name, description) VALUES (?, ?)", category)
        else:
            print(f"Категория {category[0]} уже существует, пропускаем.")
    
    for product in test_data.test_products:
        cursor.execute("SELECT name FROM products WHERE name = ?", (product[1],))
        if cursor.fetchone() is None:
            print(f"Добавляем продукт: {product}")
            cursor.execute("""
                INSERT INTO products (category_id, name, description, price, img_url)
                VALUES(?, ?, ?, ?, ?)
            """, product)
        else:
            print(f"Продукт {product[1]} уже существует, пропускаем.")

    conn.commit()
    print("Закончим заполнение базы данных тестовыми данными.")
    conn.close()

def add_to_cart(user_id: int, product_id: int):
    print(f"add_to_cart: user_id = {user_id}, product_id = {product_id}")
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Проверяем, есть ли уже такой товар в корзине
    query = "SELECT quantity FROM cart_items WHERE user_id = ? AND product_id = ?"
    print(f"add_to_cart: query = {query}, user_id = {user_id}, product_id = {product_id}") # Добавили логирование
    cursor.execute(query, (user_id, product_id))
    existing_item = cursor.fetchone()

    if existing_item:
        # Если товар уже есть в корзине, увеличиваем количество
        quantity = existing_item[0] + 1
        query = "UPDATE cart_items SET quantity = ? WHERE user_id = ? AND product_id = ?"
        print(f"add_to_cart: query = {query}, quantity = {quantity}, user_id = {user_id}, product_id = {product_id}") # Добавили логирование
        cursor.execute(query, (quantity, user_id, product_id))
    else:
        # Если товара еще нет в корзине, добавляем его
        query = "INSERT INTO cart_items (user_id, product_id, quantity) VALUES (?, ?, ?)"
        print(f"add_to_cart: query = {query}, user_id = {user_id}, product_id = {product_id}, quantity = 1") # Добавили логирование
        cursor.execute(query, (user_id, product_id, 1))

    conn.commit()
    conn.close()

def get_cart_items(user_id: int):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT products.id, products.name, products.price, cart_items.quantity, products.img_url
        FROM cart_items
        JOIN products ON cart_items.product_id = products.id
        WHERE cart_items.user_id = ?
    """, (user_id,))
    cart_items = cursor.fetchall()

    conn.close()
    return cart_items

def remove_from_cart(user_id: int, product_id: int):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM cart_items WHERE user_id = ? AND product_id = ?", (user_id, product_id))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_db()
    print("База данных создана/проверена.")
    fill_db_with_test_data()