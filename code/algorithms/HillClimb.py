from code.classes.quality import Quality

class HillClimbingScheduler:
    @staticmethod
    
    def hill_climbing_schedule(schedule: classmethod, max_iterations: int=1000) -> tuple[list, set]:
        i = 1
        best_score = float('-inf')
        best_schedule = None  # Initialize best_schedule variable

        while i <= max_iterations:
            schedule.add_train()

            while schedule.current_time < schedule.max_time and len(schedule.ridden) < len(schedule.total_connections):
                possible_connections = schedule.check_possible_connections()

                if len(possible_connections.keys()) == 0:
                    break

                sorted_connections = sorted(possible_connections.keys(), key=lambda x: x.travel_time)
                connection = sorted_connections[0]

                schedule.valid_connection(connection, possible_connections[connection])

            current_score = HillClimbingScheduler.calculate_schedule_score(schedule)

            if current_score > best_score:
                best_score = current_score
                best_schedule = schedule.copy_schedule()

            i += 1

            # Reset the schedule for the next iteration
            schedule = schedule.copy_schedule()

        trains = best_schedule.trains
        ridden = best_schedule.ridden

        return trains, ridden

    @staticmethod
    def calculate_schedule_score(schedule: classmethod) -> float:
        return Quality(schedule.ridden, schedule.trains, schedule.total_connections).calculate_quality()
