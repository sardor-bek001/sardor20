# ==========================================
# Tech Store UZ Bot - Kengaytirilgan Versiya
# 10 ta yangi funksiya bilan
# ==========================================

import telebot
from telebot import types
import sqlite3
import os
import logging
import sys

# ============ KONFIGURATSIYA ============

BOT_TOKEN = "8771796667:AAHv60OXYci_M8sOm-dwcWY9XQ3-E3hScC8"
ADMIN_ID = 466638794
BOT_NAME = "Tech Store UZ"
CURRENCY = "so'm"

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

# ============ LUG'AT (TRANSLATIONS) ============

TEXTS = {
    "uz": {
        "welcome": "🏪 <b>{}</b> ga xush kelibsiz!\n\nIltimos, tilni tanlang / Пожалуйста, выберите язык:",
        "main_menu": "🏠 Asosiy menyu",
        "btn_catalog": "🛍 Katalog",
        "btn_cart": "🛒 Savatcha",
        "btn_wishlist": "⭐ Sevimlilar",
        "btn_sales": "🏷 Aksiyalar",
        "btn_search": "🔍 Qidiruv",
        "btn_referral": "👥 Do'stlarni taklif qilish",
        "btn_settings": "⚙️ Tilni o'zgartirish",
        "btn_orders": "📦 Buyurtmalarim",
        "search_prompt": "🔍 Qidirmoqchi bo'lgan mahsulot nomini yozing:",
        "search_not_found": "😔 Hech narsa topilmadi.",
        "search_results": "🔍 Qidiruv natijalari:",
        "cart_empty": "🛒 Savatchangiz bo'sh.",
        "cart_content": "🛒 <b>Savatchangizda:</b>\n\n",
        "cart_total": "\n💰 <b>Jami:</b> {} {}",
        "btn_checkout": "🛍 Buyurtma berish",
        "btn_clear_cart": "🗑 Savatchani tozalash",
        "checkout_phone": "📱 Telefon raqamingizni yuboring (Masalan: +998901234567) yoxud tugmani bosing:",
        "checkout_payment": "💳 To'lov usulini tanlang:",
        "payment_cash": "💵 Naqd pul",
        "payment_click": "🔵 Click",
        "payment_payme": "🟢 Payme",
        "payment_uzum": "🟣 Uzum",
        "order_success": "✅ <b>Buyurtmangiz qabul qilindi!</b>\nBuyurtma raqami: #{}\nTo'lov usuli: <b>{}</b>\n\nOperatorlarimiz tez orada bog'lanadi.",
        "wishlist_empty": "⭐ Sevimlilar ro'yxati bo'sh.",
        "added_to_cart": "✅ Savatchaga qo'shildi!",
        "added_to_wishlist": "❤️ Sevimlilarga qo'shildi!",
        "removed_from_wishlist": "💔 Sevimlilardan o'chirildi!",
        "referral_text": "👥 <b>Do'stlarni taklif qilish</b>\n\nSizning taklif havolangiz:\n<code>{}</code>\n\nSizning balansingiz: <b>{} {}</b>\n\n<i>Har bir do'stingiz uchun 5000 so'm bonus beriladi!</i>",
        "rate_product": "⭐ Baholash:",
        "thank_you_rating": "✅ Bahoingiz uchun rahmat!",
        "admin_menu": "🔐 Admin panel",
        "btn_broadcast": "📢 Xabar yuborish (Broadcast)",
        "broadcast_prompt": "📢 Barcha foydalanuvchilarga yuboriladigan xabarni yozing yoki rasm yuboring. Bekor qilish uchun /cancel.",
        "broadcast_done": "✅ Xabar yuborildi!",
        "choose_category": "📂 Kategoriyani tanlang:",
        "choose_product": "🔽 Mahsulotni tanlang:",
        "product_info": "📦 <b>{}</b>\n\n📝 {}\n\n💰 Narxi: {} {}\n⭐ Reyting: {} ({} ta baho)",
        "product_sale": "🏷 <b>Chegirma!</b>\nEski narx: <s>{} {}</s>\nYangi narx: {} {}",
        "btn_back": "⬅️ Orqaga",
        "btn_add_cart": "🛒 Savatchaga qo'shish",
        "btn_add_wishlist": "❤️ Sevimlilarga",
        "btn_remove_wishlist": "💔 Sevimlilardan olish",
        "btn_cancel": "❌ Bekor qilish",
        "btn_send_phone": "📱 Telefon raqam yuborish",
        "lang_changed": "✅ Til o'zgartirildi!",
        "sales_title": "🏷 <b>Hozirgi Aksiyalar:</b>\n"
    },
    "ru": {
        "welcome": "🏪 Добро пожаловать в <b>{}</b>!\n\nIltimos, tilni tanlang / Пожалуйста, выберите язык:",
        "main_menu": "🏠 Главное меню",
        "btn_catalog": "🛍 Каталог",
        "btn_cart": "🛒 Корзина",
        "btn_wishlist": "⭐ Избранное",
        "btn_sales": "🏷 Акции",
        "btn_search": "🔍 Поиск",
        "btn_referral": "👥 Пригласить друзей",
        "btn_settings": "⚙️ Изменить язык",
        "btn_orders": "📦 Мои заказы",
        "search_prompt": "🔍 Напишите название товара для поиска:",
        "search_not_found": "😔 Ничего не найдено.",
        "search_results": "🔍 Результаты поиска:",
        "cart_empty": "🛒 Ваша корзина пуста.",
        "cart_content": "🛒 <b>В корзине:</b>\n\n",
        "cart_total": "\n💰 <b>Итого:</b> {} {}",
        "btn_checkout": "🛍 Оформить заказ",
        "btn_clear_cart": "🗑 Очистить корзину",
        "checkout_phone": "📱 Отправьте ваш номер телефона (Например: +998901234567) или нажмите кнопку:",
        "checkout_payment": "💳 Выберите способ оплаты:",
        "payment_cash": "💵 Наличные",
        "payment_click": "🔵 Click",
        "payment_payme": "🟢 Payme",
        "payment_uzum": "🟣 Uzum",
        "order_success": "✅ <b>Ваш заказ принят!</b>\nНомер заказа: #{}\nСпособ оплаты: <b>{}</b>\n\nНаши операторы свяжутся с вами в ближайшее время.",
        "wishlist_empty": "⭐ Список избранного пуст.",
        "added_to_cart": "✅ Добавлено в корзину!",
        "added_to_wishlist": "❤️ Добавлено в избранное!",
        "removed_from_wishlist": "💔 Удалено из избранного!",
        "referral_text": "👥 <b>Пригласить друзей</b>\n\nВаша ссылка:\n<code>{}</code>\n\nВаш баланс: <b>{} {}</b>\n\n<i>За каждого друга вы получаете бонус 5000 сум!</i>",
        "rate_product": "⭐ Оценить:",
        "thank_you_rating": "✅ Спасибо за оценку!",
        "admin_menu": "🔐 Админ панель",
        "btn_broadcast": "📢 Рассылка (Broadcast)",
        "broadcast_prompt": "📢 Напишите сообщение для рассылки всем пользователям или отправьте фото. Для отмены введите /cancel.",
        "broadcast_done": "✅ Рассылка завершена!",
        "choose_category": "📂 Выберите категорию:",
        "choose_product": "🔽 Выберите товар:",
        "product_info": "📦 <b>{}</b>\n\n📝 {}\n\n💰 Цена: {} {}\n⭐ Рейтинг: {} ({} оценок)",
        "product_sale": "🏷 <b>Скидка!</b>\nСтарая цена: <s>{} {}</s>\nНовая цена: {} {}",
        "btn_back": "⬅️ Назад",
        "btn_add_cart": "🛒 В корзину",
        "btn_add_wishlist": "❤️ В избранное",
        "btn_remove_wishlist": "💔 Из избранного",
        "btn_cancel": "❌ Отмена",
        "btn_send_phone": "📱 Отправить контакт",
        "lang_changed": "✅ Язык изменен!",
        "sales_title": "🏷 <b>Текущие акции:</b>\n"
    }
}

