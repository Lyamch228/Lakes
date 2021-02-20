def uptime(dt):
    days = dt.days
    hours, r = divmod(dt.seconds, 3600)
    minutes, seconds = divmod(r, 60)

    return f"• Days: `{days}` | Hours: `{hours}` | Minutes: `{minutes}` | Seconds: `{seconds}`"
