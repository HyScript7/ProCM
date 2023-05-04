import datetime


def parse_date(timestamp: float):
    date = datetime.datetime.fromtimestamp(timestamp)
    # Format the registration date
    # TODO: Change this to a more effective formatting method,
    #       because this is probably the single most inefficient
    #       method to do it.
    date = f"{['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][date.weekday()]} {date.day}.{date.month}.{date.year}"
    return date
