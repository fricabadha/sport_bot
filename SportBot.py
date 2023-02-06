class SportBot:
    def __init__(self) -> None:
        self.data = []
        self.goals = []

    def save_workout(self, user_id, time, distance, avg_speed):
        self.data.append({
            'user_id': user_id,
            'time': time,
            'distance': distance,
            'avg_speed': avg_speed
        })

    def history_workout(self):
        return self.data

    def stats_workout():
        pass

    def save_goal(self, user_id, distance):
        self.goals.append({
            'user_id': user_id,
            'distance': distance
        })

    def return_goal(self, user_id):
        for goal in self.goals:
            if (user_id == goal['user_id']):
                return goal
        return None

    def delete_goal(self, goal):
        self.goals.remove(goal)

    def clear_history(self, id):
        new_data = []
        workouts = self.history_workout()
        for workout in workouts:
            if id != workout['user_id']:
                new_data.append(workout)
        self.data = new_data
