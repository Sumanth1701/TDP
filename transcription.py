def speaker_diarization(path,number,language,size):
    path = path

    num_speakers = number #@param {type:"integer"}


    language = language #@param ['any', 'English']

    model_size = size #@param ['tiny', 'base', 'small', 'medium', 'large']


    model_name = model_size
    if language == 'English' and model_size != 'medium':
      model_name += '.en'



    import whisper
    
    import re
    from datetime import datetime, timedelta
    
    from pydub import AudioSegment
    from pydub.playback import play
    import pyaudio

    import subprocess

    import torch
    import pyannote.audio
    from pyannote.audio.pipelines.speaker_verification import PretrainedSpeakerEmbedding
    embedding_model = PretrainedSpeakerEmbedding( "speechbrain/spkrec-ecapa-voxceleb",device=torch.device("cpu"))

    from pyannote.audio import Audio
    from pyannote.core import Segment

    import wave
    import contextlib

    from sklearn.cluster import AgglomerativeClustering
    import numpy as np
    
    if path[-3:] != 'wav':
      subprocess.call(['ffmpeg', '-i', path, 'audio.wav', '-y'])
      path = 'audio.wav'

    model = whisper.load_model(model_size)

    result = model.transcribe(path)
    segments = result["segments"]

    with contextlib.closing(wave.open(path,'r')) as f:
      frames = f.getnframes()
      rate = f.getframerate()
      duration = frames / float(rate)

    audio = Audio()

    def segment_embedding(segment):
      start = segment["start"]
      # Whisper overshoots the end timestamp in the last segment
      end = min(duration, segment["end"])
      clip = Segment(start, end)
      waveform, sample_rate = audio.crop(path, clip)
      return embedding_model(waveform[None])

    embeddings = np.zeros(shape=(len(segments), 192))
    for i, segment in enumerate(segments):
      embeddings[i] = segment_embedding(segment)

    embeddings = np.nan_to_num(embeddings)

    clustering = AgglomerativeClustering(num_speakers).fit(embeddings)
    labels = clustering.labels_
    for i in range(len(segments)):
      segments[i]["speaker"] = 'SPEAKER ' + str(labels[i] + 1)

    def time(secs):
      return timedelta(seconds=round(secs))

    f = open("transcript.txt", "w")
    speakers = []
    distinct_speakers = []
    for (i, segment) in enumerate(segments):
      if i == 0 or segments[i - 1]["speaker"] != segment["speaker"]:
        f.write("\n" + segment["speaker"] + ' ' + str(time(segment["start"])) + '\n')
        temp1 = time(segment["start"])
        temp2 = time(segment["end"])
        speakers.append(segment["speaker"])
      f.write(segment["text"][1:] + ' ')
      if(speakers.count(segment["speaker"]) == 1):
          distinct_speakers.append(segment["speaker"])
          distinct_speakers.append(segment["start"])
          distinct_speakers.append(segment["end"])
          
    
    f.close()

    

    print(open("transcript.txt",'r').read())

    print()

    

    # Regex pattern to match the speaker and dialogue
    pattern = re.compile(r'SPEAKER (\d+) 0:(\d\d):(\d\d)\n(.*)')

    # Open the file for reading
    with open("transcript.txt", "r") as f:
        content = f.read()
        
    # Dictionary to store the dialogues for each speaker
    dialogues = {}

    # Loop through all the matches in the content
    for match in re.finditer(pattern, content):
        speaker = "SPEAKER " + str(match.group(1))
        #time = "0:" + match.group(2) + ":" + match.group(3)
        dialogue = match.group(4)
        
        # If the speaker is not already in the dictionary, add it and start a list
        if speaker not in dialogues:
            dialogues[speaker] = []
        
        # Add the dialogue to the list for this speaker
        dialogues[speaker].append(dialogue)
        
    # Write the dialogues for each speaker to a separate file
    #for speaker, speaker_dialogues in dialogues.items():
        #with open(speaker + ".txt", "w") as f:
            #f.write("\n".join(speaker_dialogues))

    
    audio_file = AudioSegment.from_file(path, format="wav")
    speaker_names=[]
    val = len(distinct_speakers)//3
    for i in range(val):
      j = 1+ i*3
      start_time_str= str(distinct_speakers[j])
      end_time_str= str(distinct_speakers[j+1])
      start_time = float(start_time_str)
      end_time = float(end_time_str)
      segment = audio_file[start_time*1000:end_time*1000]
      p = pyaudio.PyAudio()
      device_index = p.get_default_output_device_info()['index']
      stream = p.open(output_device_index=device_index, format=pyaudio.paInt16, channels=2, rate=44100, output=True)
      stream.write(segment.raw_data)
      stream.stop_stream()
      stream.close()
      p.terminate()

      import random

      # List of first names and last names
      first_names = ["Emma", "Liam", "Ava", "Noah", "Sophia", "William", "Isabella", "James", "Mia", "Benjamin", "Charlotte", "Oliver", "Amelia", "Evelyn", "Henry", "Harper", "Ella", "Alexander", "Abigail", "Michael"]
      last_names = ["Smith", "Johnson", "Brown", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Perez", "Taylor", "Anderson", "Wilson", "Jackson", "White", "Harris", "Martin", "Thompson"]

      
      def generate_name():
          first_name = random.choice(first_names)
          last_name = random.choice(last_names)
          return f"{first_name} {last_name}"

      name = generate_name()

      speaker_names.append(name)
      export_file = name +".mp3"
      segment.export(export_file, format="mp3")
    

    for i in range(val):
       distinct_speakers[i*3] = speaker_names[i]
    
    print(distinct_speakers)
    print(speaker_names)
    
    i = 0

    for speaker, speaker_dialogues in dialogues.items():
        with open(speaker_names[i] + ".txt", "w") as f:
          f.write("\n".join(speaker_dialogues))
        i= i+1

        

speaker_diarization("test123.wav", 2, 'English','tiny')



