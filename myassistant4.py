import speech_recognition as sr
import pyttsx3
import datetime

import requests
from weatherKey import KEY_WEATHER #You need to get a key 

es = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-ES_HELENA_11.0"


def audioToText():
    r = sr.Recognizer() #El objeto con el que trabajaremos

    with sr.Microphone() as source:
        r.pause_threshold = 1 #Una pausa antes del speech recognition

        print("Waiting for speech recognition...")

        audio = r.listen(source)

        try:
            text = r.recognize_google(audio,language="es")
            print("Speech recognition triggered: ", text)

            return text
        
        except sr.UnknownValueError: #No se entiende lo que decimos
            print("I can't recognize speech recognition")
            return "Error"
        except sr.RequestError: #Falla por hardware
            print("Hardware error")
            return "Error"
        except:
            print("Error!")
            return "Error"
        
def textToAudio(text):

    engine = pyttsx3.init()

    engine.setProperty("rate", 190)

    engine.setProperty("volume",1)

    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[0].id)

    engine.say(text) 

    engine.runAndWait()

def regards():
    hour = datetime.datetime.now()

    if 6 <= hour.hour < 14:
        now = "Buenos dias"
    elif 14 <= hour.hour < 20:
        now = "Buenas tardes"
    else:
        now = "Buenas noches"
    
    textToAudio(f"{now}, soy Bob tu asistente personal")

#FUNCIÓN PRINCIPAL
def mainFunction():
    regards()

    while True:
        petition = audioToText().lower()
        print(petition)

        if "dime la temperatura de" in petition:
            textToAudio("Midiendo la temperatura...")
            petition = petition.replace("dime la temperatura de", "")
            url = f"https://api.openweathermap.org/data/2.5/weather?q={petition}&appid={KEY_WEATHER}&units=metric"
            result = requests.get(url)
            data = result.json() #Pasarlo a json
            temperatura = data["main"]["temp"]
            temperatura_min = data["main"]["temp_min"]
            temperatura_max = data["main"]["temp_max"]
            humedad = data ["main"]["humidity"]

            textToAudio(f"La temperatura de {petition} es de {temperatura} grados, con un minimo de {temperatura_min} y un máximo de {temperatura_max}, la humedad es de {humedad}")

        elif "20 40 76 b15" in petition:
            textToAudio("Abortando mision")
            break

        else:
            textToAudio("No entiendo")


mainFunction()
