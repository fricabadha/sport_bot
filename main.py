from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler
from SportBot import SportBot
import os
import logging
import re

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

load_dotenv()
sportBot = SportBot()

def start(update, context) -> None:
    update.message.reply_text(
        "Ciao! Sono il tuo assistente per la tracciatura degli allenamenti di corsa. Invia il comando /help per avere la lista dei comandi disponibili.")

def help(update, context) -> None:
    update.message.reply_text("Lista dei comandi disponibili:\n\n"
                              "/start - Avvia il bot\n"
                              "/help - Mostra questo messaggio di aiuto\n"
                              "/save - Salva i dati del proprio allenamento\n"
                              "/history - Mostra la cronologia di tutti gli allenamenti\n"
                              "/goal - Imposta un obiettivo di distanza\n"
                              "/stats - Mostra statistiche complessive: Totale e media di km percorsi, tempo impiegato, velocità media\n"
                              "/clear - Elimina tutti i dati.")

def save(update, context) -> None:
    id = update.effective_chat.id
    time, distance = context.args
    rx = r"^([01]?\d|2[0-3]):([0-5]\d):([0-5]\d)$"
    matches = re.findall(rx, time)
    if len(matches) == 0:
        update.message.reply_text("Formato del tempo non valido, deve essere HH:MM:SS")
        return
    sportBot.save_workout(id, time, distance)
    
    goal = sportBot.return_goal(id)
    print(goal)
    if(goal):
        if float(distance) >= float(goal[2]):
            update.message.reply_text("Hai raggiunto il tuo obiettivo, impostane uno nuovo!")
            sportBot.delete_goal(id)
    update.message.reply_text("Dati salvati")


def history(update, context) -> None:
    id = update.effective_chat.id
    workouts = sportBot.history_workout(id)
    for workout in workouts:
        update.message.reply_text(f"Time: {workout[2]}, Distance: {workout[3]}, Average Speed: {sportBot.avg_speed(workout[2], workout[3])}")

    
def goal(update, context) -> None:
    id = update.effective_chat.id
    distance = context.args[0]
    sportBot.save_goal(id, distance)
    update.message.reply_text("Obiettivo di distanza memorizzato.")

def stats(update, context) -> None:
    id = update.effective_chat.id
    res = sportBot.stats_workout(id)
    print(res)
    if res == None:
        update.message.reply_text("Non ci sono allenamenti")
    else:
        update.message.reply_text(f"Totale ore: {res['tot_ore']},\nMedia ore: {res['media_ore']},\nTotale km: {res['tot_km']},\nMedia km: {res['media_km']},\nVelocità media: {res['avg_speed']},\nTotale allenamenti: {res['tot_works']}" )

def clear(update, context) -> None:
    id = update.effective_chat.id
    sportBot.clear_history(id)
    update.message.reply_text("Dati eliminati")
    

def error(update, context) -> None:
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
    dp.add_handler(CommandHandler('stats', stats))
    dp.add_handler(CommandHandler('clear', clear))

    # dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()
