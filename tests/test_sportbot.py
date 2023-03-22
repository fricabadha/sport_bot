import mysql.connector
from src.SportBot import SportBot
from dotenv import load_dotenv
import os


def get_bot():
    load_dotenv()

    mydb = mysql.connector.connect(
        host=os.getenv("DB_TEST_HOST"),
        user=os.getenv("DB_TEST_USER"),
        password=os.getenv("DB_TEST_PASSWORD"),
        database=os.getenv("DB_TEST_DATABASE")
    )

    conn = mydb.cursor()

    # Drop tables if they exist
    conn.execute("DROP TABLE IF EXISTS workouts")
    conn.execute("DROP TABLE IF EXISTS goals")

    return {
        "bot": SportBot(mydb),
        "mydb": mydb
    }


class TestSportBot:
    def test_setup(self) -> None:
        test_data = get_bot()

        conn = test_data["mydb"].cursor()
        conn.execute("SHOW TABLES")
        tables = conn.fetchall()

        assert len(tables) == 2
        assert tables[0][0] == "goals"
        assert tables[1][0] == "workouts"
        test_data["mydb"].close()

    def test_save_workout(self):
        test_data = get_bot()
        bot = test_data["bot"]
        mydb = test_data["mydb"]
        bot.save_workout(1, "00:30:00", 5)
        conn = mydb.cursor()
        conn.execute("SELECT * FROM workouts")
        workouts = conn.fetchall()

        test_data["mydb"].close()

        assert len(workouts) == 1
        assert workouts[0][1] == 1
        assert workouts[0][2] == "00:30:00"
        assert workouts[0][3] == 5

    def test_history_workout(self):
        test_data = get_bot()
        bot = test_data["bot"]

        bot.save_workout(1, "00:30:00", 5)
        bot.save_workout(2, "00:35:00", 15)

        workouts = bot.history_workout(1)
        test_data["mydb"].close()

        assert len(workouts) == 1
        assert workouts[0][1] == 1
        assert workouts[0][2] == "00:30:00"
        assert workouts[0][3] == 5

