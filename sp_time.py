import re
from datetime import datetime, timedelta
import pytz

# read in the transcript file
with open('transcript.txt', 'r') as f:
    transcript = f.read()

# find all occurrences of speaker and their corresponding start times
matches = re.findall(r'(\bSPEAKER \d\b)\s(\d+:\d+:\d+)', transcript)

# arbitrary date and time in UTC timezone
arbitrary_time = datetime(2023, 3, 5, 1, 17, 19, tzinfo=pytz.UTC)
sp_time =[]
# loop through the matches and calculate the time period for each speaker
for i, match in enumerate(matches):
    try:
        speaker, start_time = match
        start_time = datetime.strptime(start_time, '%H:%M:%S')
        end_time = matches[i+1][1] if i+1 < len(matches) else re.findall(r'(\d+:\d+:\d+)\n?\Z', transcript)[-1]
        end_time = datetime.strptime(end_time, '%H:%M:%S')
        time_period = (end_time - start_time).total_seconds()
        speaker_start_time = arbitrary_time + timedelta(seconds=start_time.second, minutes=start_time.minute, hours=start_time.hour)
        speaker_end_time = arbitrary_time + timedelta(seconds=end_time.second, minutes=end_time.minute, hours=end_time.hour)
        a = str(f"{speaker}  {speaker_start_time.isoformat()} - {speaker_end_time.isoformat()}")
        sp_time.append(a)
    except:
        print("index error")

print(sp_time)