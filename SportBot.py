import mysql.connector
import math

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="sesso6969",
    database="sportBot"
)

conn = mydb.cursor()
conn.execute("CREATE TABLE IF NOT EXISTS workouts (id BIGINT AUTO_INCREMENT PRIMARY KEY, user_id BIGINT, time TEXT, distance FLOAT)")
conn.execute(
    "CREATE TABLE IF NOT EXISTS goals (id BIGINT AUTO_INCREMENT PRIMARY KEY,user_id BIGINT, distance FLOAT)")


class SportBot:
    def __init__(self) -> None:
        pass

    def save_workout(self, user_id, time, distance):
        conn.execute(
            "INSERT into workouts (user_id, time, distance) values (%s, %s, %s)", (user_id, time, distance))
        mydb.commit()

    def history_workout(self, user_id):
        conn.execute("SELECT * FROM workouts where user_id = %s", (user_id,))
        workouts = conn.fetchall()
        return workouts

    def stats_workout(self, user_id):
        conn.execute("SELECT * FROM workouts where user_id = %s", (user_id,))
        workouts = conn.fetchall()
        if len(workouts) == 0:
            return
        sum_ore = 0
        sum_km = 0
        for workout in workouts:
            print("Tempo: ", workout[2], self.convert_time_in_sec(workout[2]))
            print("Dustanza: ", workout[3])
            sum_ore+=self.convert_time_in_sec(workout[2])
            sum_km+=workout[3]
        print("Totale ore in sec: ", sum_ore)
        print("Totale ore: ", self.convert_sec_in_time(sum_ore))
        media = sum_ore/max(len(workouts), 1)
        ogg = {
            "tot_ore" : self.convert_sec_in_time(sum_ore),
            "media_ore" : self.convert_sec_in_time(media),
            "tot_km" : sum_km,
            "media_km" : round(sum_km/max(len(workouts), 1), 2),
            "avg_speed" : round(self.avg_speed(self.convert_sec_in_time(sum_ore), sum_km), 2),
            "tot_works" : len(workouts)
        }
        return ogg

    def save_goal(self, user_id, distance):
        res = self.return_goal(user_id)
        if res:
            conn.execute("DELETE FROM goals where user_id = %s", (user_id,))
        conn.execute(
            "INSERT into goals (user_id, distance) values (%s, %s)", (user_id, distance))
        mydb.commit()

    def return_goal(self, user_id):
        conn.execute("SELECT * FROM goals where user_id = %s", (user_id,))
        goals = conn.fetchall()
        for goal in goals:
            return goal
        return None

    def delete_goal(self, user_id):
        conn.execute("DELETE FROM goals where user_id = %s", (user_id,))
        mydb.commit()

    def clear_history(self, user_id):
        conn.execute("DELETE FROM workouts where user_id = %s", (user_id,))
        mydb.commit()

    def avg_speed(self, time, distance):
        splitted_time = time.split(":")
        sec = int(splitted_time[2])
        min = int(splitted_time[1])
        ore = int(splitted_time[0])

        ore += min/60
        ore += sec/3600

        return round(distance/ore, 3)
    
    def convert_time_in_sec(self, time):
        splitted_time = time.split(":")
        sec = int(splitted_time[2])
        min = int(splitted_time[1])
        ore = int(splitted_time[0])
        return (ore*3600)+(min*60)+sec
    
    def convert_sec_in_time(self, sec):
        ore = math.floor(sec/3600)
        min = math.floor((sec%3600)/60)
        sec = math.floor((sec%3600)%60)

        l = [ore, min, sec]

        time = ':'.join(str(n) for n in l)
        return time


