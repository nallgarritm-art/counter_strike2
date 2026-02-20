from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os
TOKEN = os.getenv("BOT_TOKEN")
from database import get_player
from duel import fight

pending_duels = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    get_player(user.id, user.username)
    await update.message.reply_text("🎮 Ты зарегистрирован в CS2 Duel Bot!")

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    p = get_player(user.id, user.username)
    await update.message.reply_text(
        f"👤 {user.username}\n"
        f"🎯 Aim: {p[2]}\n"
        f"🧠 Sense: {p[3]}\n"
        f"⚡ Reaction: {p[4]}\n"
        f"🔥 Luck: {p[5]}\n"
        f"🏅 Rating: {p[6]}"
    )

async def duel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Укажи @username")
        return

    challenger = update.effective_user
    opponent = context.args[0].replace("@", "")
    pending_duels[opponent] = challenger.username

    await update.message.reply_text(
        f"⚔️ @{challenger.username} вызвал @{opponent} на дуэль!\n"
        f"Напиши /accept"
    )

async def accept(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.username not in pending_duels:
        await update.message.reply_text("❌ Нет активных дуэлей")
        return

    challenger_name = pending_duels.pop(user.username)
    p1 = get_player(user.id, user.username)
    p2 = get_player(update.effective_user.id, challenger_name)

    winner, weapon, map_ = fight(p1, p2)

    await update.message.reply_text(
        f"💥 Дуэль на {map_}\n"
        f"🔫 Оружие: {weapon}\n"
        f"🏆 Победитель: @{winner[1]}"
    )

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("profile", profile))
    app.add_handler(CommandHandler("duel", duel))
    app.add_handler(CommandHandler("accept", accept))

    app.run_polling()

if __name__ == "__main__":
    main()