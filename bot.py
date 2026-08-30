# ==========================================
# Tech Store UZ Bot - @Tech_Store_uz_bot
# pyTelegramBotAPI (telebot) asosida
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

# Logging
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)

# Bot yaratish
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

# ============ MA'LUMOTLAR BAZASI ============

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tech_store.db")

# Foydalanuvchi holatlari (FSM o'rniga)
user_states = {}  # {user_id: {"state": "...", "data": {...}}}


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        emoji TEXT DEFAULT '📦'
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        description TEXT,
        price INTEGER NOT NULL,
        in_stock INTEGER DEFAULT 1,
        FOREIGN KEY (category_id) REFERENCES categories(id)
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        user_fullname TEXT,
        username TEXT,
        phone TEXT,
        product_id INTEGER NOT NULL,
        product_name TEXT NOT NULL,
        product_price INTEGER NOT NULL,
        quantity INTEGER DEFAULT 1,
        status TEXT DEFAULT 'yangi',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        fullname TEXT,
        username TEXT,
        phone TEXT,
        registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")

    conn.commit()
    conn.close()


def add_sample_data():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM categories")
    if c.fetchone()[0] > 0:
        conn.close()
        return

    categories = [
        ("📱 Smartfonlar", "📱"),
        ("💻 Noutbuklar", "💻"),
        ("🎧 Aksessuarlar", "🎧"),
        ("⌚ Smart soatlar", "⌚"),
        ("📟 Planshetlar", "📟"),
    ]
    c.executemany("INSERT INTO categories (name, emoji) VALUES (?, ?)", categories)

    products = [
        (1, "iPhone 15 Pro Max", "🔥 A17 Pro chip\n📸 48MP kamera\n🔋 4422 mAh batareya\n💾 256GB xotira", 14500000, 1),
        (1, "Samsung Galaxy S24 Ultra", "🔥 Snapdragon 8 Gen 3\n📸 200MP kamera\n🔋 5000 mAh\n💾 256GB xotira", 13800000, 1),
        (1, "Xiaomi 14 Pro", "🔥 Snapdragon 8 Gen 3\n📸 50MP Leica kamera\n🔋 4880 mAh\n💾 256GB", 7500000, 1),
        (1, "iPhone 15", "🔥 A16 Bionic chip\n📸 48MP kamera\n🔋 3877 mAh\n💾 128GB xotira", 10200000, 1),
        (1, "Samsung Galaxy A55", "🔥 Exynos 1480\n📸 50MP kamera\n🔋 5000 mAh\n💾 128GB", 3800000, 1),

        (2, "MacBook Air M3", "🔥 Apple M3 chip\n🖥 13.6\" Liquid Retina\n💾 8GB/256GB\n🔋 18 soat batareya", 15500000, 1),
        (2, "Lenovo IdeaPad 3", "🔥 Intel i5-12450H\n🖥 15.6\" FHD\n💾 8GB/512GB SSD\n🎮 Integ. GPU", 5200000, 1),
        (2, "HP Pavilion 15", "🔥 AMD Ryzen 5 7530U\n🖥 15.6\" FHD IPS\n💾 8GB/512GB SSD", 5800000, 1),
        (2, "ASUS VivoBook 15", "🔥 Intel i3-1215U\n🖥 15.6\" FHD\n💾 8GB/256GB SSD", 3900000, 1),

        (3, "AirPods Pro 2", "🎵 Aktiv shovqin bekor qilish\n🔋 6 soat ishlash\n💧 IPX4 suv o'tkazmaydi", 2800000, 1),
        (3, "Samsung Galaxy Buds2 Pro", "🎵 ANC\n🔋 5 soat\n💧 IPX7", 1500000, 1),
        (3, "Baseus 65W zaryadka", "⚡ 65W tez zaryadlash\n🔌 USB-C + USB-A\n📱 Barcha qurilmalarga mos", 250000, 1),
        (3, "Anker PowerBank 20000mAh", "🔋 20000 mAh\n⚡ 22.5W tez zaryadlash\n📱 2 ta qurilmani zaryadlaydi", 350000, 1),
        (3, "iPhone 15 Pro chexol (MagSafe)", "🛡 Himoya chexol\n🧲 MagSafe\n🎨 6 xil rang", 150000, 1),

        (4, "Apple Watch Series 9", "🖥 Always-On Retina\n❤️ Sog'liq sensori\n💧 50m suv o'tkazmaydi\n🔋 18 soat", 5500000, 1),
        (4, "Samsung Galaxy Watch 6", "🖥 Super AMOLED\n❤️ BioActive sensor\n💧 5ATM+IP68\n🔋 40 soat", 3200000, 1),
        (4, "Xiaomi Watch S3", "🖥 1.43\" AMOLED\n❤️ SpO2, yurak urishi\n💧 5ATM\n🔋 15 kun", 1200000, 1),

        (5, "iPad Air M2", "🔥 Apple M2 chip\n🖥 11\" Liquid Retina\n💾 128GB\n✏️ Apple Pencil Pro", 8500000, 1),
        (5, "Samsung Galaxy Tab S9", "🔥 Snapdragon 8 Gen 2\n🖥 11\" AMOLED 120Hz\n💾 128GB\n✏️ S Pen", 7200000, 1),
        (5, "Xiaomi Pad 6", "🔥 Snapdragon 870\n🖥 11\" 2.8K 144Hz\n💾 128GB\n🔋 8840 mAh", 3500000, 1),
    ]
    c.executemany("INSERT INTO products (category_id, name, description, price, in_stock) VALUES (?, ?, ?, ?, ?)", products)

    conn.commit()
    conn.close()
    logger.info("✅ Namuna ma'lumotlar qo'shildi!")


