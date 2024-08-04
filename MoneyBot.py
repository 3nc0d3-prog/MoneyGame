import nest_asyncio
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters
from telegram.constants import ParseMode

# nest_asyncio'yu uygula
nest_asyncio.apply()

# Bot token'ı
TOKEN = "7369038732:AAG1THLHOc6olTeED7_dGne2hIrSvDeOB8M"

# Uygulama oluştur
application = ApplicationBuilder().token(TOKEN).build()

# Kullanıcıların bakiyelerini saklamak için basit bir sözlük
user_balances = {}

# /start komutu işleyicisi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Bakiye", callback_data='balance')],
        [InlineKeyboardButton("Referans", callback_data='refer')],
        [InlineKeyboardButton("Kayıt", callback_data='register')],
        [InlineKeyboardButton("Para Çek", callback_data='withdraw')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Merhaba! Lütfen bir seçenek belirleyin:', reply_markup=reply_markup)

# Buton tıklama işleyicisi
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    try:
        if query.data == 'balance':
            await query.edit_message_text(text="Mevcut bakiyeniz: 100 MNG")
        elif query.data == 'refer':
            await query.edit_message_text(text="Referans kodunuz: ABC123")
        elif query.data == 'register':
            await query.edit_message_text(text="Başarıyla kayıt oldunuz!")
        elif query.data == 'withdraw':
            await query.edit_message_text(text="Para çekme işlemi başlatıldı. Lütfen talimatları takip edin.")
    except Exception as e:
        print(f"Error occurred in button handler: {e}")

# /balance komutu işleyicisi
async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    balance = user_balances.get(user_id, 0)
    await update.message.reply_text(f"Mevcut bakiyeniz: {balance} MNG")

# /refer komutu işleyicisi
async def refer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Referans kodunuz: ABC123")

# /register komutu işleyicisi
async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Başarıyla kayıt oldunuz!")

# /withdraw komutu işleyicisi
async def withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Para çekme işlemi başlatıldı. Lütfen talimatları takip edin.")

# Bilinmeyen komut işleyicisi
async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Üzgünüm, bu komutu tanımıyorum. Geçerli komutlar için /help yazabilirsiniz.")

# Ana fonksiyon
async def main():
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("balance", balance))
    application.add_handler(CommandHandler("refer", refer))
    application.add_handler(CommandHandler("register", register))
    application.add_handler(CommandHandler("withdraw", withdraw))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.COMMAND, unknown_command))
    
    try:
        await application.run_polling()
    except Exception as e:
        print(f"Error occurred during polling: {e}")

if __name__ == '__main__':
    asyncio.run(main())
