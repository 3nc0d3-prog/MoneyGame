import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

API_KEY = '7369038732:AAG1THLHOc6olTeED7_dGne2hIrSvDeOB8M'  # Bot API anahtarınızı buraya girin

# Logging ayarları
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Kullanıcıların bakiyelerini tutmak için bir sözlük
user_balances = {}

# Başlatma komutu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_balances:
        user_balances[user_id] = 0  # Yeni kullanıcı için başlangıç bakiyesi 0

    keyboard = [
        [InlineKeyboardButton("Görev Yap", callback_data='gorev_yap')],
        [InlineKeyboardButton("Cüzdana Para Aktar", callback_data='para_aktar')],
        [InlineKeyboardButton("Bakiye Görüntüle", callback_data='bakiye_goster')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text("Hoşgeldiniz! Lütfen bir işlem seçin:", reply_markup=reply_markup)

# Buton komutları için geri çağırma fonksiyonu
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    
    if query.data == 'gorev_yap':
        user_balances[user_id] += 10  # Görev başına 10 MNG ekle
        await query.edit_message_text(text=f"Görevi tamamladınız! Mevcut bakiyeniz: {user_balances[user_id]} MNG")
    
    elif query.data == 'para_aktar':
        if user_balances[user_id] >= 100:
            user_balances[user_id] -= 100
            await query.edit_message_text(text="Başarıyla 100 MNG cüzdanınıza aktarıldı!")
        else:
            await query.edit_message_text(text="Yetersiz bakiye. En az 100 MNG gerekiyor.")
    
    elif query.data == 'bakiye_goster':
        await query.edit_message_text(text=f"Mevcut bakiyeniz: {user_balances[user_id]} MNG")

# Ana fonksiyon
async def main():
    application = ApplicationBuilder().token(API_KEY).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button))
    
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
