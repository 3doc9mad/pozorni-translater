import queue
import threading

import speech_recognition as sr
from TTS.api import TTS
from deep_translator import GoogleTranslator

from translator import listen_microphone, recognize_speech, translate_speech, text_to_speech, play_audio
from utils import config, send_status

'''
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
    translator = GoogleTranslator(source=config['translation']['source_language'],
                                  target=config['translation']['destination_language'])
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
    '''
# это выглядит очень нездорово, я, честно сказать, не сильно разобрался в этом,
# но имеем, что имеем...
#
# ps прошу меня не осуждать я только учусь + вообще не хотел это писать
'''
global text_for_translate
global text_for_speech
global audio_paths_for_playing
audios_for_recognize = queue.Queue()
text_for_translate = queue.Queue()
text_for_speech = queue.Queue()
audio_paths_for_playing = queue.Queue()
'''


class MultiThreadTranslation:
    def __init__(self):
        self.microphone = sr.Microphone(device_index=config['audio']['input_device_index'])
        self.recognizer = sr.Recognizer()

        self.translator = GoogleTranslator(source=config['translation']['source_language'],
                                           target=config['translation']['destination_language'])

        self.tts = TTS(model_name=config['tts']['model_name'], gpu=config['tts']['use_gpu'])
        self.tts.to(config['tts']['gpu_accelerator'] if config['tts']['use_gpu'] else 'cpu')
        self.thread_work = False
        self.audios_for_recognize = queue.Queue()
        self.text_for_translate = queue.Queue()
        self.text_for_speech = queue.Queue()
        self.audio_paths_for_playing = queue.Queue()

        self.listener_thread = threading.Thread(target=self.listen)
        self.recognize_thread = threading.Thread(target=self.recognize)
        self.translate_thread = threading.Thread(target=self.translate)
        self.synthesizer_thread = threading.Thread(target=self.speech)
        self.play_thread = threading.Thread(target=self.playing)
        self.full_translate_thread = threading.Thread(target=self.full_translate)

    def start_translation_multi_thread(self):
        self.thread_work = True
        self.listener_thread.start()
        self.recognize_thread.start()
        self.translate_thread.start()
        self.synthesizer_thread.start()
        self.play_thread.start()

    def start_translation_one_thread(self):
        send_status('loading', self.stop_translation)
        self.thread_work = True
        self.full_translate_thread.start()

    def stop_translation(self):
        send_status('stopped', self.start_translation_one_thread)
        self.thread_work = False

    def full_translate(self):
        while True:
            if not self.thread_work:
                return
            text = recognize_speech(
                listen_microphone(self.microphone, self.recognizer),
                self.recognizer)
            if text is None:
                continue
            play_audio(
                text_to_speech(
                    translate_speech(
                        text, self.translator),
                    self.tts
                )
            )

    def listen(self):
        while True:
            if not self.thread_work:
                return
            self.audios_for_recognize.put(
                listen_microphone(
                    self.microphone, self.recognizer
                )
            )

    def recognize(self):
        while True:
            if not self.thread_work:
                return
            audio = self.audios_for_recognize.get()
            if audio is None:
                break
            text = recognize_speech(audio, self.recognizer)
            self.text_for_translate.put(text)
            print('text recognized')
            self.audios_for_recognize.task_done()

    def translate(self):
        translator = GoogleTranslator(source=config['translation']['source_language'],
                                      target=config['translation']['destination_language'])
        print('translate is start')
        while True:
            if not self.thread_work:
                return
            text = self.text_for_translate.get()
            print('get text for translate')
            if text is None:
                print('text is none')
                break
            self.text_for_speech.put(translate_speech(text, translator))
            self.text_for_translate.task_done()

    def speech(self):
        tts = TTS(model_name=config['tts']['model_name'], gpu=config['tts']['use_gpu'])
        tts.to(config['tts']['gpu_accelerator'] if config['tts']['use_gpu'] else 'cpu')
        print('tts started')
        while True:
            if not self.thread_work:
                return
            text = self.text_for_speech.get()
            if text is None:
                break
            self.audio_paths_for_playing.put(text_to_speech(text, tts))
            self.text_for_speech.task_done()

    def playing(self):
        while True:
            if not self.thread_work:
                return
            audio_path = self.audio_paths_for_playing.get()
            if audio_path is None:
                break
            play_audio(audio_path)
            self.audio_paths_for_playing.task_done()
