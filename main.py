from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler
from SportBot import SportBot
import os
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

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
    goal = sportBot.return_goal(id)
    if(goal):
        if float(distance) >= float(goal['distance']):
            update.message.reply_text("Hai raggiunto il tuo obiettivo, impostane uno nuovo!")
            sportBot.delete_goal(goal)
    update.message.reply_text("Dati salvati")


def history(update, context):
    id = update.effective_chat.id
    workouts = sportBot.history_workout()
    for workout in workouts:
        if id == workout['user_id']:
            update.message.reply_text("Tempo: %s, Distanza: %s, Velocità media: %s" % (
                workout['time'], workout['distance'], workout['avg_speed']))

def goal(update, context):
    id = update.effective_chat.id
    distance = context.args[0]
    goal = sportBot.return_goal(id)
    if(goal):
        sportBot.delete_goal(goal)
    sportBot.save_goal(id, distance)
    update.message.reply_text("Obiettivo di distanza memorizzato.")


def clear(update, context):
    id = update.effective_chat.id
    sportBot.clear_history(id)
    update.message.reply_text("Dati eliminati")
    

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
    dp.add_handler(CommandHandler('goal', goal))
    dp.add_handler(CommandHandler('clear', clear))

    # dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()
