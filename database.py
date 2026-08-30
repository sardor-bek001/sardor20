# ==========================================
# Tech Store UZ Bot - Ma'lumotlar bazasi
# ==========================================

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "tech_store.db")


def get_connection():
    """Ma'lumotlar bazasiga ulanish"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Jadvallarni yaratish"""
    conn = get_connection()
    cursor = conn.cursor()

    # Kategoriyalar jadvali
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            emoji TEXT DEFAULT '📦'
        )
    """)

    # Mahsulotlar jadvali
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            price INTEGER NOT NULL,
            photo_url TEXT,
            in_stock INTEGER DEFAULT 1,
            FOREIGN KEY (category_id) REFERENCES categories(id)
        )
    """)

    # Buyurtmalar jadvali
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
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
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)

    # Foydalanuvchilar jadvali
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            fullname TEXT,
            username TEXT,
            phone TEXT,
            registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def add_sample_data():
    """Namuna mahsulotlarini qo'shish (birinchi ishga tushirilganda)"""
    conn = get_connection()
    cursor = conn.cursor()

    # Kategoriyalar bormi tekshirish
    cursor.execute("SELECT COUNT(*) FROM categories")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return

    # Kategoriyalar
    categories = [
        ("📱 Smartfonlar", "📱"),
        ("💻 Noutbuklar", "💻"),
        ("🎧 Aksessuarlar", "🎧"),
        ("⌚ Smart soatlar", "⌚"),
        ("📟 Planshetlar", "📟"),
    ]
    cursor.executemany("INSERT INTO categories (name, emoji) VALUES (?, ?)", categories)

    # Namuna mahsulotlar
    products = [
        # Smartfonlar
        (1, "iPhone 15 Pro Max", "🔥 A17 Pro chip\n📸 48MP kamera\n🔋 4422 mAh batareya\n💾 256GB xotira", 14500000, None, 1),
        (1, "Samsung Galaxy S24 Ultra", "🔥 Snapdragon 8 Gen 3\n📸 200MP kamera\n🔋 5000 mAh\n💾 256GB xotira", 13800000, None, 1),
        (1, "Xiaomi 14 Pro", "🔥 Snapdragon 8 Gen 3\n📸 50MP Leica kamera\n🔋 4880 mAh\n💾 256GB", 7500000, None, 1),
        (1, "iPhone 15", "🔥 A16 Bionic chip\n📸 48MP kamera\n🔋 3877 mAh\n💾 128GB xotira", 10200000, None, 1),
        (1, "Samsung Galaxy A55", "🔥 Exynos 1480\n📸 50MP kamera\n🔋 5000 mAh\n💾 128GB", 3800000, None, 1),

        # Noutbuklar
        (2, "MacBook Air M3", "🔥 Apple M3 chip\n🖥 13.6\" Liquid Retina\n💾 8GB/256GB\n🔋 18 soat batareya", 15500000, None, 1),
        (2, "Lenovo IdeaPad 3", "🔥 Intel i5-12450H\n🖥 15.6\" FHD\n💾 8GB/512GB SSD\n🎮 Integ. GPU", 5200000, None, 1),
        (2, "HP Pavilion 15", "🔥 AMD Ryzen 5 7530U\n🖥 15.6\" FHD IPS\n💾 8GB/512GB SSD", 5800000, None, 1),
        (2, "ASUS VivoBook 15", "🔥 Intel i3-1215U\n🖥 15.6\" FHD\n💾 8GB/256GB SSD", 3900000, None, 1),

        # Aksessuarlar
        (3, "AirPods Pro 2", "🎵 Aktiv shovqin bekor qilish\n🔋 6 soat ishlash\n💧 IPX4 suv o'tkazmaydi", 2800000, None, 1),
        (3, "Samsung Galaxy Buds2 Pro", "🎵 ANC\n🔋 5 soat\n💧 IPX7", 1500000, None, 1),
        (3, "Baseus 65W zaryadka", "⚡ 65W tez zaryadlash\n🔌 USB-C + USB-A\n📱 Barcha qurilmalarga mos", 250000, None, 1),
        (3, "Anker PowerBank 20000mAh", "🔋 20000 mAh\n⚡ 22.5W tez zaryadlash\n📱 2 ta qurilmani zaryadlaydi", 350000, None, 1),
        (3, "iPhone 15 Pro chexol (MagSafe)", "🛡 Himoya chexol\n🧲 MagSafe\n🎨 6 xil rang", 150000, None, 1),

        # Smart soatlar
        (4, "Apple Watch Series 9", "🖥 Always-On Retina\n❤️ Sog'liq sensori\n💧 50m suv o'tkazmaydi\n🔋 18 soat", 5500000, None, 1),
        (4, "Samsung Galaxy Watch 6", "🖥 Super AMOLED\n❤️ BioActive sensor\n💧 5ATM+IP68\n🔋 40 soat", 3200000, None, 1),
        (4, "Xiaomi Watch S3", "🖥 1.43\" AMOLED\n❤️ SpO2, yurak urishi\n💧 5ATM\n🔋 15 kun", 1200000, None, 1),

        # Planshetlar
        (5, "iPad Air M2", "🔥 Apple M2 chip\n🖥 11\" Liquid Retina\n💾 128GB\n✏️ Apple Pencil Pro", 8500000, None, 1),
        (5, "Samsung Galaxy Tab S9", "🔥 Snapdragon 8 Gen 2\n🖥 11\" AMOLED 120Hz\n💾 128GB\n✏️ S Pen", 7200000, None, 1),
        (5, "Xiaomi Pad 6", "🔥 Snapdragon 870\n🖥 11\" 2.8K 144Hz\n💾 128GB\n🔋 8840 mAh", 3500000, None, 1),
    ]
    cursor.executemany(
        "INSERT INTO products (category_id, name, description, price, photo_url, in_stock) VALUES (?, ?, ?, ?, ?, ?)",
        products
    )

    conn.commit()
    conn.close()
    print("✅ Namuna ma'lumotlar muvaffaqiyatli qo'shildi!")


