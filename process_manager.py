from utils import config, send_status
import queue
import threading

import speech_recognition as sr
from TTS.api import TTS
from googletrans import Translator
from translator import listen_microphone, recognize_speech, translate_speech, text_to_speech, play_audio


def listen():
    microphone = sr.Microphone(device_index=config['audio']['input_device_index'])
    recognizer = sr.Recognizer()
    audios_for_recognize.put(listen_microphone(microphone, recognizer))


def recognize():
    recognizer = sr.Recognizer()
    while True:
        audio = audios_for_recognize.get()
        if audio is None:
            break
        recognize_speech(audio, recognizer)
        audios_for_recognize.task_done()


def translate():
    translator = Translator()
    while True:
        text = text_for_translate.get()
        if text is None:
            break
        translate_speech(text, translator)
        text_for_translate.task_done()


def speech():
    tts = TTS(model_name=config['tts']['model_name'], gpu=config['tts']['use_gpu'])
    tts.to(config['tts']['gpu_accelerator'] if config['tts']['use_gpu'] else 'cpu')
    while True:
        text = text_for_speech.get()
        if text is None:
            break
        text_to_speech(text, tts)
        text_for_speech.task_done()


def playing(audio_paths_for_playing):
    while True:
        audio_path = audio_paths_for_playing.get()
        if audio_path is None:
            break
        play_audio(audio_path)
        audio_paths_for_playing.task_done()


def start_translation_multi_thread():
    global audios_for_recognize, text_for_translate, text_for_speech, audio_paths_for_playing
    audios_for_recognize = queue.Queue()
    text_for_translate = queue.Queue()
    text_for_speech = queue.Queue()
    audio_paths_for_playing = queue.Queue()

    listener_thread = threading.Thread(target=listen)
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

    send_status('loading')
    translator = Translator()
    microphone = sr.Microphone(device_index=config['audio']['input_device_index'])
    recognizer = sr.Recognizer()
    tts = TTS(model_name=config['tts']['model_name'], gpu=config['tts']['use_gpu'])
    tts.to(config['tts']['gpu_accelerator'] if config['tts']['use_gpu'] else 'cpu')
    while True:
        text = recognize_speech(
            listen_microphone(microphone, recognizer),
            recognizer)
        if text is None:
            continue
        play_audio(
            text_to_speech(
                translate_speech(
                    text, translator),
                tts
            )
        )


