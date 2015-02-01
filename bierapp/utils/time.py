def timedelta_range(start, end, delta):
    current = start

    while current <= end:
        yield current
        current = current + delta