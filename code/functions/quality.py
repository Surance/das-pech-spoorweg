def calculate_quality(ridden: list, trains: list, all_connections: list) -> float:
    """
    Function calculates quality of created schedule according to RailNL formula
   
     Args:
        ridden (list): List of connections ridden by the trains.
        trains (list): List of trains in the schedule.
        all_connections (list): List of all connections in the Netherlands.

    Returns:
        float: The calculated quality value.
    """
    p = len(ridden) / len(all_connections)
    T = len(trains)
    Min = sum([train.total_time for train in trains])
    K = p * 10000 - (T * 100 + Min)
    
    return K