import datetime

iso_time = '2023-04-06T12:30:00.000Z'  # Replace with your ISO time
hours = 2  # Replace with the number of hours you want to add
minutes = 15  # Replace with the number of minutes you want to add
seconds = 30  # Replace with the number of seconds you want to add

# Convert ISO time to datetime object
dt = datetime.datetime.fromisoformat(iso_time)

# Add hours, minutes, and seconds
dt += datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)

# Convert datetime object back to ISO time format
iso_time_with_hms = dt.isoformat(timespec='milliseconds') + 'Z'

print(iso_time_with_hms)