def format_price(price):
    return f"{price:,}".replace(",", " ")


# ============ KLAVIATURALAR ============

def main_menu_kb():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(types.KeyboardButton("🛍 Katalog"), types.KeyboardButton("🛒 Buyurtmalarim"))
    kb.row(types.KeyboardButton("📞 Biz bilan bog'lanish"), types.KeyboardButton("ℹ️ Bot haqida"))
    return kb


def phone_kb():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(types.KeyboardButton("📱 Telefon raqamni yuborish", request_contact=True))
    kb.row(types.KeyboardButton("❌ Bekor qilish"))
    return kb


def cancel_kb():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(types.KeyboardButton("❌ Bekor qilish"))
    return kb


def admin_menu_kb():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(types.KeyboardButton("📊 Statistika"), types.KeyboardButton("📋 Buyurtmalar"))
    kb.row(types.KeyboardButton("➕ Mahsulot qo'shish"), types.KeyboardButton("🗑 Mahsulot o'chirish"))
    kb.row(types.KeyboardButton("🏠 Asosiy menyu"))
    return kb


def categories_inline_kb():
    kb = types.InlineKeyboardMarkup()
    conn = get_db()
    cats = conn.execute("SELECT * FROM categories").fetchall()
    conn.close()
    for cat in cats:
        kb.add(types.InlineKeyboardButton(text=cat["name"], callback_data=f"cat_{cat['id']}"))
    return kb


def products_inline_kb(category_id):
    kb = types.InlineKeyboardMarkup()
    conn = get_db()
    prods = conn.execute("SELECT * FROM products WHERE category_id = ? AND in_stock = 1", (category_id,)).fetchall()
    conn.close()
    for p in prods:
        kb.add(types.InlineKeyboardButton(
            text=f"{p['name']} — {format_price(p['price'])} {CURRENCY}",
            callback_data=f"prod_{p['id']}"
        ))
    kb.add(types.InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_cats"))
    return kb


def product_detail_kb(product_id, category_id):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text="🛒 Buyurtma berish", callback_data=f"order_{product_id}"))
    kb.add(types.InlineKeyboardButton(text="⬅️ Orqaga", callback_data=f"cat_{category_id}"))
    return kb


