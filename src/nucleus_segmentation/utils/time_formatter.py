import time


def format_elapsed_time(start_time):
    if start_time is None:
        return '00:00:00'

    elapsed = int(time.time() - start_time)
    hours, remainder = divmod(elapsed, 3600)
    minutes, seconds = divmod(remainder, 60)

    return f'{hours:02d}:{minutes:02d}:{seconds:02d}'
