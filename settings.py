import tkinter as tk
from tkinter import ttk, filedialog

class SettingsWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Настройки")
        self.geometry("400x300")

        # Входное устройство
        self.input_device_label = ttk.Label(self, text="Входное устройство:")
        self.input_device_label.pack(pady=5)
        self.input_device_var = tk.StringVar()
        self.input_device_combobox = ttk.Combobox(self, textvariable=self.input_device_var)
        self.input_device_combobox['values'] = self.get_audio_devices()
        self.input_device_combobox.pack(pady=5)

        # Выходное устройство
        self.output_device_label = ttk.Label(self, text="Выходное устройство:")
        self.output_device_label.pack(pady=5)
        self.output_device_var = tk.StringVar()
        self.output_device_combobox = ttk.Combobox(self, textvariable=self.output_device_var)
        self.output_device_combobox['values'] = self.get_audio_devices()
        self.output_device_combobox.pack(pady=5)

        # Язык ввода
        self.input_language_label = ttk.Label(self, text="Язык ввода:")
        self.input_language_label.pack(pady=5)
        self.input_language_var = tk.StringVar()
        self.input_language_combobox = ttk.Combobox(self, textvariable=self.input_language_var)
        self.input_language_combobox['values'] = self.get_languages()
        self.input_language_combobox.pack(pady=5)

        # Язык вывода
        self.output_language_label = ttk.Label(self, text="Язык вывода:")
        self.output_language_label.pack(pady=5)
        self.output_language_var = tk.StringVar()
        self.output_language_combobox = ttk.Combobox(self, textvariable=self.output_language_var)
        self.output_language_combobox['values'] = self.get_languages()
        self.output_language_combobox.pack(pady=5)

        # Файл для синтеза голоса
        self.voice_file_label = ttk.Label(self, text="Файл для синтеза голоса:")
        self.voice_file_label.pack(pady=5)
        self.voice_file_var = tk.StringVar()
        self.voice_file_entry = ttk.Entry(self, textvariable=self.voice_file_var, width=40)
        self.voice_file_entry.pack(pady=5)
        self.browse_button = ttk.Button(self, text="Обзор...", command=self.browse_file)
        self.browse_button.pack(pady=5)

        # Кнопка сохранения
        self.save_button = ttk.Button(self, text="Сохранить", command=self.save_settings)
        self.save_button.pack(pady=20)

    def get_audio_devices(self):
        # Здесь вы можете использовать библиотеку pyaudio для получения списка доступных аудиоустройств
        # Пример:
        # import pyaudio
        # p = pyaudio.PyAudio()
        # devices = [p.get_device_info_by_index(i)['name'] for i in range(p.get_device_count())]
        # p.terminate()
        # return devices
        return ["Устройство 1", "Устройство 2", "Устройство 3"]

    def get_languages(self):
        # Возвращает список доступных языков
        return ["ru-RU", "en-US", "fr-FR", "de-DE"]

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3")])
        if file_path:
            self.voice_file_var.set(file_path)

    def save_settings(self):
        settings = {
            "input_device": self.input_device_var.get(),
            "output_device": self.output_device_var.get(),
            "input_language": self.input_language_var.get(),
            "output_language": self.output_language_var.get(),
            "voice_file": self.voice_file_var.get()
        }
        print("Настройки сохранены:", settings)
        # Здесь вы можете сохранить настройки в файл или применить их непосредственно

if __name__ == "__main__":
    app = SettingsWindow()
    app.mainloop()
