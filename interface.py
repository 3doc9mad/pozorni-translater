import json
from utils import get_config
import dearpygui.dearpygui as dpg

from process_manager import start_translation_one_thread, start_translation_multi_thread, stop_translation_one_thread, stop_translation_multi_thread


def start_translation_thread():
    change_button(1)
    if get_config()['interface']['multiprocessing']:
        start_translation_multi_thread()
    else:
        start_translation_one_thread()


def stop_translation_thread():
    change_button(0)


def change_button(status=0):
    if status == 0:
        dpg.configure_item('main_button', texture_tag='mic-mute', enabled=True, callback=start_translation_thread,)
    if status == 1:
        dpg.configure_item('main_button', texture_tag='mic', enabled=False)
    if status == 2:
        dpg.configure_item('main_button', texture_tag='mic-fill', enabled=True, callback=stop_translation_thread)


def window():
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
    dpg.create_context()
    with dpg.font_registry():
        with dpg.font("fonts/SegoeUI-Light.ttf", 25) as default_font:
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)

    with dpg.theme() as global_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (255, 255, 255), category=dpg.mvThemeCat_Core)  # Фон окна
            dpg.add_theme_color(dpg.mvThemeCol_Text, (11, 11, 11), category=dpg.mvThemeCat_Core)  # Цвет текста
            dpg.add_theme_color(dpg.mvThemeCol_Border, (200, 200, 200), category=dpg.mvThemeCat_Core)  # Цвет границы
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 8, category=dpg.mvThemeCat_Core)  # Закругление рамок
        with dpg.theme_component(dpg.mvImageButton, enabled_state=True):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (255, 255, 255),
                                category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (255, 255, 255),
                                category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (255, 255, 255),
                                category=dpg.mvThemeCat_Core)

        with dpg.theme_component(dpg.mvImageButton, enabled_state=False):
            dpg.add_theme_color(dpg.mvThemeCol_Button, (255, 255, 255),
                                category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (255, 255, 255),
                                category=dpg.mvThemeCat_Core)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (255, 255, 255),
                                category=dpg.mvThemeCat_Core)
    texture_names = [
        'mic', 'mic-mute', 'mic-fill'
    ]

    dpg.bind_theme(global_theme)

    for texture_name in texture_names:
        width, height, channels, data = dpg.load_image(f"icons/{texture_name}.png")
        with dpg.texture_registry(show=False):
            dpg.add_static_texture(width=width, height=height, default_value=data, tag=texture_name)

    width, height, channels, data = dpg.load_image("icons/logo.gif")
    with dpg.texture_registry(show=False):
        dpg.add_static_texture(width=width, height=height, default_value=data, tag='logo')

    with dpg.window(label="Автопереводчик", width=450, height=800, no_collapse=False, no_move=True, no_title_bar=True,
                    no_resize=True, ):
        with dpg.group():
            dpg.add_image(texture_tag='logo', pos=[0, 0])
            dpg.bind_font(default_font)
            dpg.add_text("\n\n\n\n\n\n", )
            dpg.add_image_button(
                label="Начать перевод",
                texture_tag='mic-mute',
                tag='main_button',
                callback=start_translation_thread,
            )
            dpg.set_item_pos("main_button", [158, 250])

            dpg.add_text("Нажмите кнопку, чтобы начать перевод речи:\n\n\n\n\n\n\n\n\n\n\n", )
            dpg.add_separator()
            dpg.add_text("Распознанный текст:", )
            dpg.add_text('\n\n\n', tag='recognize_text')
            dpg.add_text("Переведенный текст:", )
            dpg.add_text('\n\n\n', tag='translate_text')
            if not config['interface']['multiprocessing']:
                dpg.add_text("Статус", )
                dpg.add_text("Выключен", tag='status_text')

            dpg.add_text('', tag='log_text', show=False)
    dpg.create_viewport(title='Автопереводчик', width=450, height=800, resizable=False)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == '__main__':
    window()