def quantity_kb(product_id):
    kb = types.InlineKeyboardMarkup(row_width=3)
    kb.add(
        types.InlineKeyboardButton(text="1 dona", callback_data=f"qty_{product_id}_1"),
        types.InlineKeyboardButton(text="2 dona", callback_data=f"qty_{product_id}_2"),
        types.InlineKeyboardButton(text="3 dona", callback_data=f"qty_{product_id}_3"),
    )
    kb.add(types.InlineKeyboardButton(text="⬅️ Orqaga", callback_data=f"prod_{product_id}"))
    return kb


def order_status_kb(order_id):
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton(text="✅ Qabul qilindi", callback_data=f"st_{order_id}_qabul"),
        types.InlineKeyboardButton(text="🚚 Yetkazilmoqda", callback_data=f"st_{order_id}_yetkazish"),
    )
    kb.add(
        types.InlineKeyboardButton(text="📦 Topshirildi", callback_data=f"st_{order_id}_topshirildi"),
        types.InlineKeyboardButton(text="❌ Bekor qilindi", callback_data=f"st_{order_id}_bekor"),
    )
    return kb


# ============ /start KOMANDASI ============

@bot.message_handler(commands=["start"])
def cmd_start(message):
    # Foydalanuvchini saqlash
    conn = get_db()
    conn.execute("INSERT OR REPLACE INTO users (id, fullname, username) VALUES (?, ?, ?)",
                 (message.from_user.id, message.from_user.full_name, message.from_user.username))
    conn.commit()
    conn.close()

    # State tozalash
    user_states.pop(message.from_user.id, None)

    text = (
        f"🏪 <b>{BOT_NAME}</b> ga xush kelibsiz!\n\n"
        f"👋 Salom, <b>{message.from_user.first_name}</b>!\n\n"
        "🛍 Bizda eng sifatli va arzon texnika mahsulotlari!\n\n"
        "📱 Smartfonlar\n"
        "💻 Noutbuklar\n"
        "🎧 Aksessuarlar\n"
        "⌚ Smart soatlar\n"
        "📟 Planshetlar\n\n"
        "⬇️ Quyidagi menyudan tanlang:"
    )
    bot.send_message(message.chat.id, text, reply_markup=main_menu_kb())


# ============ /admin KOMANDASI ============

@bot.message_handler(commands=["admin"])
def cmd_admin(message):
    if message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, "⛔ Sizda admin huquqi yo'q!")
        return
    bot.send_message(message.chat.id, "🔐 <b>Admin panel</b>\n\nQuyidagi menyudan tanlang:", reply_markup=admin_menu_kb())


# ============ ASOSIY MENYU HANDLERLARI ============

@bot.message_handler(func=lambda m: m.text == "🏠 Asosiy menyu")
def go_main_menu(message):
    user_states.pop(message.from_user.id, None)
    bot.send_message(message.chat.id, "🏠 Asosiy menyu", reply_markup=main_menu_kb())


@bot.message_handler(func=lambda m: m.text == "🛍 Katalog")
def show_catalog(message):
    bot.send_message(message.chat.id, "📂 <b>Kategoriyalardan birini tanlang:</b>", reply_markup=categories_inline_kb())