user_states = {}  # {user_id: {"state": "...", "data": {}}}

# ============ MA'LUMOTLAR BAZASI ============

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tech_store.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        fullname TEXT,
        username TEXT,
        phone TEXT,
        language TEXT DEFAULT 'uz',
        referrer_id INTEGER,
        balance INTEGER DEFAULT 0,
        registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name_uz TEXT NOT NULL,
        name_ru TEXT NOT NULL,
        emoji TEXT DEFAULT '📦'
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_id INTEGER NOT NULL,
        name_uz TEXT NOT NULL,
        name_ru TEXT NOT NULL,
        desc_uz TEXT,
        desc_ru TEXT,
        price INTEGER NOT NULL,
        old_price INTEGER,
        photo_url TEXT,
        rating_sum INTEGER DEFAULT 0,
        rating_count INTEGER DEFAULT 0,
        in_stock INTEGER DEFAULT 1,
        FOREIGN KEY (category_id) REFERENCES categories(id)
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS cart (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER DEFAULT 1,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (product_id) REFERENCES products(id)
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS wishlist (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        UNIQUE(user_id, product_id)
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS ratings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        score INTEGER NOT NULL,
        UNIQUE(user_id, product_id)
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        phone TEXT,
        payment_method TEXT,
        total_price INTEGER NOT NULL,
        status TEXT DEFAULT 'yangi',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        price INTEGER NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders(id)
    )""")

    conn.commit()
    conn.close()

def add_sample_data():
    conn = get_db()
    c = conn.cursor()
    if c.execute("SELECT COUNT(*) FROM categories").fetchone()[0] > 0:
        conn.close()
        return

    categories = [
        ("📱 Smartfonlar", "📱 Смартфоны", "📱"),
        ("💻 Noutbuklar", "💻 Ноутбуки", "💻"),
        ("🎧 Aksessuarlar", "🎧 Аксессуары", "🎧"),
    ]
    c.executemany("INSERT INTO categories (name_uz, name_ru, emoji) VALUES (?, ?, ?)", categories)

    products = [
        (1, "iPhone 15 Pro Max", "iPhone 15 Pro Max (RU)", "256GB xotira, 48MP kamera", "256ГБ память, 48МП камера", 14500000, 15000000, "https://images.uzum.uz/cl4d4il6sfhvcppsflfg/original.jpg"),
        (1, "Samsung Galaxy S24 Ultra", "Samsung Galaxy S24 Ultra (RU)", "Snapdragon 8 Gen 3, 200MP", "Snapdragon 8 Gen 3, 200МП", 13800000, None, "https://images.uzum.uz/cnqbsm7i3rtms91fclvg/original.jpg"),
        (2, "MacBook Air M3", "MacBook Air M3 (RU)", "Apple M3 chip, 13.6 dyuym", "Чип Apple M3, 13.6 дюйм", 15500000, 16000000, "https://images.uzum.uz/cos5363i3rtteup85t80/original.jpg"),
        (3, "AirPods Pro 2", "AirPods Pro 2 (RU)", "Aktiv shovqin bekor qilish", "Активное шумоподавление", 2800000, None, "https://images.uzum.uz/cm399t3i3rtms90ss2t0/original.jpg")
    ]
    c.executemany("INSERT INTO products (category_id, name_uz, name_ru, desc_uz, desc_ru, price, old_price, photo_url) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", products)

    conn.commit()
    conn.close()
    logger.info("Namuna ma'lumotlar qo'shildi!")

def format_price(price):
    return f"{price:,}".replace(",", " ")

def get_lang(user_id):
    conn = get_db()
    row = conn.execute("SELECT language FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return row["language"] if row else "uz"

def t(user_id, key, *args):
    lang = get_lang(user_id)
    text = TEXTS.get(lang, TEXTS["uz"]).get(key, key)
    if args:
        return text.format(*args)
    return text

# ============ KEYBOARDS ============

def lang_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(
        types.InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="lang_uz"),
        types.InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")
    )
    return kb

def main_menu_kb(user_id):
    lang = get_lang(user_id)
    texts = TEXTS[lang]
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add(
        types.KeyboardButton(texts["btn_catalog"]),
        types.KeyboardButton(texts["btn_cart"]),
        types.KeyboardButton(texts["btn_sales"]),
        types.KeyboardButton(texts["btn_search"]),
        types.KeyboardButton(texts["btn_wishlist"]),
        types.KeyboardButton(texts["btn_orders"]),
        types.KeyboardButton(texts["btn_referral"]),
        types.KeyboardButton(texts["btn_settings"])
    )
    return kb

def cancel_kb(user_id):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(types.KeyboardButton(t(user_id, "btn_cancel")))
    return kb

def phone_kb(user_id):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(types.KeyboardButton(t(user_id, "btn_send_phone"), request_contact=True))
    kb.add(types.KeyboardButton(t(user_id, "btn_cancel")))
    return kb

def payment_kb(user_id):
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton(t(user_id, "payment_cash"), callback_data="pay_cash"),
        types.InlineKeyboardButton(t(user_id, "payment_click"), callback_data="pay_click"),
        types.InlineKeyboardButton(t(user_id, "payment_payme"), callback_data="pay_payme"),
        types.InlineKeyboardButton(t(user_id, "payment_uzum"), callback_data="pay_uzum")
    )
    return kb

def categories_inline_kb(user_id):
    kb = types.InlineKeyboardMarkup(row_width=1)
    conn = get_db()
    cats = conn.execute("SELECT * FROM categories").fetchall()
    conn.close()
    lang = get_lang(user_id)
    name_col = f"name_{lang}"
    for cat in cats:
        kb.add(types.InlineKeyboardButton(text=f"{cat['emoji']} {cat[name_col]}", callback_data=f"cat_{cat['id']}"))
    return kb

def products_inline_kb(user_id, category_id=None, is_sale=False, search_query=None):
    kb = types.InlineKeyboardMarkup(row_width=1)
    conn = get_db()
    lang = get_lang(user_id)
    name_col = f"name_{lang}"
    
    if category_id:
        prods = conn.execute(f"SELECT * FROM products WHERE category_id = ? AND in_stock = 1", (category_id,)).fetchall()
    elif is_sale:
        prods = conn.execute(f"SELECT * FROM products WHERE old_price IS NOT NULL AND in_stock = 1").fetchall()
    elif search_query:
        query = f"%{search_query}%"
        prods = conn.execute(f"SELECT * FROM products WHERE (name_uz LIKE ? OR name_ru LIKE ?) AND in_stock = 1", (query, query)).fetchall()
    else:
        prods = []
    
    conn.close()
    
    for p in prods:
        price_text = format_price(p['price'])
        kb.add(types.InlineKeyboardButton(text=f"{p[name_col]} — {price_text} {CURRENCY}", callback_data=f"prod_{p['id']}"))
    
    if category_id or is_sale:
        kb.add(types.InlineKeyboardButton(text=t(user_id, "btn_back"), callback_data="back_cats"))
    return kb, len(prods)

def product_detail_kb(user_id, product_id, category_id):
    kb = types.InlineKeyboardMarkup(row_width=2)
    
    conn = get_db()
    in_wishlist = conn.execute("SELECT 1 FROM wishlist WHERE user_id = ? AND product_id = ?", (user_id, product_id)).fetchone()
    conn.close()
    
    wish_text = t(user_id, "btn_remove_wishlist") if in_wishlist else t(user_id, "btn_add_wishlist")
    
    kb.add(types.InlineKeyboardButton(text=t(user_id, "btn_add_cart"), callback_data=f"addcart_{product_id}"))
    kb.add(types.InlineKeyboardButton(text=wish_text, callback_data=f"wish_{product_id}"))
    
    kb.add(
        types.InlineKeyboardButton("⭐ 1", callback_data=f"rate_{product_id}_1"),
        types.InlineKeyboardButton("⭐ 2", callback_data=f"rate_{product_id}_2"),
        types.InlineKeyboardButton("⭐ 3", callback_data=f"rate_{product_id}_3"),
        types.InlineKeyboardButton("⭐ 4", callback_data=f"rate_{product_id}_4"),
        types.InlineKeyboardButton("⭐ 5", callback_data=f"rate_{product_id}_5")
    )
    
    kb.add(types.InlineKeyboardButton(text=t(user_id, "btn_back"), callback_data=f"cat_{category_id}"))
    return kb

def cart_kb(user_id):
    kb = types.InlineKeyboardMarkup(row_width=3)
    conn = get_db()
    items = conn.execute("SELECT c.id, p.name_uz, p.name_ru, c.quantity, c.product_id FROM cart c JOIN products p ON c.product_id = p.id WHERE c.user_id = ?", (user_id,)).fetchall()
    conn.close()
    
    lang = get_lang(user_id)
    name_col = f"name_{lang}"
    
    for item in items:
        kb.add(
            types.InlineKeyboardButton("➖", callback_data=f"cartminus_{item['product_id']}"),
            types.InlineKeyboardButton(f"{item[name_col]} ({item['quantity']}x)", callback_data="none"),
            types.InlineKeyboardButton("➕", callback_data=f"cartplus_{item['product_id']}")
        )
    
    if items:
        kb.row(
            types.InlineKeyboardButton(t(user_id, "btn_clear_cart"), callback_data="cart_clear"),
            types.InlineKeyboardButton(t(user_id, "btn_checkout"), callback_data="cart_checkout")
        )
    return kb

def admin_menu_kb():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(types.KeyboardButton("📊 Statistika"), types.KeyboardButton("📋 Buyurtmalar"))
    kb.row(types.KeyboardButton("📢 Xabar yuborish"), types.KeyboardButton("🏠 Asosiy menyu"))
    return kb


# ============ COMMANDS ============

@bot.message_handler(commands=["start"])
def cmd_start(message):
    referrer_id = None
    args = message.text.split()
    if len(args) > 1 and args[1].startswith("ref_"):
        try:
            referrer_id = int(args[1].split("_")[1])
            if referrer_id == message.from_user.id:
                referrer_id = None
        except:
            pass

    conn = get_db()
    user = conn.execute("SELECT id FROM users WHERE id = ?", (message.from_user.id,)).fetchone()
    if not user:
        conn.execute("INSERT INTO users (id, fullname, username, referrer_id) VALUES (?, ?, ?, ?)",
                     (message.from_user.id, message.from_user.full_name, message.from_user.username, referrer_id))
        if referrer_id:
            conn.execute("UPDATE users SET balance = balance + 5000 WHERE id = ?", (referrer_id,))
            try:
                bot.send_message(referrer_id, f"🎉 Yangi do'stingiz botga qo'shildi! Balansingizga 5000 so'm qo'shildi.")
            except: pass
    conn.commit()
    conn.close()

    bot.send_message(message.chat.id, TEXTS["uz"]["welcome"].format(BOT_NAME), reply_markup=lang_kb())

@bot.callback_query_handler(func=lambda c: c.data.startswith("lang_"))
def set_language(call):
    lang = call.data.split("_")[1]
    conn = get_db()
    conn.execute("UPDATE users SET language = ? WHERE id = ?", (lang, call.from_user.id))
    conn.commit()
    conn.close()
    
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.send_message(call.message.chat.id, t(call.from_user.id, "main_menu"), reply_markup=main_menu_kb(call.from_user.id))


@bot.message_handler(commands=["admin"])
def cmd_admin(message):
    if message.from_user.id != ADMIN_ID:
        return
    bot.send_message(message.chat.id, "🔐 <b>Admin panel</b>", reply_markup=admin_menu_kb())


# ============ MENU HANDLERS ============

@bot.message_handler(func=lambda m: m.text in [TEXTS["uz"]["btn_catalog"], TEXTS["ru"]["btn_catalog"]])
def menu_catalog(message):
    bot.send_message(message.chat.id, t(message.from_user.id, "choose_category"), reply_markup=categories_inline_kb(message.from_user.id))

@bot.message_handler(func=lambda m: m.text in [TEXTS["uz"]["btn_sales"], TEXTS["ru"]["btn_sales"]])
def menu_sales(message):
    kb, count = products_inline_kb(message.from_user.id, is_sale=True)
    if count == 0:
        bot.send_message(message.chat.id, t(message.from_user.id, "search_not_found"))
        return
    bot.send_message(message.chat.id, t(message.from_user.id, "sales_title"), reply_markup=kb)

@bot.message_handler(func=lambda m: m.text in [TEXTS["uz"]["btn_settings"], TEXTS["ru"]["btn_settings"]])
def menu_settings(message):
    bot.send_message(message.chat.id, "🇺🇿 Tilni tanlang / 🇷🇺 Выберите язык:", reply_markup=lang_kb())

@bot.message_handler(func=lambda m: m.text in [TEXTS["uz"]["btn_referral"], TEXTS["ru"]["btn_referral"]])
def menu_referral(message):
    uid = message.from_user.id
    conn = get_db()
    balance = conn.execute("SELECT balance FROM users WHERE id = ?", (uid,)).fetchone()["balance"]
    conn.close()
    
    link = f"https://t.me/{bot.get_me().username}?start=ref_{uid}"
    text = t(uid, "referral_text", link, format_price(balance), CURRENCY)
    bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda m: m.text in [TEXTS["uz"]["btn_wishlist"], TEXTS["ru"]["btn_wishlist"]])
def menu_wishlist(message):
    uid = message.from_user.id
    conn = get_db()
    items = conn.execute("SELECT p.* FROM wishlist w JOIN products p ON w.product_id = p.id WHERE w.user_id = ?", (uid,)).fetchall()
    conn.close()
    
    if not items:
        bot.send_message(message.chat.id, t(uid, "wishlist_empty"))
        return
        
    lang = get_lang(uid)
    name_col = f"name_{lang}"
    kb = types.InlineKeyboardMarkup(row_width=1)
    for p in items:
        kb.add(types.InlineKeyboardButton(text=f"⭐ {p[name_col]}", callback_data=f"prod_{p['id']}"))
    
    bot.send_message(message.chat.id, t(uid, "btn_wishlist") + ":", reply_markup=kb)

@bot.message_handler(func=lambda m: m.text in [TEXTS["uz"]["btn_search"], TEXTS["ru"]["btn_search"]])
def menu_search(message):
    user_states[message.from_user.id] = {"state": "waiting_search", "data": {}}
    bot.send_message(message.chat.id, t(message.from_user.id, "search_prompt"), reply_markup=cancel_kb(message.from_user.id))

@bot.message_handler(func=lambda m: m.from_user.id in user_states and user_states[m.from_user.id].get("state") == "waiting_search")
def process_search(message):
    uid = message.from_user.id
    if message.text in [TEXTS["uz"]["btn_cancel"], TEXTS["ru"]["btn_cancel"]]:
        user_states.pop(uid, None)
        bot.send_message(message.chat.id, t(uid, "main_menu"), reply_markup=main_menu_kb(uid))
        return
        
    kb, count = products_inline_kb(uid, search_query=message.text)
    user_states.pop(uid, None)
    
    bot.send_message(message.chat.id, t(uid, "main_menu"), reply_markup=main_menu_kb(uid))
    if count == 0:
        bot.send_message(message.chat.id, t(uid, "search_not_found"))
    else:
        bot.send_message(message.chat.id, t(uid, "search_results"), reply_markup=kb)


@bot.message_handler(func=lambda m: m.text in [TEXTS["uz"]["btn_orders"], TEXTS["ru"]["btn_orders"]])
def menu_orders(message):
    uid = message.from_user.id
    conn = get_db()
    orders = conn.execute("SELECT * FROM orders WHERE user_id = ? ORDER BY created_at DESC LIMIT 10", (uid,)).fetchall()
    conn.close()
    
    if not orders:
        bot.send_message(message.chat.id, t(uid, "search_not_found"))
        return
        
    for o in orders:
        text = f"📦 Buyurtma #{o['id']}\n💰 {format_price(o['total_price'])} {CURRENCY}\n💳 To'lov: {o['payment_method']}\n📌 Status: {o['status']}\n📅 {o['created_at']}\n"
        bot.send_message(message.chat.id, text)

# ============ CATALOG CALLBACKS ============

@bot.callback_query_handler(func=lambda c: c.data == "back_cats")
def back_cats(call):
    bot.edit_message_text(t(call.from_user.id, "choose_category"), call.message.chat.id, call.message.message_id, reply_markup=categories_inline_kb(call.from_user.id))

@bot.callback_query_handler(func=lambda c: c.data.startswith("cat_"))
def show_category(call):
    cat_id = int(call.data.split("_")[1])
    kb, count = products_inline_kb(call.from_user.id, category_id=cat_id)
    if count == 0:
        bot.answer_callback_query(call.id, t(call.from_user.id, "search_not_found"), show_alert=True)
        return
    bot.edit_message_text(t(call.from_user.id, "choose_product"), call.message.chat.id, call.message.message_id, reply_markup=kb)

@bot.callback_query_handler(func=lambda c: c.data.startswith("prod_"))
def show_product(call):
    prod_id = int(call.data.split("_")[1])
    uid = call.from_user.id
    lang = get_lang(uid)
    
    conn = get_db()
    p = conn.execute("SELECT * FROM products WHERE id = ?", (prod_id,)).fetchone()
    conn.close()
    
    if not p:
        bot.answer_callback_query(call.id, "Error", show_alert=True)
        return
        
    name = p[f"name_{lang}"]
    desc = p[f"desc_{lang}"]
    price = format_price(p['price'])
    rating = round(p['rating_sum'] / p['rating_count'], 1) if p['rating_count'] > 0 else 0
    
    if p['old_price']:
        old_price = format_price(p['old_price'])
        price_text = t(uid, "product_sale", old_price, CURRENCY, price, CURRENCY)
    else:
        price_text = f"{price} {CURRENCY}"
        
    text = t(uid, "product_info", name, desc, price_text, "", rating, p['rating_count'])
    kb = product_detail_kb(uid, prod_id, p['category_id'])
    
    bot.delete_message(call.message.chat.id, call.message.message_id)
    if p['photo_url']:
        bot.send_photo(call.message.chat.id, p['photo_url'], caption=text, reply_markup=kb, parse_mode="HTML")
    else:
        bot.send_message(call.message.chat.id, text, reply_markup=kb, parse_mode="HTML")


@bot.callback_query_handler(func=lambda c: c.data.startswith("rate_"))
def rate_product(call):
    parts = call.data.split("_")
    prod_id = int(parts[1])
    score = int(parts[2])
    uid = call.from_user.id
    
    conn = get_db()
    existing = conn.execute("SELECT score FROM ratings WHERE user_id = ? AND product_id = ?", (uid, prod_id)).fetchone()
    if existing:
        bot.answer_callback_query(call.id, "Siz allaqachon baholagansiz / Вы уже оценили", show_alert=True)
        conn.close()
        return
        
    conn.execute("INSERT INTO ratings (user_id, product_id, score) VALUES (?, ?, ?)", (uid, prod_id, score))
    conn.execute("UPDATE products SET rating_sum = rating_sum + ?, rating_count = rating_count + 1 WHERE id = ?", (score, prod_id))
    conn.commit()
    
    p = conn.execute("SELECT rating_sum, rating_count, category_id FROM products WHERE id = ?", (prod_id,)).fetchone()
    conn.close()
    
    bot.answer_callback_query(call.id, t(uid, "thank_you_rating"), show_alert=True)
    
    try:
        # Refresh the keyboard so ratings update (not updating text to save space)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=product_detail_kb(uid, prod_id, p['category_id']))
    except: pass

@bot.callback_query_handler(func=lambda c: c.data.startswith("wish_"))
def toggle_wishlist(call):
    prod_id = int(call.data.split("_")[1])
    uid = call.from_user.id
    
    conn = get_db()
    existing = conn.execute("SELECT 1 FROM wishlist WHERE user_id = ? AND product_id = ?", (uid, prod_id)).fetchone()
    if existing:
        conn.execute("DELETE FROM wishlist WHERE user_id = ? AND product_id = ?", (uid, prod_id))
        msg = t(uid, "removed_from_wishlist")
    else:
        conn.execute("INSERT INTO wishlist (user_id, product_id) VALUES (?, ?)", (uid, prod_id))
        msg = t(uid, "added_to_wishlist")
    conn.commit()
    conn.close()
    
    p_cat = get_db().execute("SELECT category_id FROM products WHERE id = ?", (prod_id,)).fetchone()
    kb = product_detail_kb(uid, prod_id, p_cat['category_id'] if p_cat else 1)
    
    try:
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=kb)
    except: pass
    
    bot.answer_callback_query(call.id, msg)


# ============ CART & CHECKOUT ============

@bot.callback_query_handler(func=lambda c: c.data.startswith("addcart_"))
def add_to_cart(call):
    prod_id = int(call.data.split("_")[1])
    uid = call.from_user.id
    
    conn = get_db()
    existing = conn.execute("SELECT quantity FROM cart WHERE user_id = ? AND product_id = ?", (uid, prod_id)).fetchone()
    if existing:
        conn.execute("UPDATE cart SET quantity = quantity + 1 WHERE user_id = ? AND product_id = ?", (uid, prod_id))
    else:
        conn.execute("INSERT INTO cart (user_id, product_id, quantity) VALUES (?, ?, 1)", (uid, prod_id))
    conn.commit()
    conn.close()
    
    bot.answer_callback_query(call.id, t(uid, "added_to_cart"))

@bot.message_handler(func=lambda m: m.text in [TEXTS["uz"]["btn_cart"], TEXTS["ru"]["btn_cart"]])
def show_cart(message):
    uid = message.from_user.id
    conn = get_db()
    items = conn.execute("SELECT c.quantity, p.price FROM cart c JOIN products p ON c.product_id = p.id WHERE c.user_id = ?", (uid,)).fetchall()
    conn.close()
    
    if not items:
        bot.send_message(message.chat.id, t(uid, "cart_empty"))
        return
        
    total = sum(i['quantity'] * i['price'] for i in items)
    
    text = t(uid, "cart_content")
    text += t(uid, "cart_total", format_price(total), CURRENCY)
    
    bot.send_message(message.chat.id, text, reply_markup=cart_kb(uid))

@bot.callback_query_handler(func=lambda c: c.data.startswith("cartminus_") or c.data.startswith("cartplus_"))
def modify_cart(call):
    action, prod_id = call.data.split("_")
    prod_id = int(prod_id)
    uid = call.from_user.id
    
    conn = get_db()
    qty = conn.execute("SELECT quantity FROM cart WHERE user_id = ? AND product_id = ?", (uid, prod_id)).fetchone()
    
    if qty:
        q = qty['quantity']
        if action == "cartminus" and q > 1:
            conn.execute("UPDATE cart SET quantity = quantity - 1 WHERE user_id = ? AND product_id = ?", (uid, prod_id))
        elif action == "cartminus" and q == 1:
            conn.execute("DELETE FROM cart WHERE user_id = ? AND product_id = ?", (uid, prod_id))
        elif action == "cartplus":
            conn.execute("UPDATE cart SET quantity = quantity + 1 WHERE user_id = ? AND product_id = ?", (uid, prod_id))
        conn.commit()
    
    items = conn.execute("SELECT c.quantity, p.price FROM cart c JOIN products p ON c.product_id = p.id WHERE c.user_id = ?", (uid,)).fetchall()
    conn.close()
    
    if not items:
        bot.edit_message_text(t(uid, "cart_empty"), call.message.chat.id, call.message.message_id)
        return
        
    total = sum(i['quantity'] * i['price'] for i in items)
    text = t(uid, "cart_content") + t(uid, "cart_total", format_price(total), CURRENCY)
    
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=cart_kb(uid))

@bot.callback_query_handler(func=lambda c: c.data == "cart_clear")
def clear_cart(call):
    uid = call.from_user.id
    conn = get_db()
    conn.execute("DELETE FROM cart WHERE user_id = ?", (uid,))
    conn.commit()
    conn.close()
    bot.edit_message_text(t(uid, "cart_empty"), call.message.chat.id, call.message.message_id)


@bot.callback_query_handler(func=lambda c: c.data == "cart_checkout")
def checkout_start(call):
    uid = call.from_user.id
    user_states[uid] = {"state": "checkout_phone", "data": {}}
    
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.send_message(call.message.chat.id, t(uid, "checkout_phone"), reply_markup=phone_kb(uid))

@bot.message_handler(content_types=["contact", "text"], func=lambda m: m.from_user.id in user_states and user_states[m.from_user.id].get("state") == "checkout_phone")
def checkout_phone(message):
    uid = message.from_user.id
    if message.text in [TEXTS["uz"]["btn_cancel"], TEXTS["ru"]["btn_cancel"]]:
        user_states.pop(uid, None)
        bot.send_message(message.chat.id, t(uid, "main_menu"), reply_markup=main_menu_kb(uid))
        return
        
    phone = message.contact.phone_number if message.contact else message.text
    user_states[uid]["data"]["phone"] = phone
    user_states[uid]["state"] = "checkout_payment"
    
    bot.send_message(message.chat.id, t(uid, "main_menu"), reply_markup=main_menu_kb(uid))
    bot.send_message(message.chat.id, t(uid, "checkout_payment"), reply_markup=payment_kb(uid))


@bot.callback_query_handler(func=lambda c: c.data.startswith("pay_"))
def checkout_finish(call):
    uid = call.from_user.id
    if uid not in user_states or user_states[uid].get("state") != "checkout_payment":
        return
        
    payment = call.data.split("_")[1]
    phone = user_states[uid]["data"]["phone"]
    
    conn = get_db()
    items = conn.execute("SELECT c.product_id, c.quantity, p.price FROM cart c JOIN products p ON c.product_id = p.id WHERE c.user_id = ?", (uid,)).fetchall()
    
    if not items:
        bot.answer_callback_query(call.id, "Xatolik!", show_alert=True)
        return
        
    total = sum(i['quantity'] * i['price'] for i in items)
    
    c = conn.cursor()
    c.execute("INSERT INTO orders (user_id, phone, payment_method, total_price) VALUES (?, ?, ?, ?)", (uid, phone, payment, total))
    order_id = c.lastrowid
    
    for item in items:
        c.execute("INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (?, ?, ?, ?)", 
                  (order_id, item['product_id'], item['quantity'], item['price']))
                  
    c.execute("DELETE FROM cart WHERE user_id = ?", (uid,))
    conn.commit()
    conn.close()
    
    user_states.pop(uid, None)
    
    pay_texts = {"cash": "Naqd", "click": "Click", "payme": "Payme", "uzum": "Uzum"}
    p_name = pay_texts.get(payment, payment)
    
    bot.edit_message_text(t(uid, "order_success", order_id, p_name), call.message.chat.id, call.message.message_id)
    
    try:
        bot.send_message(ADMIN_ID, f"🆕 <b>Yangi buyurtma #{order_id}</b>\nTelefon: {phone}\nTo'lov: {p_name}\nSumma: {format_price(total)} {CURRENCY}")
    except: pass


# ============ ADMIN BROADCAST ============

@bot.message_handler(func=lambda m: m.text == "📢 Xabar yuborish" and m.from_user.id == ADMIN_ID)
def admin_broadcast_start(message):
    user_states[message.from_user.id] = {"state": "admin_broadcast"}
    bot.send_message(message.chat.id, "📢 Xabarni yoki rasmni yuboring. /cancel bekor qilish uchun.")

@bot.message_handler(content_types=["text", "photo"], func=lambda m: m.from_user.id in user_states and user_states[m.from_user.id].get("state") == "admin_broadcast")
def admin_broadcast_send(message):
    if message.text == "/cancel":
        user_states.pop(message.from_user.id, None)
        bot.send_message(message.chat.id, "❌ Bekor qilindi.", reply_markup=admin_menu_kb())
        return
        
    conn = get_db()
    users = conn.execute("SELECT id FROM users").fetchall()
    conn.close()
    
    success = 0
    for u in users:
        try:
            if message.photo:
                bot.send_photo(u['id'], message.photo[-1].file_id, caption=message.caption, parse_mode="HTML")
            else:
                bot.send_message(u['id'], message.text, parse_mode="HTML")
            success += 1
        except:
            pass
            
    user_states.pop(message.from_user.id, None)
    bot.send_message(message.chat.id, f"✅ Xabar {success} ta foydalanuvchiga yuborildi!", reply_markup=admin_menu_kb())

@bot.message_handler(func=lambda m: m.text == "🏠 Asosiy menyu" and m.from_user.id == ADMIN_ID)
def go_main_menu(message):
    user_states.pop(message.from_user.id, None)
    bot.send_message(message.chat.id, "🏠 Asosiy menyu", reply_markup=main_menu_kb(message.from_user.id))

@bot.message_handler(func=lambda m: m.text == "📊 Statistika" and m.from_user.id == ADMIN_ID)
def show_stats_admin(message):
    conn = get_db()
    users_count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    orders_count = conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
    total_revenue = conn.execute("SELECT SUM(total_price) FROM orders WHERE status != 'bekor'").fetchone()[0] or 0
    conn.close()
    
    bot.send_message(message.chat.id, f"📊 <b>Statistika:</b>\nFoydalanuvchilar: {users_count}\nBuyurtmalar: {orders_count}\nUmumiy summa: {format_price(total_revenue)} {CURRENCY}")

if __name__ == "__main__":
    init_db()
    add_sample_data()
    logger.info("Bot ishga tushmoqda...")
    bot.infinity_polling(skip_pending=True)
