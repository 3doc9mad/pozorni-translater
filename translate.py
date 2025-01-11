import speech_recognition as sr
from googletrans import Translator
from TTS.api import TTS
import pyaudio
import wave

recognizer = sr.Recognizer()
microphone = sr.Microphone()

translator = Translator()

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 128
RECORD_SECONDS = 3
WAV_OUTPUT_FILENAME = "output.wav"


tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", gpu=True)
tts.to(1)
def text_to_speech(text, WAV_OUTPUT_FILENAME):
    tts.tts_to_file(text=text, file_path=WAV_OUTPUT_FILENAME, speaker_wav=['neco-arc-1.wav'], language='ru', split_sentences=True)

def play_audio(file):
        p = pyaudio.PyAudio()
        wf = wave.open(file, 'rb')
        print(f"Файл '{file}' успешно открыт.")

        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True,
                        output_device_index=11)

        data = wf.readframes(CHUNK)
        while data:
            stream.write(data)
            data = wf.readframes(CHUNK)

        stream.stop_stream()
        stream.close()
        p.terminate()
        print(f"Аудио из '{file}' успешно воспроизведено.")

def translate_speech():
    with microphone as source:
        print("Скажи что-нибудь...")
        audio = recognizer.listen(source)

    try:
        speech_text = recognizer.recognize_google(audio, language="ru-RU")
        print(f"Распознано: {speech_text}")
        dest = 'ru'
        if dest != 'ru':
            translated_text = translator.translate(speech_text, src="ru", dest=dest).text
            print(f"Перевод: {translated_text}")
        else:
            translated_text = speech_text

        text_to_speech(translated_text, WAV_OUTPUT_FILENAME)

        play_audio(WAV_OUTPUT_FILENAME)

    except sr.UnknownValueError:
        print("Не удалось распознать речь")
    except sr.RequestError as e:
        print(f"Ошибка сервиса распознавания речи: {e}")

if __name__ == "__main__":
    while True:
        translate_speech()












