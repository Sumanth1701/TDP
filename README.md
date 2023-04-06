# Work Flow
## YoutubeData.py
Give your Youtube API, Video ID
Generates the start and end time of the video
Generates the JSON format of data such as *View count*, *Like count*, *Comments* along with *Timestamp*.

## Transcription.py

Takes the audio file of the video, model size and number of speakers
Generates the *Transcription.txt* file.

## TimeExtraction.py

Takes the transcript.txt file in and changes the raw time into real time
Generates the *start point* and *end point* of each speaker.

