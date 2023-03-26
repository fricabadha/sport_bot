import logging
import os
from telegram.ext import Updater, CommandHandler
from dotenv import load_dotenv
import sys
sys.path.append(".")
from src.SportBot import SportBot


sportBot = None


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
    res = sportBot.save_workout(
        update.effective_chat.id, context.args[0], context.args[1])
    if res is not None:
        update.message.reply_text(
            "Dati salvati" if not res else "Dati salvati e obiettivo raggiunto! Obiettivo eliminato.")
    else:
        update.message.reply_text(
            "Formato del tempo non valido, deve essere HH:MM:SS")


def history(update, context) -> None:
    for workout in sportBot.history_workout(update.effective_chat.id):
        update.message.reply_text(
            f"Time: {workout[2]}, Distance: {workout[3]}, Average Speed: {sportBot.avg_speed(workout[2], workout[3])}")


def goal(update, context) -> None:
    sportBot.save_goal(update.effective_chat.id, context.args[0])
    update.message.reply_text("Obiettivo di distanza memorizzato.")


def stats(update, context) -> None:
    res = sportBot.stats_workout(update.effective_chat.id)
    if res == None:
        update.message.reply_text("Non ci sono allenamenti")
    else:
        update.message.reply_text(
            f"Totale ore: {res['tot_ore']},\nMedia ore: {res['media_ore']},\nTotale km: {res['tot_km']},\nMedia km: {res['media_km']},\nVelocità media: {res['avg_speed']},\nTotale allenamenti: {res['tot_works']}")


def clear(update, context) -> None:
    sportBot.clear_history(update.effective_chat.id)
    update.message.reply_text("Dati eliminati")


def main(token: str) -> None:
    global sportBot

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    sportBot = SportBot()

    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("save", save))
    dp.add_handler(CommandHandler("history", history))
    dp.add_handler(CommandHandler('goal', goal))
    dp.add_handler(CommandHandler('stats', stats))
    dp.add_handler(CommandHandler('clear', clear))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    load_dotenv()
    TOKEN = os.getenv("TOKEN")

    main(TOKEN)
