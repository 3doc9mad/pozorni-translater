import pyaudio
import numpy as np

def get_noise_level(duration=1):
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Запись...")

    frames = []
    for _ in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Запись завершена.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    audio_data = np.frombuffer(b''.join(frames), dtype=np.int16)
    noise_level_rms = np.sqrt(np.mean(audio_data ** 2))
    reference = 0.00002
    if noise_level_rms > 0:
        noise_level_db = 20 * np.log10(noise_level_rms / reference)
    else:
        noise_level_db = -np.inf

    return noise_level_db


if __name__ == "__main__":
    noise_level = []
    for i in range(5):
        noise_level.append(get_noise_level())
    print(f"Уровень шума: {noise_level}")
