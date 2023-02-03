from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler
import os

load_dotenv()


def start(update, context):
    update.message.reply_text(
        "Ciao! Sono il tuo assistente per la tracciatura degli allenamenti di corsa. Invia il comando /help per avere la lista dei comandi disponibili.")


def help(update, context):
    update.message.reply_text("Questo è l'aiuto del bot")


def error(update, context):
    print('Update "%s" caused error "%s"' % (update, context.error))


if __name__ == "__main__":
    TOKEN = os.getenv("TOKEN")
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()
