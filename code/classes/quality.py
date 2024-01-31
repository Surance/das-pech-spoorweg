def calculate_quality(ridden: list, trains: list, all_connections: list) -> float:
    """
    Calculates quality of created schedule according to RailNL formula
    """
    p = len(ridden) / len(all_connections)
    T = len(trains)
    Min = sum([train.total_time for train in trains])
    K = p * 10000 - (T * 100 + Min)
    
    return K