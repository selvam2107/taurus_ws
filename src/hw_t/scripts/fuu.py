from datetime import datetime

now = datetime.now()
seconds_today = now.hour * 3600 + now.minute * 60 + now.second

print(now)
