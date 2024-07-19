# import libraries
import tkinter as tk
from tkinter import ttk
from datetime import datetime
import pytz
import speech_recognition as sr
from keras.layers import TextVectorization
import re
import requests
# import tensorflow.strings as tf_strings
import json
import string
from keras.models import load_model
from tensorflow import argmax
from keras.preprocessing.text import tokenizer_from_json
from keras.utils import pad_sequences
import numpy as np
import tensorflow as tf


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

## loading the tokenizers
model_hi = load_model('english_to_hindi_lstm_model')
# model_fr = load_model('english_to_french_lstm_model')

#load Tokenizers

with open('english_tokenizer_hindi.json') as f:
    data = json.load(f)
    english_tokenizer_hindi = tokenizer_from_json(data)

with open('hindi_tokenizer.json') as f:
    data = json.load(f)
    hindi_tokenizer = tokenizer_from_json(data)


max_decoded_sentence_length = 20
    
    
with open('sequence_length_hindi.json') as f:
    max_length_hindi = json.load(f)
    
def pad(x, length=None):
    return pad_sequences(x, maxlen=length, padding='post')

def translate_to_hindi(english_sentence):
    english_sentence = english_sentence.lower()
    
    english_sentence = english_sentence.replace(".", '')
    english_sentence = english_sentence.replace("?", '')
    english_sentence = english_sentence.replace("!", '')
    english_sentence = english_sentence.replace(",", '')
    
    english_sentence = english_tokenizer_hindi.texts_to_sequences([english_sentence])
    english_sentence = pad(english_sentence, max_length_hindi)
    
    english_sentence = english_sentence.reshape((-1,max_length_hindi))
    
    hindi_sentence = model_hi.predict(english_sentence)[0]
    
    hindi_sentence = [np.argmax(word) for word in hindi_sentence]

    hindi_sentence = hindi_tokenizer.sequences_to_texts([hindi_sentence])[0]
    
    # print("hindi translation: ", hindi_sentence)
    
    return hindi_sentence

def is_after_6pm_ist():
    ist = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(ist)
    # return current_time.hour >= 18
    return True

def capture_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    return audio

def listen_and_translate(audio=None):
    if audio is None:
        return "No audio input provided."

    recognizer = sr.Recognizer()

    try:
        english_text = recognizer.recognize_google(audio)
        print(f"You said: {english_text}")

        if not is_after_6pm_ist():
            return "Please try after 6 PM IST."

        if english_text.strip().lower()[0] in ['m', 'o']:
            return "Cannot translate words starting with 'M' or 'O'."

        url = "https://translate.googleapis.com/translate_a/single"
        params = {
            'client': 'gtx',
            'sl': 'en',  
            'tl': 'hi',  
            'dt': 't',
            'q': english_text  
        }
    
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            translation = response.json()[0][0][0]
            translated_sent = f"Hindi: {translation}"
        except Exception as e:
            translated_sent = "Error"
            
        return translated_sent

    except sr.UnknownValueError:
        return "Sorry, I couldn't understand the audio. Please try again."
    except sr.RequestError as e:
        return f"Could not request results; {e}"

def solve():
   
    instruction_label.config(text="Listening... Please speak now.")
    root.update()  # Update the GUI to show the new instruction
    audio = capture_audio()
    instruction_label.config(text="Processing...")
    root.update() 
    result = listen_and_translate(audio)    
    result_label.config(text=result)
    

root = tk.Tk()
root.title("English Audio Translator")
root.geometry("500x300")

font = ('Helvetica', 14)

input_entry = tk.Entry(root, width=80, font=font)
input_entry.pack(pady=10)

instruction_label = tk.Label(root, text="Enter sentence for English to French translation", wraplength=400, font=font)
instruction_label.pack(pady=10)

translate_button = tk.Button(root, text="Translate", command=solve, font=font)
translate_button.pack(pady=10)

result_label = tk.Label(root, text="", wraplength=400, font=font)
result_label.pack(pady=20)

instruction_label.config(text="Click the Translate button to speak")
input_entry.config(state='disabled')

root.mainloop()