@bot.message_handler(func=lambda m: m.text == "🛒 Buyurtmalarim")
def show_my_orders(message):
    conn = get_db()
    orders = conn.execute("SELECT * FROM orders WHERE user_id = ? ORDER BY created_at DESC LIMIT 10",
                          (message.from_user.id,)).fetchall()
    conn.close()

    if not orders:
        bot.send_message(message.chat.id, "📭 Sizda hali buyurtmalar yo'q.\n\n🛍 Buyurtma berish uchun <b>Katalog</b> tugmasini bosing!")
        return

    status_emoji = {"yangi": "🆕", "qabul": "✅", "yetkazish": "🚚", "topshirildi": "📦", "bekor": "❌"}
    text = "🛒 <b>Sizning buyurtmalaringiz:</b>\n\n"
    for o in orders:
        emoji = status_emoji.get(o["status"], "❓")
        text += (
            f"📋 Buyurtma #{o['id']}\n"
            f"📦 {o['product_name']}\n"
            f"💰 {format_price(o['product_price'])} {CURRENCY} x {o['quantity']} dona\n"
            f"{emoji} Status: <b>{o['status']}</b>\n"
            f"📅 {o['created_at']}\n"
            f"{'─' * 25}\n\n"
        )
    bot.send_message(message.chat.id, text)


@bot.message_handler(func=lambda m: m.text == "📞 Biz bilan bog'lanish")
def contact_info(message):
    text = (
        "📞 <b>Biz bilan bog'lanish:</b>\n\n"
        "📱 Telefon: +998 XX XXX XX XX\n"
        "📧 Email: techstoreuz@gmail.com\n"
        "📍 Manzil: Toshkent sh.\n"
        "🕐 Ish vaqti: 09:00 - 21:00\n\n"
        "💬 Telegram: @tech_store_uz_admin\n"
        "📸 Instagram: @tech_store_uz\n\n"
        "❓ Savollaringiz bo'lsa, yozing!"
    )
    bot.send_message(message.chat.id, text)


@bot.message_handler(func=lambda m: m.text == "ℹ️ Bot haqida")
def about_bot(message):
    text = (
        f"ℹ️ <b>{BOT_NAME} haqida</b>\n\n"
        "🤖 Bu bot orqali siz eng yangi va sifatli\n"
        "texnika mahsulotlarini xarid qilishingiz mumkin.\n\n"
        "✅ <b>Afzalliklarimiz:</b>\n"
        "• 📦 Tez yetkazib berish\n"
        "• 💯 Original mahsulotlar\n"
        "• 🔄 Kafolat bilan\n"
        "• 💰 Eng arzon narxlar\n"
        "• 🚚 Bepul yetkazib berish (Toshkent bo'ylab)\n\n"
        "🛍 Xarid qilish uchun <b>Katalog</b> tugmasini bosing!"
    )
    bot.send_message(message.chat.id, text)


# ============ KATALOG CALLBACK ============

@bot.callback_query_handler(func=lambda c: c.data == "back_cats")
def back_to_categories(call):
    bot.edit_message_text("📂 <b>Kategoriyalardan birini tanlang:</b>",
                          call.message.chat.id, call.message.message_id,
                          reply_markup=categories_inline_kb())
    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda c: c.data.startswith("cat_"))
def show_category(call):
    cat_id = int(call.data.split("_")[1])
    conn = get_db()
    prods = conn.execute("SELECT * FROM products WHERE category_id = ? AND in_stock = 1", (cat_id,)).fetchall()
    cat = conn.execute("SELECT name FROM categories WHERE id = ?", (cat_id,)).fetchone()
    conn.close()

    if not prods:
        bot.answer_callback_query(call.id, "😔 Bu kategoriyada mahsulotlar yo'q.", show_alert=True)
        return

    cat_name = cat["name"] if cat else "Kategoriya"
    bot.edit_message_text(
        f"📂 <b>{cat_name}</b>\n\n🔽 Mahsulotni tanlang:",
        call.message.chat.id, call.message.message_id,
        reply_markup=products_inline_kb(cat_id)
    )
    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda c: c.data.startswith("prod_"))
