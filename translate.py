import json
import wave

import pyaudio

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

recognizer = sr.Recognizer()
microphone = sr.Microphone(device_index=config['audio']['input_device_index'])

translator = Translator()

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = config['audio']['sample_rate']
CHUNK = config['audio']['chunk_size']
WAV_OUTPUT_FILENAME = config['recording']['wav_output_filename']

tts = TTS(model_name=config['tts']['model_name'], gpu=config['tts']['use_gpu'])
tts.to(config['tts']['gpu_accelerator'] if config['tts']['use_gpu'] else 'cpu')


a


def play_audio(file):
    p = pyaudio.PyAudio()
    wf = wave.open(file, 'rb')
    print(f"Файл '{file}' успешно открыт.")

    sample_rate = wf.getframerate()
    print(f"Частота дискретизации: {sample_rate}")

    if sample_rate not in [44100, 48000]:
        print(f"Недопустимая частота дискретизации: {sample_rate}. Используйте 44100 Гц.")
        sample_rate = 24000

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=sample_rate,
                    output=True)

    data = wf.readframes(CHUNK)
    while data:
        stream.write(data)
        data = wf.readframes(CHUNK)

    stream.stop_stream()
    stream.close()
    p.terminate()
    print(f"Аудио из '{file}' успешно воспроизведено.")




if __name__ == "__main__":
    while True:
        translate_speech()
