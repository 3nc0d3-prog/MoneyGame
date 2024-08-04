import nest_asyncio
nest_asyncio.apply()

import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder,Application, CommandHandler, ContextTypes, MessageHandler, filters

# Kullanıcıların bakiyelerini saklamak için basit bir sözlük
user_balances = {}

# Başlangıç komutu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id not in user_balances:
        user_balances[user_id] = 0  # Yeni kullanıcılar için başlangıç bakiyesi
    await update.message.reply_text("Merhaba! Para kazanma botuna hoş geldiniz.\nMNG bakiyenizi öğrenmek için /balance komutunu kullanın.")

# Bakiye kontrol komutu
async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    balance = user_balances.get(user_id, 0)
    await update.message.reply_text(f"Mevcut MNG bakiyeniz: {balance} MNG")

# Referans kodu oluşturma komutu
async def refer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    referral_code = f"ref-{user_id}"
    await update.message.reply_text(f"Referans kodunuz: {referral_code}\nBu kodu arkadaşlarınızla paylaşarak MNG kazanabilirsiniz.")

# Referans kodu ile kayıt olma komutu
async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    referrer_code = context.args[0] if context.args else None
    if referrer_code and referrer_code.startswith("ref-"):
        referrer_id = int(referrer_code.split("-")[1])
        if referrer_id in user_balances:
            user_balances[referrer_id] += 10  # Referans bonusu
            await update.message.reply_text("Kayıt tamamlandı! Referans bonusu kazandınız.")
        else:
            await update.message.reply_text("Geçersiz referans kodu.")
    else:
        await update.message.reply_text("Lütfen geçerli bir referans kodu sağlayın.")

# Cüzdana aktarım komutu (Bu sadece bir simülasyondur)
async def withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    amount = int(context.args[0]) if context.args else 0
    if user_balances.get(user_id, 0) >= amount:
        user_balances[user_id] -= amount
        await update.message.reply_text(f"{amount} MNG başarıyla cüzdanınıza aktarıldı.")
    else:
        await update.message.reply_text("Yetersiz bakiye.")
# Botu başlatan ana fonksiyon
async def main():
    application = ApplicationBuilder().token("7369038732:AAG1THLHOc6olTeED7_dGne2hIrSvDeOB8M").build()

    # Komutları ekle
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("balance", balance))
    application.add_handler(CommandHandler("refer", refer))
    application.add_handler(CommandHandler("register", register))
    application.add_handler(CommandHandler("withdraw", withdraw))
# Diğer komutlarınız burada olacak...

# Bilinmeyen komutlar için fallback işleyicisi
async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Üzgünüm, bu komutu tanımıyorum. Geçerli komutlar için /help yazabilirsiniz.")

# Bilinmeyen mesajlar için fallback işleyicisi
unknown_handler = MessageHandler(filters.COMMAND, unknown_command)

# Fallback işleyicisini uygulamaya ekleyin
application.add_handler(unknown_handler)

# Diğer komutlarınızı ve uygulamanızın başlatılmasını ekleyin...

    # Botu başlat
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