def show_product(call):
    prod_id = int(call.data.split("_")[1])
    conn = get_db()
    p = conn.execute("SELECT * FROM products WHERE id = ?", (prod_id,)).fetchone()
    conn.close()

    if not p:
        bot.answer_callback_query(call.id, "❌ Mahsulot topilmadi.", show_alert=True)
        return

    text = (
        f"📦 <b>{p['name']}</b>\n\n"
        f"📝 <b>Tavsif:</b>\n{p['description']}\n\n"
        f"💰 <b>Narxi:</b> {format_price(p['price'])} {CURRENCY}\n\n"
        f"{'✅ Mavjud' if p['in_stock'] else '❌ Mavjud emas'}"
    )
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                          reply_markup=product_detail_kb(prod_id, p["category_id"]))
    bot.answer_callback_query(call.id)


# ============ BUYURTMA BERISH ============

@bot.callback_query_handler(func=lambda c: c.data.startswith("order_"))
def start_order(call):
    prod_id = int(call.data.split("_")[1])
    conn = get_db()
    p = conn.execute("SELECT * FROM products WHERE id = ?", (prod_id,)).fetchone()
    conn.close()

    if not p:
        bot.answer_callback_query(call.id, "❌ Mahsulot topilmadi.", show_alert=True)
        return

    bot.edit_message_text(
        f"🛒 <b>{p['name']}</b>\n"
        f"💰 Narxi: {format_price(p['price'])} {CURRENCY}\n\n"
        f"📦 Nechta buyurtma bermoqchisiz?",
        call.message.chat.id, call.message.message_id,
        reply_markup=quantity_kb(prod_id)
    )
    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda c: c.data.startswith("qty_"))
def select_quantity(call):
    parts = call.data.split("_")
    prod_id = int(parts[1])
    qty = int(parts[2])

    conn = get_db()
    p = conn.execute("SELECT * FROM products WHERE id = ?", (prod_id,)).fetchone()
    conn.close()

    if not p:
        bot.answer_callback_query(call.id, "❌ Mahsulot topilmadi.", show_alert=True)
        return

    total = p["price"] * qty
    user_states[call.from_user.id] = {
        "state": "waiting_phone",
        "data": {
            "product_id": prod_id,
            "product_name": p["name"],
            "product_price": p["price"],
            "quantity": qty,
            "category_id": p["category_id"]
        }
    }

    bot.edit_message_text(
        f"🛒 <b>Buyurtma:</b>\n\n"
        f"📦 {p['name']}\n"
        f"📦 Miqdori: {qty} dona\n"
        f"💰 Jami: {format_price(total)} {CURRENCY}\n\n"
        f"📱 Telefon raqamingizni yuboring:",
        call.message.chat.id, call.message.message_id
    )
    bot.send_message(
        call.message.chat.id,
        "📱 Quyidagi tugmani bosing yoki raqamingizni yozing:\n(Masalan: +998901234567)",
        reply_markup=phone_kb()
    )
    bot.answer_callback_query(call.id)


# Telefon raqam — kontakt orqali
@bot.message_handler(content_types=["contact"], func=lambda m: m.from_user.id in user_states and user_states[m.from_user.id]["state"] == "waiting_phone")
def receive_phone_contact(message):
    phone = message.contact.phone_number
    if not phone.startswith("+"):
        phone = "+" + phone
    conn = get_db()
    conn.execute("UPDATE users SET phone = ? WHERE id = ?", (phone, message.from_user.id))
    conn.commit()
    conn.close()
    user_states[message.from_user.id]["data"]["phone"] = phone
    process_order(message)


# Telefon raqam — matn orqali
@bot.message_handler(func=lambda m: m.from_user.id in user_states and user_states[m.from_user.id]["state"] == "waiting_phone")
def receive_phone_text(message):
    if message.text == "❌ Bekor qilish":
        user_states.pop(message.from_user.id, None)
        bot.send_message(message.chat.id, "❌ Buyurtma bekor qilindi.", reply_markup=main_menu_kb())
        return

    phone = message.text.strip()
    clean_phone = phone.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
    if not (clean_phone.startswith("+998") and len(clean_phone) == 13):
        bot.send_message(message.chat.id, "⚠️ Noto'g'ri format! Iltimos, to'g'ri telefon raqam kiriting.\nMasalan: +998901234567")
        return

    conn = get_db()
    conn.execute("UPDATE users SET phone = ? WHERE id = ?", (phone, message.from_user.id))
    conn.commit()
    conn.close()
    user_states[message.from_user.id]["data"]["phone"] = phone
    process_order(message)


