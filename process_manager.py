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
    while True:
        audios_for_recognize.put(listen_microphone(microphone, recognizer))


def recognize():
    recognizer = sr.Recognizer()
    while True:
        audio = audios_for_recognize.get()
        if audio is None:
            break
        text = recognize_speech(audio, recognizer)
        text_for_translate.put(text)
        print('text recognized')
        audios_for_recognize.task_done()


def translate():
    translator = Translator()
    print('translate is start')
    while True:
        text = text_for_translate.get()
        print('get text for translate')
        if text is None:
            print('text is none')
            break
        text_for_speech.put(translate_speech(text, translator))
        text_for_translate.task_done()


def speech():
    tts = TTS(model_name=config['tts']['model_name'], gpu=config['tts']['use_gpu'])
    tts.to(config['tts']['gpu_accelerator'] if config['tts']['use_gpu'] else 'cpu')
    print('tts started')
    while True:
        text = text_for_speech.get()
        if text is None:
            break
        audio_paths_for_playing.put(text_to_speech(text, tts))
        text_for_speech.task_done()


def playing():
    while True:
        audio_path = audio_paths_for_playing.get()
        if audio_path is None:
            break
        play_audio(audio_path)
        audio_paths_for_playing.task_done()


def start_translation_multi_thread():
    global audios_for_recognize
    global text_for_translate
    global text_for_speech
    global audio_paths_for_playing
    audios_for_recognize = queue.Queue()
    text_for_translate = queue.Queue()
    text_for_speech = queue.Queue()
    audio_paths_for_playing = queue.Queue()

    listener_thread = threading.Thread(target=listen)
    recognize_thread = threading.Thread(target=recognize)
    translate_thread = threading.Thread(target=translate)
    synthesizer_thread = threading.Thread(target=speech)
    play_thread = threading.Thread(target=playing)

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

def stop_translation_one_thread():
    listener_thread.stop()
    recognize_thread.stop()
    translate_thread.stop()
    synthesizer_thread.stop()
    play_thread.stop()