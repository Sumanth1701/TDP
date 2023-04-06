
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

speaker_diarization("test123.wav", 2, 'English','tiny')