def process_order(message):
    uid = message.from_user.id
    data = user_states[uid]["data"]

    total = data["product_price"] * data["quantity"]

    conn = get_db()
    c = conn.cursor()
    c.execute(
        "INSERT INTO orders (user_id, user_fullname, username, phone, product_id, product_name, product_price, quantity) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (uid, message.from_user.full_name, message.from_user.username or "", data["phone"],
         data["product_id"], data["product_name"], data["product_price"], data["quantity"])
    )
    order_id = c.lastrowid
    conn.commit()
    conn.close()

    # Foydalanuvchiga xabar
    user_text = (
        f"✅ <b>Buyurtma #{order_id} qabul qilindi!</b>\n\n"
        f"📦 Mahsulot: {data['product_name']}\n"
        f"📦 Miqdori: {data['quantity']} dona\n"
        f"💰 Narxi: {format_price(data['product_price'])} {CURRENCY}\n"
        f"💰 Jami: {format_price(total)} {CURRENCY}\n"
        f"📱 Telefon: {data['phone']}\n\n"
        f"📞 Tez orada operator siz bilan bog'lanadi!\n"
        f"⏰ Ish vaqti: 09:00 - 21:00"
    )
    bot.send_message(message.chat.id, user_text, reply_markup=main_menu_kb())

    # Adminga xabar
    admin_text = (
        f"🆕 <b>Yangi buyurtma #{order_id}!</b>\n\n"
        f"👤 Mijoz: {message.from_user.full_name}\n"
        f"👤 Username: @{message.from_user.username or 'yoq'}\n"
        f"📱 Telefon: {data['phone']}\n\n"
        f"📦 Mahsulot: {data['product_name']}\n"
        f"📦 Miqdori: {data['quantity']} dona\n"
        f"💰 Narxi: {format_price(data['product_price'])} {CURRENCY}\n"
        f"💰 Jami: {format_price(total)} {CURRENCY}"
    )
    try:
        bot.send_message(ADMIN_ID, admin_text, reply_markup=order_status_kb(order_id))
    except Exception as e:
        logger.error(f"Adminga xabar yuborishda xatolik: {e}")

    user_states.pop(uid, None)


# ============ ADMIN: BUYURTMA STATUS O'ZGARTIRISH ============

@bot.callback_query_handler(func=lambda c: c.data.startswith("st_"))
def change_order_status(call):
    if call.from_user.id != ADMIN_ID:
        bot.answer_callback_query(call.id, "⛔ Sizda ruxsat yo'q!", show_alert=True)
        return

    parts = call.data.split("_")
    order_id = int(parts[1])
    new_status = parts[2]

    status_texts = {
        "qabul": "✅ Qabul qilindi",
        "yetkazish": "🚚 Yetkazilmoqda",
        "topshirildi": "📦 Topshirildi",
        "bekor": "❌ Bekor qilindi"
    }

    conn = get_db()
    conn.execute("UPDATE orders SET status = ? WHERE id = ?", (new_status, order_id))
    conn.commit()
    conn.close()

    bot.edit_message_text(
        call.message.text + f"\n\n{status_texts.get(new_status, new_status)} ✔️",
        call.message.chat.id, call.message.message_id,
        parse_mode="HTML"
    )
    bot.answer_callback_query(call.id, f"Buyurtma #{order_id} statusi yangilandi!", show_alert=True)


# ============ ADMIN: STATISTIKA ============

