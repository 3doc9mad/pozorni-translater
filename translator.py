import json
import random
import wave

import pyaudio
import speech_recognition as sr
from TTS.api import TTS
from googletrans import Translator

from utils import log_message


def listen_microphone(microphone, recognizer):
    with microphone as source:
        log_message("Скажи что-нибудь...")
        return recognizer.listen(source)


def recognize_speech(audio):
    if not config['interface']['multiprocessing']:
        pass

    try:
        speech_text = recognizer.recognize_google(audio, language=config['translation']['source_language'])
        return speech_text
    except sr.UnknownValueError:
        log_message("Не удалось распознать речь")
    except sr.RequestError as e:
        log_message(f"Ошибка сервиса распознавания речи: {e}")


def translate_speech(text, translator):
    if config['translation']['destination_language'] != config['translation']['source_language']:
        translated_text = translator.translate(text, src=config['translation']['source_language'],
                                               dest=config['translation']['destination_language']).text
        print(f"Перевод: {translated_text}")
    else:
        translated_text = text
    return translated_text


def text_to_speech(text, tts):
    code = ''.join(random.choice(string.ascii_letters) for _ in range(10))
    file_path = f'/output/{config['recording']['wav_output_filename']}_{code}.wav'
    try:
        tts.tts_to_file(
            text=text,
            file_path=file_path,
            speaker_wav=config['tts']['speaker_wav'],
            language=config['translation']['destination_language'],
            split_sentences=True,
            speed=config['tts']['speed']
        )
        return file_path
    except Exception as e:
        print(f"Ошибка при синтезе речи: {e}")


def play_audio(file):
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    p = pyaudio.PyAudio()
    wf = wave.open(file, 'rb')
    print(f"Файл '{file}' успешно открыт.")

    sample_rate = wf.getframerate()
    print(f"Частота дискретизации: {sample_rate}")

    if sample_rate not in [44100, 48000]:
        print(f"Недопустимая частота дискретизации: {sample_rate}. Используйте 44100 Гц.")
        sample_rate = 44100

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=sample_rate,
                    output=True)

    data = wf.readframes(config['audio']['chunk_size'])
    while data:
        stream.write(data)
        data = wf.readframes(config['audio']['chunk_size'])

    stream.stop_stream()
    stream.close()
    p.terminate()
    print(f"Аудио из '{file}' успешно воспроизведено.")


def translate_queue(microphone, recognizer, translator, tts):
    play_audio(
        text_to_speech(
            translate_speech(
                recognize_speech(
                    listen_microphone(microphone, recognizer)
                ),
            translator),
        tts)
    )


def main():
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
    translator = Translator()
    microphone = sr.Microphone(device_index=config['audio']['input_device_index'])
    recognizer = sr.Recognizer()
    tts = TTS(model_name=config['tts']['model_name'], gpu=config['tts']['use_gpu'])
    tts.to(config['tts']['gpu_accelerator'] if config['tts']['use_gpu'] else 'cpu')
    while True:
        translate_queue(microphone, recognizer, translator, tts)


if __name__ == '__main__':
    main()
