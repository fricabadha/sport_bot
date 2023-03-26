from pytest_mock import MockerFixture
import src.main
from tests.test_sportbot import get_bot


def test_start(mocker: MockerFixture):
    update = mocker.Mock()
    update.message.reply_text = mocker.Mock()

    src.main.start(update, None)

    update.message.reply_text.assert_called_once_with(
        "Ciao! Sono il tuo assistente per la tracciatura degli allenamenti di corsa. Invia il comando /help per avere la lista dei comandi disponibili.")


def test_help(mocker: MockerFixture):
    update = mocker.Mock()
    update.message.reply_text = mocker.Mock()

    src.main.help(update, None)

    update.message.reply_text.assert_called_once_with("Lista dei comandi disponibili:\n\n"
                                                      "/start - Avvia il bot\n"
                                                      "/help - Mostra questo messaggio di aiuto\n"
                                                      "/save - Salva i dati del proprio allenamento\n"
                                                      "/history - Mostra la cronologia di tutti gli allenamenti\n"
                                                      "/goal - Imposta un obiettivo di distanza\n"
                                                      "/stats - Mostra statistiche complessive: Totale e media di km percorsi, tempo impiegato, velocità media\n"
                                                      "/clear - Elimina tutti i dati.")


def test_save(mocker: MockerFixture):
    update = mocker.Mock()
    update.effective_chat.id = 1
    update.message.reply_text = mocker.Mock()
    context = mocker.Mock()
    context.args = ["1", "00:00:00"]
    src.main.sportBot = mocker.Mock()
    src.main.sportBot.save_workout = mocker.Mock(return_value=None)

    src.main.save(update, context)

    src.main.sportBot.save_workout.assert_called_once_with(1, "1", "00:00:00")
    update.message.reply_text.assert_called_once_with(
        "Formato del tempo non valido, deve essere HH:MM:SS")


def test_history(mocker: MockerFixture):
    update = mocker.Mock()
    update.effective_chat.id = 1
    update.message.reply_text = mocker.Mock()
    context = mocker.Mock()
    context.args = ["1", "00:00:00"]
    src.main.sportBot = mocker.Mock()
    src.main.sportBot.history_workout = mocker.Mock(
        return_value=[(1, 1, "00:00:00", "1")])
    src.main.sportBot.avg_speed = mocker.Mock(return_value=0.0)

    src.main.history(update, context)

    src.main.sportBot.history_workout.assert_called_once_with(1)
    update.message.reply_text.assert_called_once_with(
        f"Time: 00:00:00, Distance: 1, Average Speed: 0.0")


def test_goal(mocker: MockerFixture):
    update = mocker.Mock()
    update.effective_chat.id = 1
    update.message.reply_text = mocker.Mock()
    context = mocker.Mock()
    context.args = ["1"]
    src.main.sportBot = mocker.Mock()
    src.main.sportBot.save_goal = mocker.Mock(return_value=None)

    src.main.goal(update, context)

    src.main.sportBot.save_goal.assert_called_once_with(1, "1")
    update.message.reply_text.assert_called_once_with(
        f"Obiettivo di distanza memorizzato.")


def test_stats(mocker: MockerFixture):
    update = mocker.Mock()
    update.effective_chat.id = 1
    update.message.reply_text = mocker.Mock()
    context = mocker.Mock()
    context.args = ["1"]
    src.main.sportBot = mocker.Mock()
    src.main.sportBot.stats_workout = mocker.Mock(return_value={
        "tot_ore": 1,
        "tot_km": 1,
        "media_ore": 1,
        "media_km": 1,
        "avg_speed": 1,
        "tot_works": 1,
    })

    src.main.stats(update, context)

    src.main.sportBot.stats_workout.assert_called_once_with(1)
    update.message.reply_text.assert_called_once_with(
        f"Totale ore: 1,\n"
        f"Media ore: 1,\n"
        f"Totale km: 1,\n"
        f"Media km: 1,\n"
        f"Velocità media: 1,\n"
        f"Totale allenamenti: 1")


def test_clear(mocker: MockerFixture):
    update = mocker.Mock()
    update.effective_chat.id = 1
    update.message.reply_text = mocker.Mock()
    context = mocker.Mock()
    context.args = ["1"]
    src.main.sportBot = mocker.Mock()
    src.main.sportBot.clear_history = mocker.Mock(return_value=None)

    src.main.clear(update, context)

    src.main.sportBot.clear_history.assert_called_once_with(1)
    update.message.reply_text.assert_called_once_with(
        f"Dati eliminati")


def test_main(mocker: MockerFixture):
    mocker.patch("src.main.Updater")

    src.main.main("token")

    src.main.Updater.assert_called_once