@bot.message_handler(func=lambda m: m.text == "📊 Statistika" and m.from_user.id == ADMIN_ID)
def show_stats(message):
    conn = get_db()
    total_users = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    total_orders = conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
    new_orders = conn.execute("SELECT COUNT(*) FROM orders WHERE status = 'yangi'").fetchone()[0]
    total_products = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
    conn.close()

    text = (
        "📊 <b>Statistika:</b>\n\n"
        f"👥 Jami foydalanuvchilar: <b>{total_users}</b>\n"
        f"🛒 Jami buyurtmalar: <b>{total_orders}</b>\n"
        f"🆕 Yangi buyurtmalar: <b>{new_orders}</b>\n"
        f"📦 Jami mahsulotlar: <b>{total_products}</b>\n"
    )
    bot.send_message(message.chat.id, text)


# ============ ADMIN: BUYURTMALAR RO'YXATI ============

@bot.message_handler(func=lambda m: m.text == "📋 Buyurtmalar" and m.from_user.id == ADMIN_ID)
def show_all_orders(message):
    conn = get_db()
    orders = conn.execute("SELECT * FROM orders ORDER BY created_at DESC LIMIT 15").fetchall()
    conn.close()

    if not orders:
        bot.send_message(message.chat.id, "📭 Buyurtmalar yo'q.")
        return

    status_emoji = {"yangi": "🆕", "qabul": "✅", "yetkazish": "🚚", "topshirildi": "📦", "bekor": "❌"}
    text = "📋 <b>Oxirgi buyurtmalar:</b>\n\n"
    for o in orders:
        emoji = status_emoji.get(o["status"], "❓")
        text += (
            f"📋 #{o['id']} | {emoji} {o['status']}\n"
            f"👤 {o['user_fullname']} | 📱 {o['phone']}\n"
            f"📦 {o['product_name']} x{o['quantity']}\n"
            f"💰 {format_price(o['product_price'])} {CURRENCY}\n"
            f"{'─' * 25}\n"
        )
    bot.send_message(message.chat.id, text)


# ============ ADMIN: MAHSULOT QO'SHISH ============

@bot.message_handler(func=lambda m: m.text == "➕ Mahsulot qo'shish" and m.from_user.id == ADMIN_ID)
def start_add_product(message):
    conn = get_db()
    cats = conn.execute("SELECT * FROM categories").fetchall()
    conn.close()

    text = "📂 Kategoriya raqamini kiriting:\n\n"
    for cat in cats:
        text += f"{cat['id']}. {cat['name']}\n"

    user_states[message.from_user.id] = {"state": "add_category", "data": {}}
    bot.send_message(message.chat.id, text, reply_markup=cancel_kb())


@bot.message_handler(func=lambda m: m.from_user.id in user_states and user_states[m.from_user.id]["state"] == "add_category")
def add_prod_category(message):
    if message.text == "❌ Bekor qilish":
        user_states.pop(message.from_user.id, None)
        bot.send_message(message.chat.id, "❌ Bekor qilindi.", reply_markup=admin_menu_kb())
        return
    try:
        cat_id = int(message.text)
        user_states[message.from_user.id]["data"]["category_id"] = cat_id
        user_states[message.from_user.id]["state"] = "add_name"
        bot.send_message(message.chat.id, "📝 Mahsulot nomini kiriting:")
    except ValueError:
        bot.send_message(message.chat.id, "⚠️ Raqam kiriting!")


@bot.message_handler(func=lambda m: m.from_user.id in user_states and user_states[m.from_user.id]["state"] == "add_name")
def add_prod_name(message):
    if message.text == "❌ Bekor qilish":
        user_states.pop(message.from_user.id, None)
        bot.send_message(message.chat.id, "❌ Bekor qilindi.", reply_markup=admin_menu_kb())
        return
    user_states[message.from_user.id]["data"]["name"] = message.text
    user_states[message.from_user.id]["state"] = "add_desc"
    bot.send_message(message.chat.id, "📝 Mahsulot tavsifini kiriting:")


