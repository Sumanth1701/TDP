import datetime

def add_time(start_time, add_hrs=0, add_mins=0, add_secs=0):
    # Convert start time to datetime object
    dt = datetime.datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%SZ')

    # Add hours, minutes, and seconds
    dt += datetime.timedelta(hours=add_hrs, minutes=add_mins, seconds=add_secs)

    # Convert datetime object back to ISO time format
    iso_time_with_hms = dt.strftime('%Y-%m-%dT%H:%M:%SZ')

    return iso_time_with_hms


start_time = '2023-03-05T01:17:19Z'
new_time = add_time(start_time, add_mins=1, add_secs=32)
print(new_time)
