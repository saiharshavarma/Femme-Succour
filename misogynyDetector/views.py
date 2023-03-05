from django.shortcuts import render
from .models import MeetingRecording
from accounts.models import Profile
import speech_recognition as sr
import moviepy.editor as mp
from pydub import AudioSegment
from pydub.silence import split_on_silence
from sklearn.feature_extraction.text import TfidfVectorizer
from PyPDF2 import PdfReader
from misogynyDetector import predict
import os
import pickle
import numpy
import nltk

r = sr.Recognizer()

# Create your views here.
def uploadVideo(request):
    if request.method == "POST":
        profile = Profile.objects.get(user=request.user.id)
        recording = request.FILES['recording']
        try:
            os.remove('media/recording.pdf')
        except:
            pass
        record = MeetingRecording.objects.create(profile=profile, recording=recording, transcript="")
        record.save()
        os.rename(('media/'+recording.name).replace(" ", "_"), 'media/recording.pdf')
        readPDF(request, record)
    return render(request, "misogyny.html")

def getTranscript(record):
    video_path = "media/recording.mp4"
    video_clip = mp.VideoFileClip(video_path)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile("transcript.wav")
    transcript = get_large_audio_transcription()
    # with sr.AudioFile("transcript.wav") as source:
    #     audio_data = recognizer.record(source)
    # transcript = recognizer.recognize_google(audio_data)
    # print(transcript)
    record.transcript = transcript
    record.save()
    return

def get_large_audio_transcription():
    path = "transcript.wav"
    sound = AudioSegment.from_wav(path)
    chunks = split_on_silence(sound,
        min_silence_len = 500,
        silence_thresh = sound.dBFS-14,
        keep_silence=500,
    )
    folder_name = "audio-chunks"
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    for i, audio_chunk in enumerate(chunks, start=1):
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            try:
                text = r.recognize_google(audio_listened)
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                print(chunk_filename, ":", text)
                whole_text += text
    
    print("Whole text:", whole_text)
    return whole_text

def miogyny(request, record):
    pickled_model = pickle.load(open('misogynyDetector/detector.pkl', 'rb'))
    transcript = record
    toxicity = predict.xyz(record)
    # vectorizer = TfidfVectorizer()
    # new_vector = vectorizer.transform([transcript])
    # toxicity = pickled_model.predict(new_vector)[0]
    print(toxicity)
    return render(request, "home.html")

def readPDF(request, record):
    reader = PdfReader('media/recording.pdf')
    text = ""
    for pageNo in range(len(reader.pages)):
        page = reader.pages[pageNo]
        text += page.extract_text()
    text = text.replace("s***", "shit")
    print(text)
    miogyny(request, text)
    return render(request, "leave.html")