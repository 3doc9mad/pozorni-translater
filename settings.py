import json
import tkinter as tk
from tkinter import ttk, messagebox

import pyaudio


# Функция для загрузки конфигурации
def load_config():
    with open('config.json', 'r') as config_file:
        return json.load(config_file)


# Функция для сохранения конфигурации
def save_config(config):
    with open('config.json', 'w') as config_file:
        json.dump(config, config_file, indent=4)


# Функция для получения доступных устройств
def get_audio_devices():
    p = pyaudio.PyAudio()
    devices = []
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        devices.append((i, info['name'], info['maxInputChannels']))
    p.terminate()
    return devices


# Функция для обновления списка устройств
def update_device_list():
    devices = get_audio_devices()
    input_device_combobox['values'] = [f"{name} (ID: {id})" for id, name, channels in devices if channels > 0]
    output_device_combobox['values'] = [f"{name} (ID: {id})" for id, name, channels in devices if channels > 0]


# Функция для сохранения настроек
def save_settings():
    try:
        config['audio']['input_device_index'] = int(input_device_combobox.get().split(" (ID: ")[-1][:-1])
        config['audio']['output_device_index'] = int(output_device_combobox.get().split(" (ID: ")[-1][:-1])
        config['translation']['source_language'] = language_codes[source_language_entry.get()]
        config['translation']['destination_language'] = language_codes[destination_language_entry.get()]
        config['tts']['use_gpu'] = gpu_var.get()
        config['tts']['gpu_accelerator'] = gpu_accelerator_entry.get()

        save_config(config)
        messagebox.showinfo("Сохранение", "Настройки успешно сохранены!")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось сохранить настройки: {e}")


# Загрузка конфигурации
config = load_config()

# Создание основного окна
root = tk.Tk()
root.title("Настройки переводчика")
language_codes = {
    'Русский': 'ru',
    'Английский': 'en',
    'Испанский': 'es',
    'Французский': 'fr',
    'Немецкий': 'de',
    'Итальянский': 'it',
    'Португальский': 'pt',
    'Польский': 'pl',
    'Венгерский': 'hu',
    'Турецкий': 'tr',
    'Голландский': 'nl',
    'Чешский': 'cs',
    'Арабский': 'ar',
    'Китайский': 'zh-cn',
    'Японский': 'ja',
    'Корейский': 'ko',
    'Хинди': 'hi',
}

# Создание виджетов
ttk.Label(root, text="Выберите устройство ввода:").grid(column=0, row=0, padx=10, pady=10)
input_device_combobox = ttk.Combobox(root)
input_device_combobox.grid(column=1, row=0, padx=10, pady=10)

ttk.Label(root, text="Выберите устройство вывода:").grid(column=0, row=1, padx=10, pady=10)
output_device_combobox = ttk.Combobox(root)
output_device_combobox.grid(column=1, row=1, padx=10, pady=10)

# Создание виджетов
ttk.Label(root, text="Язык источника:").grid(column=0, row=2, padx=10, pady=10)
source_language_entry = ttk.Combobox(root, values=list(language_codes.keys()))
source_language_entry.grid(column=1, row=2, padx=10, pady=10)
source_language_entry.set(
    [key for key, value in language_codes.items() if value == config['translation']['source_language']][0])

ttk.Label(root, text="Язык назначения:").grid(column=0, row=3, padx=10, pady=10)
destination_language_entry = ttk.Combobox(root, values=list(language_codes.keys()))
destination_language_entry.grid(column=1, row=3, padx=10, pady=10)
destination_language_entry.set(
    [key for key, value in language_codes.items() if value == config['translation']['destination_language']][0])

gpu_var = tk.BooleanVar(value=config['tts']['use_gpu'])
gpu_checkbox = ttk.Checkbutton(root, text="Использовать GPU", variable=gpu_var)
gpu_checkbox.grid(column=0, row=4, columnspan=2, padx=10, pady=10)

ttk.Label(root, text="Ускоритель GPU:").grid(column=0, row=5, padx=10, pady=10)
gpu_accelerator_entry = ttk.Entry(root)
gpu_accelerator_entry.grid(column=1, row=5, padx=10, pady=10)
gpu_accelerator_entry.insert(0, config['tts']['gpu_accelerator'])

save_button = ttk.Button(root, text="Сохранить настройки", command=save_settings)
save_button.grid(column=0, row=6, columnspan=2, padx=10, pady=10)

# Обновление списка устройств
update_device_list()

# Запуск основного цикла
root.mainloop()
