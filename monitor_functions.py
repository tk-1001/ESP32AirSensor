import os
# import importlib.util
import time

from inkplate6COLOR import Inkplate


from emojis_in_bitmaps_black import smiley_face_b, medium_face_b, medium_face_orange_b, angry_face_b
from emojis_in_bitmaps import smiley_face, medium_face, medium_face_orange, angry_face

from api_functions import get_pm10_norm_percent, get_pm25_norm_percent, get_pm1_norm_percent

display = Inkplate()
display.begin()
display.initSDCard()
print(os.listdir("/sd"))
# display.setFont('./JetBrainsMonoNL-Regular.ttf')
# module_path = "/sd/sml.py"



def get_color_of_pm_level(color_of_pm_level):
    if color_of_pm_level == "green":
        return display.GREEN
    if color_of_pm_level == "yellow":
        return display.YELLOW
    if color_of_pm_level == "orange":
        return display.ORANGE
    if color_of_pm_level == "red":
        return display.RED

def show_bitmap_face(x, y, representative_color, theme):
    # print(representative_color)
    if theme == 'dark':
        representative_dictionary = {'green': smiley_face_b, 'yellow': medium_face_b, 'orange': medium_face_orange_b,
                                     'red': angry_face_b}
    else:
        representative_dictionary = {'green': smiley_face, 'yellow': medium_face, 'orange': medium_face_orange,
                                     'red': angry_face}
    type_of_face = representative_dictionary[representative_color]

    for x_local in range(0,127):
        for y_local in range(0,127):
            display.drawPixel(x+x_local,y+y_local, type_of_face[x_local][y_local])

def show_ascii_face(x, y, representative_color, font_size):
    representative_dictionary = {'green': 'g', 'yellow': 'm', 'orange': 'mm', 'red': 'b'}
    type_of_face = representative_dictionary[representative_color]

    ascii_faces = {'g': './happy_face.ascii', 'm': './medium_face.ascii', 'mm': './medium_face.ascii',
                   'b': './angry_face.ascii'}
    ascii_colors = {'g': display.GREEN, 'm': display.YELLOW, 'mm': display.ORANGE, 'b': display.RED}
    face_to_display_file = ascii_faces[type_of_face]
    color_of_face_to_display = ascii_colors[type_of_face]

    display.setTextSize(font_size)
    with open(face_to_display_file, 'r') as f:
            current_lines = f.readlines()

    for current_line in current_lines:
        display.printText(x, y, current_line, color_of_face_to_display)
        y += 10


def get_face_color_by_all_colors(pm1_color, pm2_color, pm3_color):
    if pm1_color == pm2_color:
        return pm1_color
    if pm3_color == pm2_color:
        return pm3_color
    if pm1_color == pm3_color:
        return pm1_color

    return 'yellow'

def show_pm_sensor_levels(x,y, pm_levels, pm_status, font_size, theme):
    display.setTextSize(font_size)
    if theme == 'dark':
        display.drawRoundRect(x,y, 250, 250, 10, 1)
    else:
        display.drawRoundRect(x,y, 250, 250, 10, 0)

    if pm_levels is None or pm_status is None:
        pm1_color = 0
        pm25_color = 0
        pm10_color = 0
        pm_levels = {'pm1': 0, 'pm2.5': 0, 'pm10': 0}
    else:
        pm1_color = get_color_of_pm_level(pm_status['pm1'])
        pm25_color = get_color_of_pm_level(pm_status['pm2.5'])
        pm10_color = get_color_of_pm_level(pm_status['pm10'])


    pm1_levels = pm_levels['pm1']
    display.printText(x+10, y+10, f'PM1: {pm1_levels}', pm1_color)
    pm1_norm_percent = get_pm1_norm_percent(pm_levels['pm1'])
    display.printText(x + 10, y + 50, f'{pm1_norm_percent}%', pm25_color)

    pm25_levels  = pm_levels['pm2.5']
    display.printText(x+10, y+95, f'PM2.5: {pm25_levels}', pm25_color)
    pm25_norm_percent = get_pm25_norm_percent(pm_levels['pm2.5'])
    display.printText(x+10, y+135, f'{pm25_norm_percent}%', pm25_color)

    pm10_levels = pm_levels['pm10']
    display.printText(x+10, y+180, f'PM10: {pm10_levels}', pm10_color)
    pm10_norm_percent = get_pm10_norm_percent(pm_levels['pm10'])
    display.printText(x+10, y+220, f'{pm10_norm_percent}%', pm10_color)


def show_color_examples():
    display.fillRect(10, 390, 50, 50, display.GREEN)
    display.fillRect(70, 390, 50, 50, display.YELLOW)
    display.fillRect(130, 390, 50, 50, display.ORANGE)
    display.fillRect(190, 390, 50, 50, display.RED)

def show_exception():
    display.printText(10, 330, 'wifi disconnected', display.RED)


def show_splash_screen():
    display.clearDisplay()

    with open('/sd/5bw', 'r') as f:
        for y_local in range(0, 447):
            current_line = f.readline().strip()
            for x_local in range(0, 599):
                display.drawPixel(x_local, y_local, int(current_line[x_local]))

    display.display()




def show_time(formatted_time ,theme='light'):
    if theme == 'light':
        display.printText(270, 405, formatted_time, display.BLACK)
    else:
        display.printText(270, 405, formatted_time, display.WHITE)


def show_pm_interface(formatted_time ,air_sensors, image_type='bitmap', image_connection='all', theme='light', is_connected='False'):
    display.clearDisplay()

    if theme == 'dark':
        display.fillScreen(0)


    current_x = 0
    for sensor in air_sensors:
        print(sensor)
        if sensor is []:
            continue
        show_pm_sensor_levels(current_x+10, 10, sensor[0], sensor[1], 4, theme)
        current_x += 300

    if is_connected is False:
        show_exception()

    show_color_examples()

    show_time(formatted_time ,theme)

    pm_status = air_sensors[0][1]

    representative_color = get_face_color_by_all_colors(pm_status["pm1"], pm_status["pm2.5"], pm_status["pm10"])
    if image_connection == 'pm1':
        representative_color = pm_status["pm1"]
    elif image_connection == 'pm2.5':
        representative_color = pm_status["pm2.5"]
    elif image_connection == 'pm10':
        representative_color = pm_status["pm10"]

    if image_type == 'bitmap':
        show_bitmap_face(470,320, representative_color, theme)
    if image_type == 'ascii':
        show_ascii_face(420, 300,representative_color, 1)

    display.display()

# if __name__ == '__main__':
#     pm_levels = {'pm1': 30, 'pm2.5': 54, 'pm10': 61}
#     pm_status = {'pm1': 'green', 'pm25': 'red', 'pm10': 'orange'}
#
#     show_pm_interface([pm_levels, pm_status])
