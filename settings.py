import json
import dearpygui.dearpygui as dpg
import pyaudio


def load_config():
    with open('config.json', 'r') as config_file:
        return json.load(config_file)


def save_config(config):
    with open('config.json', 'w') as config_file:
        json.dump(config, config_file, indent=4)


def get_audio_devices():
    p = pyaudio.PyAudio()
    devices = []
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        devices.append((i, info['name'], info['maxInputChannels']))
    p.terminate()
    return devices


def update_device_list():
    devices = get_audio_devices()
    input_device_list = [f"{name} (ID: {id})" for id, name, channels in devices if channels > 0]
    output_device_list = [f"{name} (ID: {id})" for id, name, channels in devices if channels > 0]

    dpg.set_value("input_device_combobox", input_device_list)
    dpg.set_value("output_device_combobox", output_device_list)


def save_settings():
    try:
        config['audio']['input_device_index'] = int(dpg.get_value("input_device_combobox")[1])
        config['audio']['output_device_index'] = int(dpg.get_value("output_device_combobox")[1])
        config['translation']['source_language'] = language_codes[dpg.get_value("source_language_combobox")]
        config['translation']['destination_language'] = language_codes[dpg.get_value("destination_language_combobox")]
        config['tts']['use_gpu'] = dpg.get_value("gpu_checkbox")
        config['tts']['gpu_accelerator'] = dpg.get_value("gpu_accelerator_entry")

        save_config(config)
        dpg.show_item("save_success")
    except Exception as e:
        dpg.show_item("save_error")


config = load_config()

dpg.create_context()
with dpg.font_registry():
    with dpg.font("fonts/SegoeUI-Light.ttf", 25) as default_font:
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)

texture_names = [
    'mic', 'mic-mute', 'mic-fill'
]

with dpg.theme() as global_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_style(dpg.mvWindowAppItem, )
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (255, 255, 255), category=dpg.mvThemeCat_Core)

        dpg.add_theme_color(dpg.mvThemeCol_Text, (11, 11, 11), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Border, (200, 200, 200), category=dpg.mvThemeCat_Core)

        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (200, 200, 200), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (185, 185, 185), category=dpg.mvThemeCat_Core)


        dpg.add_theme_color(dpg.mvThemeCol_Button, (200, 200, 200), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (185, 185, 185), category=dpg.mvThemeCat_Core)

        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (200, 200, 200), category=dpg.mvThemeCat_Core)

        dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (200, 200, 200), category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 8, category=dpg.mvThemeCat_Core)

        dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg, (200, 200, 200), category=dpg.mvThemeCat_Core)

    with dpg.theme_component(dpg.mvImageButton, enabled_state=True):
        dpg.add_theme_color(dpg.mvThemeCol_Button, (255, 255, 255),
                            category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (255, 255, 255),
                            category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (255, 255, 255),
                            category=dpg.mvThemeCat_Core)
    # with dpg.theme_component(dpg.mvCombo, enabled_state=True):
    #     dpg.add_theme_color(dpg.mvSelectable, (255, 255, 255),
    #                         category=dpg.mvThemeCat_Core)
    #     dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (255, 255, 255),
    #                         category=dpg.mvThemeCat_Core)
    #     dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (255, 255, 255),
    #                         category=dpg.mvThemeCat_Core)
    with dpg.theme_component(dpg.mvImageButton, enabled_state=False):
        dpg.add_theme_color(dpg.mvThemeCol_Button, (255, 255, 255),
                            category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (255, 255, 255),
                            category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (255, 255, 255),
                            category=dpg.mvThemeCat_Core)

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
with dpg.window(label="Настройки", width=450, height=800, no_collapse=True, no_move=False, no_title_bar=False,
                    no_resize=True, ):
    dpg.bind_font(default_font)
    dpg.bind_theme(global_theme)
    dpg.add_text("Выберите устройство ввода:")
    dpg.add_combo(label="Устройство ввода", items=get_audio_devices(), tag="input_device_combobox")

    dpg.add_text("Выберите устройство вывода:")
    dpg.add_combo(label="Устройство вывода", items=get_audio_devices(), tag="output_device_combobox")

    dpg.add_text("Язык источника:")
    dpg.add_combo(label="Язык источника", items=list(language_codes.keys()), tag="source_language_combobox")
    dpg.set_value("source_language_combobox",
                  [key for key, value in language_codes.items() if value == config['translation']['source_language']][
                      0])

    dpg.add_text("Язык назначения:")
    dpg.add_combo(label="Язык назначения", items=list(language_codes.keys()), tag="destination_language_combobox")
    dpg.set_value("destination_language_combobox", [key for key, value in language_codes.items() if
                                                    value == config['translation']['destination_language']][0])

    dpg.add_checkbox(label="Использовать GPU", tag="gpu_checkbox", default_value=config['tts']['use_gpu'])

    dpg.add_text("Ускоритель GPU:")
    dpg.add_input_text(tag="gpu_accelerator_entry", default_value=config['tts']['gpu_accelerator'])

    dpg.add_button(label="Сохранить настройки", callback=save_settings)
    dpg.add_text("Успешно сохранено!", tag='save_success', show=False)
    dpg.add_text("Не сохранено сохранено!", tag='save_error', show=False)


dpg.show_style_editor()

dpg.create_viewport(title='Автопереводчик', width=450, height=800, resizable=True)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()

