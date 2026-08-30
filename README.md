# 🏪 Tech Store UZ Bot (@Tech_Store_uz_bot)

Telegram orqali texnika mahsulotlarini ko'rish va buyurtma berish boti.

## 📋 Funksiyalar

- 🛍 **Katalog** — 5 ta kategoriyada mahsulotlarni ko'rish
- 📦 **Buyurtma berish** — miqdor tanlash, telefon raqam kiritish
- 🛒 **Buyurtmalarim** — o'z buyurtmalarini kuzatish
- 🔐 **Admin panel** — statistika, buyurtmalarni boshqarish, mahsulot qo'shish/o'chirish
- 📞 **Bog'lanish** — do'kon kontaktlari

## 🚀 O'rnatish va ishga tushirish

### 1. Python o'rnatish
Python 3.10+ ni [python.org](https://www.python.org/downloads/) dan yuklab o'rnating.

> ⚠️ O'rnatish vaqtida **"Add Python to PATH"** ni belgilang!

### 2. Kutubxonalarni o'rnatish
```bash
pip install -r requirements.txt
```

### 3. Bot tokenini sozlash
1. Telegramda [@BotFather](https://t.me/BotFather) ga boring
2. `/mybots` yuboring → @Tech_Store_uz_bot ni tanlang → API Token
3. `config.py` faylida `BOT_TOKEN` ni o'z tokeningiz bilan almashtiring
4. `ADMIN_ID` ni o'z Telegram ID raqamingiz bilan almashtiring

> 💡 Telegram ID ni bilish uchun [@userinfobot](https://t.me/userinfobot) ga yozing

### 4. Botni ishga tushirish
```bash
python bot.py
```

## 📂 Fayl tuzilmasi

```
📁 Tech Store UZ Bot
├── bot.py           # Asosiy bot fayli
├── config.py        # Sozlamalar (token, admin ID)
├── database.py      # Ma'lumotlar bazasi
├── keyboards.py     # Tugmalar (klaviaturalar)
├── requirements.txt # Kutubxonalar
└── README.md        # Qo'llanma
```

## 🔐 Admin panel

Admin panelga kirish uchun botga `/admin` buyrug'ini yuboring.

**Admin imkoniyatlari:**
- 📊 Statistikani ko'rish
- 📋 Buyurtmalar ro'yxatini ko'rish
- ✅ Buyurtma statusini o'zgartirish (Qabul / Yetkazish / Topshirildi / Bekor)
- ➕ Yangi mahsulot qo'shish
- 🗑 Mahsulot o'chirish

## 📱 Foydalanuvchi uchun

1. Botga `/start` yuboring
2. **🛍 Katalog** tugmasini bosing
3. Kategoriya tanlang
4. Mahsulotni tanlang va tafsilotlarini ko'ring
5. **🛒 Buyurtma berish** tugmasini bosing
6. Miqdor tanlang
7. Telefon raqamingizni yuboring
8. ✅ Buyurtma qabul qilindi!
