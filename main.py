from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler
import os
from SportBot import SportBot

load_dotenv()
sportBot = SportBot()


def start(update, context):
    update.message.reply_text(
        "Ciao! Sono il tuo assistente per la tracciatura degli allenamenti di corsa. Invia il comando /help per avere la lista dei comandi disponibili.")


def help(update, context):
    update.message.reply_text("Questo è l'aiuto del bot")


def save(update, context):
    id = update.effective_chat.id
    time, distance, avg_speed = context.args
    sportBot.save_workout(id, time, distance, avg_speed)
    update.message.reply_text("Dati appena salvati")


def history(update, context):
    id = update.effective_chat.id
    workouts = sportBot.history_workout()
    for workout in workouts:
        if id == workout['user_id']:
            update.message.reply_text("Tempo: %s, Distanza: %s, Velocità media: %s" % (
                workout['time'], workout['distance'], workout['avg_speed']))


def error(update, context):
    print('Update "%s" caused error "%s"' % (update, context.error))


if __name__ == "__main__":
    TOKEN = os.getenv("TOKEN")
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("save", save))
    dp.add_handler(CommandHandler("history", history))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()
