import asyncio
from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler

TOKEN = '7369038732:AAG1THLHOc6olTeED7_dGne2hIrSvDeOB8M'
REFERRAL_REWARD = 10  # MNG cinsinden ödül
balance = {}  # Kullanıcı bakiyelerini tutar

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id not in balance:
        balance[user_id] = 0

    keyboard = [
        [InlineKeyboardButton("Hesap Bakiyesi", callback_data='balance')],
        [InlineKeyboardButton("Referans Linki", callback_data='referral')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Merhaba! MNG Botuna Hoşgeldiniz. Seçenekler:', reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    if query.data == 'balance':
        await query.edit_message_text(text=f"Bakiyeniz: {balance[user_id]} MNG")
    elif query.data == 'referral':
        referral_link = f"http://t.me/YourBotUsername?start={user_id}"
        await query.edit_message_text(text=f"Referans linkiniz: {referral_link}")

async def referral_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    referral_id = update.message.text.split()[1] if len(update.message.text.split()) > 1 else None
    if referral_id and referral_id.isdigit():
        referral_id = int(referral_id)
        if referral_id in balance:
            balance[referral_id] += REFERRAL_REWARD
            await update.message.reply_text(f"Referans için teşekkürler! {REFERRAL_REWARD} MNG kazandınız.")
        else:
            await update.message.reply_text("Geçersiz referans kodu.")
    else:
        await update.message.reply_text("Referans kodu bulunamadı.")

async def main():
    bot = Bot(token=TOKEN)
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(CommandHandler("referral", referral_handler))

    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    await application.idle()

if __name__ == "__main__":
    asyncio.run(main())
