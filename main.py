from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Fila de espera e pares ativos
esperando = []
pares = {}

# Quando o usuário digita /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in pares:
        await update.message.reply_text("Você já está em um chat.")
        return
    if esperando and esperando[0] != user_id:
        parceiro = esperando.pop(0)
        pares[user_id] = parceiro
        pares[parceiro] = user_id
        await context.bot.send_message(chat_id=user_id, text="✅ Você foi conectado! Fale algo.")
        await context.bot.send_message(chat_id=parceiro, text="✅ Você foi conectado! Fale algo.")
    else:
        esperando.append(user_id)
        await update.message.reply_text("⏳ Aguardando alguém para conversar...")

# Quando o usuário digita /sair
async def sair(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in pares:
        parceiro = pares.pop(user_id)
        pares.pop(parceiro, None)
        await context.bot.send_message(chat_id=parceiro, text="❌ A pessoa saiu do chat.")
        await update.message.reply_text("✅ Você saiu do chat.")
    elif user_id in esperando:
        esperando.remove(user_id)
        await update.message.reply_text("✅ Você saiu da fila.")
    else:
        await update.message.reply_text("⚠️ Você não está em nenhum chat.")

# Quando o usuário manda mensagem comum
async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in pares:
        parceiro = pares[user_id]
        await context.bot.send_message(chat_id=parceiro, text=update.message.text)
    else:
        await update.message.reply_text("ℹ️ Use /start para encontrar alguém.")

# INICIALIZA O BOT com seu TOKEN
app = ApplicationBuilder().token("7885167902:AAGzld0SE7YChLKZgR3RHc_m_sWbs3bI_TU").build()

# Adiciona os comandos e manipuladores de mensagens
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("sair", sair))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))

print("🤖 Bot rodando...")
app.run_polling()