@bot.message_handler(func=lambda m: m.from_user.id in user_states and user_states[m.from_user.id]["state"] == "add_desc")
def add_prod_desc(message):
    if message.text == "❌ Bekor qilish":
        user_states.pop(message.from_user.id, None)
        bot.send_message(message.chat.id, "❌ Bekor qilindi.", reply_markup=admin_menu_kb())
        return
    user_states[message.from_user.id]["data"]["description"] = message.text
    user_states[message.from_user.id]["state"] = "add_price"
    bot.send_message(message.chat.id, "💰 Mahsulot narxini kiriting (faqat raqam, so'mda):")


@bot.message_handler(func=lambda m: m.from_user.id in user_states and user_states[m.from_user.id]["state"] == "add_price")
def add_prod_price(message):
    if message.text == "❌ Bekor qilish":
        user_states.pop(message.from_user.id, None)
        bot.send_message(message.chat.id, "❌ Bekor qilindi.", reply_markup=admin_menu_kb())
        return
    try:
        price = int(message.text.replace(" ", "").replace(",", ""))
        data = user_states[message.from_user.id]["data"]

        conn = get_db()
        c = conn.cursor()
        c.execute("INSERT INTO products (category_id, name, description, price) VALUES (?, ?, ?, ?)",
                  (data["category_id"], data["name"], data["description"], price))
        prod_id = c.lastrowid
        conn.commit()
        conn.close()

        bot.send_message(
            message.chat.id,
            f"✅ Mahsulot muvaffaqiyatli qo'shildi!\n\n"
            f"🆔 ID: {prod_id}\n"
            f"📦 Nomi: {data['name']}\n"
            f"💰 Narxi: {format_price(price)} {CURRENCY}",
            reply_markup=admin_menu_kb()
        )
        user_states.pop(message.from_user.id, None)
    except ValueError:
        bot.send_message(message.chat.id, "⚠️ Faqat raqam kiriting!")


# ============ ADMIN: MAHSULOT O'CHIRISH ============

@bot.message_handler(func=lambda m: m.text == "🗑 Mahsulot o'chirish" and m.from_user.id == ADMIN_ID)
def delete_prod_prompt(message):
    user_states[message.from_user.id] = {"state": "delete_product", "data": {}}
    bot.send_message(
        message.chat.id,
        "🗑 O'chirmoqchi bo'lgan mahsulot ID sini yuboring.\n(Mahsulot ID sini katalogdan ko'rishingiz mumkin)",
        reply_markup=cancel_kb()
    )


@bot.message_handler(func=lambda m: m.from_user.id in user_states and user_states[m.from_user.id]["state"] == "delete_product")
def delete_prod(message):
    if message.text == "❌ Bekor qilish":
        user_states.pop(message.from_user.id, None)
        bot.send_message(message.chat.id, "❌ Bekor qilindi.", reply_markup=admin_menu_kb())
        return
    try:
        prod_id = int(message.text)
        conn = get_db()
        p = conn.execute("SELECT name FROM products WHERE id = ?", (prod_id,)).fetchone()
        if not p:
            bot.send_message(message.chat.id, "❌ Bunday ID li mahsulot topilmadi!")
            return
        conn.execute("DELETE FROM products WHERE id = ?", (prod_id,))
        conn.commit()
        conn.close()
        user_states.pop(message.from_user.id, None)
        bot.send_message(message.chat.id, f"🗑 <b>{p['name']}</b> o'chirildi!", reply_markup=admin_menu_kb())
    except ValueError:
        bot.send_message(message.chat.id, "⚠️ Raqam kiriting!")


# ============ ISHGA TUSHIRISH ============

if __name__ == "__main__":
    init_db()
    add_sample_data()

    logger.info(f"🤖 {BOT_NAME} bot ishga tushdi!")
    logger.info("Polling boshlandi...")

    bot.infinity_polling(skip_pending=True)
