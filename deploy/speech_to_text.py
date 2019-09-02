# SpeechRecognition
# type : .wav

import speech_recognition as sr
from pydub import AudioSegment
from langconv import Converter
import os

def convert_audio_extension(file_name): # convert file from .m4a to .wav   
    print('音訊檔案位置: ', file_name)
    sound = AudioSegment.from_file(file_name, format="m4a")
    output_filename = "tmp.wav"
    sound.export(output_filename, format="wav")
    try:
        os.remove(file_name)
    except:
        print('remove audio file error')
    return output_filename
    

def speech_to_text(file_name): # function for audio recognition
    wav_file_name = convert_audio_extension(file_name)

    ''' File Type : .wav '''
    r = sr.Recognizer()
    
    harvard = sr.AudioFile(wav_file_name)
    
    try:
        with harvard as source:
            audio = r.record(source)
            recognize_text = r.recognize_google(audio, language = 'zh-tw')
            recognize_text = Converter('zh-hant').convert(recognize_text)
    except:
        recognize_text = "無法辨識內容"
    return recognize_text