import os
import ujson
import time
import network

# from dotenv import load_dotenv

from api_functions import get_air_status, format_air_levels, get_pm_status
from monitor_functions import show_pm_interface, show_splash_screen


class MainLoop:
    minutes = 30
    configuration = None
    sta_if = None

    def __init__(self):
        self.load_configuration()
        self.minutes = self.configuration['refresh_minutes']

        if self.configuration['splash_screen'] == 'y':
            show_splash_screen()
        self.connect_to_network()

        while True:
            self.main_loop(self.check_if_connected_to_wifi())
            time.sleep(60 * self.minutes)

    def load_configuration(self, config_path='config.json'):
        self.configuration = ujson.load(open(config_path))

    def check_if_connected_to_wifi(self):
        # return False
        return self.sta_if.isconnected()

    def connect_to_network(self):
        print('Connecting to network...')
        try:
            self.sta_if = network.WLAN(network.STA_IF)
            self.sta_if.active(True)
            self.sta_if.connect(self.configuration['network']['ssid'], self.configuration['network']['pass'])
        except Exception as e:
            print(f"Exception occured {e}")

        time.sleep(5)

        # print(sta_if.isconnected())
        if not self.sta_if.isconnected():
            print('Network connection failed.')
            time.sleep(5)
            self.connect_to_network()
        print('Network connection established.')

    def main_loop(self, is_connected):
        air_sensors = []

        air_levels = self.save_status(self.configuration['sensors']['sensor1'])
        air_status = get_pm_status(air_levels)
        air_sensors.append([air_levels, air_status])

        if self.configuration['sensors']['sensor2'] is not "":
            air_levels = self.save_status(self.configuration['sensors']['sensor2'])
            air_status = get_pm_status(air_levels)
            air_sensors.append([air_status, air_levels])

        # print(air_levels)
        # print(air_status)
        # air_sensors = [[{'pm2.5': 1, 'pm1': 0, 'pm10': 1}, {'pm1': 'green', 'pm2.5': 'green', 'pm10': 'green'}],[{'pm2.5': 1, 'pm1': 0, 'pm10': 1}, {'pm1': 'green', 'pm2.5': 'green', 'pm10': 'green'}]]
        show_pm_interface(air_sensors, image_type=self.configuration['image_type'], image_connection=self.configuration['image_connection'], theme=self.configuration['theme'], is_connected=is_connected, time_zone=self.configuration['time_zone'])



    def save_status(self, ip_address=None):
        raw_air_levels = get_air_status(ip_address)
        formatted_air_levels = format_air_levels(raw_air_levels)
        return formatted_air_levels

    def print_file(self, path):
        file = open(path, "r")
        data = file.read()
        print(data)
        file.close()

if __name__ == '__main__':
    print("Starting")
    main_loop_instance = MainLoop()
else:
    print("This should not be imported")