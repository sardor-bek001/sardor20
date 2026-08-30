# ==========================================
# Tech Store UZ Bot - Klaviaturalar
# ==========================================

from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)

from config import CURRENCY


# ============ Reply Klaviaturalar ============

def main_menu_kb():
    """Asosiy menyu"""
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🛍 Katalog"), KeyboardButton(text="🛒 Buyurtmalarim")],
            [KeyboardButton(text="📞 Biz bilan bog'lanish"), KeyboardButton(text="ℹ️ Bot haqida")],
        ],
        resize_keyboard=True,
        input_field_placeholder="Menyudan tanlang..."
    )
    return kb


def phone_kb():
    """Telefon raqam yuborish"""
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Telefon raqamni yuborish", request_contact=True)],
            [KeyboardButton(text="❌ Bekor qilish")],
        ],
        resize_keyboard=True
    )
    return kb


def cancel_kb():
    """Bekor qilish tugmasi"""
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="❌ Bekor qilish")],
        ],
        resize_keyboard=True
    )
    return kb


def admin_menu_kb():
    """Admin menyu"""
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📊 Statistika"), KeyboardButton(text="📋 Buyurtmalar")],
            [KeyboardButton(text="➕ Mahsulot qo'shish"), KeyboardButton(text="🗑 Mahsulot o'chirish")],
            [KeyboardButton(text="🏠 Asosiy menyu")],
        ],
        resize_keyboard=True
    )
    return kb


# ============ Inline Klaviaturalar ============

def categories_kb(categories):
    """Kategoriyalar inline tugmalari"""
    buttons = []
    for cat in categories:
        buttons.append([
            InlineKeyboardButton(
                text=cat["name"],
                callback_data=f"category_{cat['id']}"
            )
        ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def products_kb(products, category_id):
    """Mahsulotlar ro'yxati"""
    buttons = []
    for prod in products:
        price_formatted = f"{prod['price']:,}".replace(",", " ")
        buttons.append([
            InlineKeyboardButton(
                text=f"{prod['name']} — {price_formatted} {CURRENCY}",
                callback_data=f"product_{prod['id']}"
            )
        ])
    buttons.append([
        InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_categories")
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def product_detail_kb(product_id, category_id):
    """Mahsulot tafsilotlari tugmalari"""
    buttons = [
        [InlineKeyboardButton(
            text="🛒 Buyurtma berish",
            callback_data=f"order_{product_id}"
        )],
        [InlineKeyboardButton(
            text="⬅️ Orqaga",
            callback_data=f"category_{category_id}"
        )],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def confirm_order_kb(product_id):
    """Buyurtmani tasdiqlash"""
    buttons = [
        [
            InlineKeyboardButton(text="✅ Tasdiqlash", callback_data=f"confirm_{product_id}"),
            InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cancel_order"),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def order_status_kb(order_id):
    """Admin uchun buyurtma status o'zgartirish"""
    buttons = [
        [
            InlineKeyboardButton(text="✅ Qabul qilindi", callback_data=f"status_{order_id}_qabul"),
            InlineKeyboardButton(text="🚚 Yetkazilmoqda", callback_data=f"status_{order_id}_yetkazish"),
        ],
        [
            InlineKeyboardButton(text="📦 Topshirildi", callback_data=f"status_{order_id}_topshirildi"),
            InlineKeyboardButton(text="❌ Bekor qilindi", callback_data=f"status_{order_id}_bekor"),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def quantity_kb(product_id):
    """Miqdor tanlash"""
    buttons = [
        [
            InlineKeyboardButton(text="1 dona", callback_data=f"qty_{product_id}_1"),
            InlineKeyboardButton(text="2 dona", callback_data=f"qty_{product_id}_2"),
            InlineKeyboardButton(text="3 dona", callback_data=f"qty_{product_id}_3"),
        ],
        [
            InlineKeyboardButton(text="⬅️ Orqaga", callback_data=f"product_{product_id}"),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
