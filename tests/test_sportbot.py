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
        assert bot.save_workout(1, "00:30:00", 5) is False

        bot.save_goal(1, 2)
        assert bot.save_workout(1, "00:30:00", 5) is True
        assert bot.save_workout(1, "blabla", 5) is None
        
        conn = mydb.cursor()
        conn.execute("SELECT * FROM workouts")
        workouts = conn.fetchall()

        test_data["mydb"].close()

        assert len(workouts) == 2
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

    def test_stats_workout(self):
        test_data = get_bot()
        bot = test_data["bot"]

        stats = bot.stats_workout(1)
        assert stats is None

        bot.save_workout(1, "00:30:00", 5)
        bot.save_workout(1, "00:35:00", 15)

        stats = bot.stats_workout(1)
        test_data["mydb"].close()

        assert stats["tot_ore"] == "01:05:00"
        assert stats["media_ore"] == "00:32:30"
        assert stats["tot_km"] == 20
        assert stats["media_km"] == 10
        assert stats["avg_speed"] == 18.46
        assert stats["tot_works"] == 2

    def test_save_goals(self):
        test_data = get_bot()
        bot = test_data["bot"]

        bot.save_goal(1, 10)
        bot.save_goal(1, 20)

        goal = bot.return_goal(1)
        test_data["mydb"].close()

        assert goal is not None
        assert goal[1] == 1
        assert goal[2] == 20

    def test_delete_goals(self):
        test_data = get_bot()
        bot = test_data["bot"]

        bot.save_goal(1, 10)

        bot.delete_goal(1)

        goals = bot.return_goal(1)

        test_data["mydb"].close()
        assert goals is None

    def test_clear_history(self):
        test_data = get_bot()
        bot = test_data["bot"]

        bot.save_workout(1, "00:30:00", 5)
        bot.save_workout(1, "00:35:00", 15)

        bot.clear_history(1)

        workouts = bot.history_workout(1)
        test_data["mydb"].close()

        assert len(workouts) == 0