# ============ CRUD operatsiyalari ============

def get_categories():
    """Barcha kategoriyalarni olish"""
    conn = get_connection()
    rows = conn.execute("SELECT * FROM categories").fetchall()
    conn.close()
    return rows


def get_products_by_category(category_id):
    """Kategoriya bo'yicha mahsulotlarni olish"""
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM products WHERE category_id = ? AND in_stock = 1",
        (category_id,)
    ).fetchall()
    conn.close()
    return rows


def get_product_by_id(product_id):
    """Bitta mahsulotni olish"""
    conn = get_connection()
    row = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
    conn.close()
    return row


def save_user(user_id, fullname, username):
    """Foydalanuvchini saqlash"""
    conn = get_connection()
    conn.execute(
        """INSERT OR REPLACE INTO users (id, fullname, username) 
           VALUES (?, ?, ?)""",
        (user_id, fullname, username)
    )
    conn.commit()
    conn.close()


def update_user_phone(user_id, phone):
    """Foydalanuvchi telefonini yangilash"""
    conn = get_connection()
    conn.execute("UPDATE users SET phone = ? WHERE id = ?", (phone, user_id))
    conn.commit()
    conn.close()


def create_order(user_id, user_fullname, username, phone, product_id, product_name, product_price, quantity=1):
    """Buyurtma yaratish"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO orders (user_id, user_fullname, username, phone, 
           product_id, product_name, product_price, quantity) 
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (user_id, user_fullname, username, phone, product_id, product_name, product_price, quantity)
    )
    order_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return order_id


def get_user_orders(user_id):
    """Foydalanuvchi buyurtmalarini olish"""
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM orders WHERE user_id = ? ORDER BY created_at DESC LIMIT 10",
        (user_id,)
    ).fetchall()
    conn.close()
    return rows


def get_all_orders(status=None):
    """Barcha buyurtmalarni olish (admin uchun)"""
    conn = get_connection()
    if status:
        rows = conn.execute(
            "SELECT * FROM orders WHERE status = ? ORDER BY created_at DESC",
            (status,)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM orders ORDER BY created_at DESC LIMIT 50"
        ).fetchall()
    conn.close()
    return rows


def update_order_status(order_id, status):
    """Buyurtma statusini yangilash"""
    conn = get_connection()
    conn.execute("UPDATE orders SET status = ? WHERE id = ?", (status, order_id))
    conn.commit()
    conn.close()


def get_stats():
    """Statistika"""
    conn = get_connection()
    total_users = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    total_orders = conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
    new_orders = conn.execute("SELECT COUNT(*) FROM orders WHERE status = 'yangi'").fetchone()[0]
    total_products = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
    conn.close()
    return {
        "users": total_users,
        "orders": total_orders,
        "new_orders": new_orders,
        "products": total_products
    }


# ============ Admin operatsiyalari ============

def add_product(category_id, name, description, price, photo_url=None):
    """Yangi mahsulot qo'shish"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO products (category_id, name, description, price, photo_url) 
           VALUES (?, ?, ?, ?, ?)""",
        (category_id, name, description, price, photo_url)
    )
    product_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return product_id


def delete_product(product_id):
    """Mahsulotni o'chirish"""
    conn = get_connection()
    conn.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()


def toggle_product_stock(product_id):
    """Mahsulot mavjudligini almashtirish"""
    conn = get_connection()
    conn.execute(
        "UPDATE products SET in_stock = CASE WHEN in_stock = 1 THEN 0 ELSE 1 END WHERE id = ?",
        (product_id,)
    )
    conn.commit()
    conn.close()
