from openai import OpenAI
import os
import re
from pydub import AudioSegment

os.environ['OPENAI_API_KEY'] = '*****'  # openai api key
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))


### ATTEMPTS TO TRANSCRIBE LYRICS FROM AUDIO INPUT
def transcribe(file: str, language: str, begin_vocals=0) -> list[str]: 
    mp3 = AudioSegment.from_mp3(file)
    mp3[begin_vocals:].export('resursi/temp.mp3', format='mp3')
    audio = open('resursi/temp.mp3', 'rb')
    
    transcription = ''
    
    if language == 'en':
        transcription = client.audio.transcriptions.create(
            file=audio,
            model='whisper-1',
            language=language,
            response_format='text',
        )
        
    else:
        transcription = client.audio.translations.create(
            file=audio,
            model='whisper-1',
            response_format='text',
            timeout=150
        )
    
    print(transcription)
    
    return re.sub(r'[^\w\s]', ' ', transcription).split()


### EXPORT MP3 TO WAV
def mp3_to_wav(file: str):
    AudioSegment.from_mp3(file).export('resursi/input.wav', format='wav')


### EXPORT WAV TO MP3
def wav_to_mp3(file: str):
    AudioSegment.from_wav(file).export('resursi/input.mp3', format='mp3')