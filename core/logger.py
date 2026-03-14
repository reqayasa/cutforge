import datetime

def log(message):
    ts = datetime.datetime.now()
    print(f"[{ts}] {message}")