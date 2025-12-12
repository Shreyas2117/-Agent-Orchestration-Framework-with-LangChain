import random
from datetime import datetime

def get_weather(location: str) -> str:
    r = abs(hash(location)) % 100
    temps = [22 + (r % 5), 25 + (r % 4), 18 + (r % 6)]
    conds = ["sunny", "partly cloudy", "rainy", "windy", "overcast"]
    temp = temps[r % len(temps)]
    cond = conds[r % len(conds)]
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    return f"Weather for {location} at {now}: {temp}°C, {cond}."
