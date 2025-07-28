import wave
import pyaudio
import speech_recognition as sr
from TTS.api import TTS
from googletrans import Translator
'''
по идее это нужно поменять, но так как консольная версия будет
мало кому интересна - я это тут оставлю
'''

from utils import log_message, send_status, config, send_translate_text, send_recognize_text, id_generator


def listen_microphone(microphone, recognizer):
    with microphone as source:
        log_message("Скажи что-нибудь...")
        send_status('listen')
        recognizer.adjust_for_ambient_noise(source, duration=1)
        recognizer.pause_threshold = 2
        recognizer.phrase_time_limit = 10
        # recognizer.dynamic_energy_threshold = True
        '''
        dynamic_energy_threshold - эта штука очень странно работает,
        по хорошему её надо бы включать, но у меня микрофон такое себе,
        так что когда будет возможность потестить на другом - тогда и посмотрим...
        '''
        try:
            return recognizer.listen(source)
        except Exception as e:
            print(f"Ошибка при прослушивании микрофона: {e}")


def recognize_speech(audio, recognizer):
    send_status('recognize')
    try:
        speech_text = recognizer.recognize_google(audio, language=config['translation']['source_language'])
        send_recognize_text(speech_text)
        return speech_text
    except sr.UnknownValueError:
        log_message("Не удалось распознать речь")
    except sr.RequestError as e:
        log_message(f"Ошибка сервиса распознавания речи: {e}")


def translate_speech(text, translator):
    send_status('translate')
    if config['translation']['destination_language'] != config['translation']['source_language']:
        translated_text = translator.translate(text,
                                               src=config['translation']['source_language'],
                                               dest=config['translation']['destination_language'])
        '''
        раньше использовал библиотеку от google - вроде одно время (довольно продолжительное) она работала,
        но я хз че там к чему (и разбираться лень), она, тип, теперь асинхронная (а может и всегда была такой),
        поэтому перешел на deep_translator, там по идее не так нужно вызывать translate, но оно вроде работает так
        '''
        translated_text = translated_text
    else:
        translated_text = text
    send_translate_text(translated_text)
    return translated_text


def text_to_speech(text, tts):
    send_status('text_to_speech')
    file_path = f'output/{config['recording']['wav_output_filename']}{id_generator()}.wav'
    '''
    в одно-поточном режиме генерировать id не нужно, т.к. зачем?
    в много-поточном по идее надо, но речь синтезируется медленнее чем воспроизводится, 
    но возможно когда-нибудь это будет наоборот, так что оставим
    '''
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
    send_status('play_audio')
    p = pyaudio.PyAudio()
    wf = wave.open(file, 'rb')
    sample_rate = wf.getframerate()
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
    # консольный вариант программы
    # конечно он уже не имеет первоначальный вид,
    # но он может использоваться для дебага именно переводчика
    microphone = sr.Microphone(device_index=config['audio']['input_device_index'])
    recognizer = sr.Recognizer()

    translator = Translator()

    tts = TTS(model_name=config['tts']['model_name'], gpu=config['tts']['use_gpu'])
    tts.to(config['tts']['gpu_accelerator'] if config['tts']['use_gpu'] else 'cpu')
    while True:
        translate_queue(microphone, recognizer, translator, tts)


if __name__ == '__main__':
    main()
