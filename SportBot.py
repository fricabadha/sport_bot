class SportBot:
    def __init__(self) -> None:
        self.data = []

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
    
    def save_goal():
        pass

    def delete_goal():
        pass

    def clear_history():
        pass
