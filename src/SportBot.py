import re
import mysql.connector
from dotenv import load_dotenv
import math
import os
from typing import List, Any


class SportBot:
    def __init__(self, connection=None) -> None:
        load_dotenv()
        self.mydb = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_DATABASE")
        ) if connection is None else connection

        self.conn = self.mydb.cursor()
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS workouts (id BIGINT AUTO_INCREMENT PRIMARY KEY, user_id BIGINT, time TEXT, distance FLOAT)")
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS goals (id BIGINT AUTO_INCREMENT PRIMARY KEY,user_id BIGINT, distance FLOAT)")

    def save_workout(self, user_id: str, time: str, distance: str) -> bool | None:
        rx = r"^([01]?\d|2[0-3]):([0-5]\d):([0-5]\d)$"
        matches = re.findall(rx, time)
        if len(matches) == 0:
            return None
        self.conn.execute(
            "INSERT into workouts (user_id, time, distance) values (%s, %s, %s)", (user_id, time, distance))
        self.mydb.commit()

        goal = self.return_goal(user_id)
        if goal is not None and float(distance) >= float(goal[2]):
            self.delete_goal(user_id)
            return True

        return False

    def history_workout(self, user_id: str) -> List[Any]:
        self.conn.execute(
            "SELECT * FROM workouts where user_id = %s", (user_id,))
        workouts = self.conn.fetchall()
        return workouts

    def stats_workout(self, user_id: str) -> List[Any]:
        self.conn.execute(
            "SELECT * FROM workouts where user_id = %s", (user_id,))
        workouts = self.conn.fetchall()
        if len(workouts) == 0:
            return
        sum_ore = 0
        sum_km = 0
        for workout in workouts:
            sum_ore += self.convert_time_in_sec(workout[2])
            sum_km += workout[3]
        media = sum_ore/max(len(workouts), 1)
        return {
            "tot_ore": self.convert_sec_in_time(sum_ore),
            "media_ore": self.convert_sec_in_time(media),
            "tot_km": sum_km,
            "media_km": round(sum_km/max(len(workouts), 1), 2),
            "avg_speed": round(self.avg_speed(self.convert_sec_in_time(sum_ore), sum_km), 2),
            "tot_works": len(workouts)
        }

    def save_goal(self, user_id: str, distance: str) -> None:
        res = self.return_goal(user_id)
        if res:
            self.conn.execute(
                "DELETE FROM goals where user_id = %s", (user_id,))
        self.conn.execute(
            "INSERT into goals (user_id, distance) values (%s, %s)", (user_id, distance))
        self.mydb.commit()

    def return_goal(self, user_id: str) -> List[Any]:
        self.conn.execute("SELECT * FROM goals where user_id = %s", (user_id,))
        goals = self.conn.fetchall()
        for goal in goals:
            return goal
        return None

    def delete_goal(self, user_id: str) -> None:
        self.conn.execute("DELETE FROM goals where user_id = %s", (user_id,))
        self.mydb.commit()

    def clear_history(self, user_id: str) -> None:
        self.conn.execute(
            "DELETE FROM workouts where user_id = %s", (user_id,))
        self.mydb.commit()

    def avg_speed(self, time: str, distance: str) -> float:
        splitted_time = time.split(":")
        sec = int(splitted_time[2])
        min = int(splitted_time[1])
        ore = int(splitted_time[0])

        ore += min/60
        ore += sec/3600

        return round(distance/ore, 3)

    def convert_time_in_sec(self, time: str) -> float:
        splitted_time = time.split(":")
        sec = int(splitted_time[2])
        min = int(splitted_time[1])
        ore = int(splitted_time[0])
        return (ore*3600)+(min*60)+sec

    def convert_sec_in_time(self, sec: str) -> str:
        ore = math.floor(sec/3600)
        min = math.floor((sec % 3600)/60)
        sec = math.floor((sec % 3600) % 60)

        l = [f"{ore:02d}", f"{min:02d}", f"{sec:02d}"]

        time = ':'.join(str(n) for n in l)
        return time
