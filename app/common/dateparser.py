import datetime


def parse_date(
    timestamp: float,
    show_time: bool = False,
    show_day_name: bool = True,
    show_numeric: bool = True,
    time_sep_symbol: str = "",
):
    date = datetime.datetime.fromtimestamp(timestamp)
    day_name = f"{['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][date.weekday()]} "
    numeric = f"{date.day}.{date.month}.{date.year}"
    time = f"{date.hour:0>2}:{date.minute:0>2}{(' ' + time_sep_symbol) if len(time_sep_symbol) else ''} "
    p_date = f"{time if show_time else ''}{day_name if show_day_name else ''}{numeric if show_numeric else ''}"
    return p_date
