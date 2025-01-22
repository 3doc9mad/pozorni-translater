import json
import queue
import threading
import speech_recognition as sr
from googletrans import Translator
from translator import listen_microphone, recognize_speech, translate_speech, text_to_speech, play_audio


def listen(audios_for_recognize, microphone, recognizer):
    audios_for_recognize.put(listen_microphone(microphone, recognizer))


def recognize(audios_for_recognize):
    while True:
        audio = audios_for_recognize.get()
        if audio is None:
            break
        global recognizer
        recognize_speech(audio)
        audios_for_recognize.task_done()


def translate(text_for_translate):
    while True:
        text = text_for_translate.get()
        if text is None:
            break
        translate_speech(text)
        text_for_translate.task_done()


def speech(text_for_speech):
    while True:
        text = text_for_speech.get()
        if text is None:
            break
        text_to_speech(text)
        text_for_speech.task_done()


def playing(audio_paths_for_playing):
    while True:
        audio_path = audio_paths_for_playing.get()
        if audio_path is None:
            break
        play_audio(audio_path)
        audio_paths_for_playing.task_done()


def start_translation_multi_thread():
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
    translator = Translator()
    microphone = sr.Microphone(device_index=config['audio']['input_device_index'])
    recognizer = sr.Recognizer()
    tts = TTS(model_name=config['tts']['model_name'], gpu=config['tts']['use_gpu'])
    tts.to(config['tts']['gpu_accelerator'] if config['tts']['use_gpu'] else 'cpu')

    audios_for_recognize = queue.Queue()
    text_for_translate = queue.Queue()
    text_for_speech = queue.Queue()
    audio_paths_for_playing = queue.Queue()

    listener_thread = threading.Thread(target=lambda microphone=microphone, recognizer=recognizer: listen())
    recognize_thread = threading.Thread(target=recognize)
    translate_thread = threading.Thread(target=translate)
    synthesizer_thread = threading.Thread(target=speech)
    play_thread = threading.Thread(target=playing)

    recognize_thread.start()
    listener_thread.start()
    recognize_thread.start()
    translate_thread.start()
    synthesizer_thread.start()
    play_thread.start()


def start_translation_one_thread():
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
    translator = Translator()
    microphone = sr.Microphone(device_index=config['audio']['input_device_index'])
    recognizer = sr.Recognizer()
    tts = TTS(model_name=config['tts']['model_name'], gpu=config['tts']['use_gpu'])
    tts.to(config['tts']['gpu_accelerator'] if config['tts']['use_gpu'] else 'cpu')

    audios_for_recognize = queue.Queue()
    text_for_translate = queue.Queue()
    text_for_speech = queue.Queue()
    audio_paths_for_playing = queue.Queue()

    listener_thread = threading.Thread(target=lambda microphone=microphone, recognizer=recognizer: listen())
    recognize_thread = threading.Thread(target=recognize)
    translate_thread = threading.Thread(target=translate)
    synthesizer_thread = threading.Thread(target=speech)
    play_thread = threading.Thread(target=playing)

    recognize_thread.start()
    listener_thread.start()
    recognize_thread.start()
    translate_thread.start()
    synthesizer_thread.start()
    play_thread.start()

def start_func():
    start_translation_thread()


