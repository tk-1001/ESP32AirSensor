import os
import ujson
import time
import network
import ntptime

# from dotenv import load_dotenv

from api_functions import get_air_status, format_air_levels, get_pm_status
from monitor_functions import show_pm_interface, show_splash_screen


class MainLoop:
    refresh_minutes = 30
    configuration = None
    sta_if = None

    synced_time = None
    current_time = None

    def __init__(self):
        self.load_configuration()
        self.refresh_minutes = int(self.configuration['refresh_minutes'])

        if self.configuration['splash_screen'] == 'y':
            show_splash_screen()
        self.connect_to_network()

        while True:
            try:
                while True:
                    connection_status = self.check_if_connected_to_wifi()
                    if not connection_status:
                        self.connect_to_network()
                    else:
                        break

                self.main_loop(connection_status)
                time.sleep(60 * self.refresh_minutes)
            except Exception as e:
                print(e)
                self.write_errors(e)

    @staticmethod
    def write_errors(e):
        error_file_path = "sd/errors.txt"
        try:
            with open(error_file_path, "r") as f:
                lines = f.readlines()

            if len(lines) > 100:
                lines = lines[1:]
                lines.append(str(e) + "\n")
                with open(error_file_path, "w") as f:
                    f.writelines(lines)
            else:
                with open(error_file_path, "a") as f:
                    f.write(str(e)+ "\n")
        except FileNotFoundError:
            with open(error_file_path, "a+") as f:
                f.write(str(e) + "\n")

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

    @staticmethod
    def synchronize_time(time_zone="+0"):
        # ntptime.host = "1.europe.pool.ntp.org"
        formatted_time = None
        while formatted_time is None:
            try:
                # print("Local time before synchronization：%s" % str(time.localtime()))
                # make sure to have internet connection
                ntptime.settime()
                # print("Local time after synchronization：%s" % str(time.localtime()))
                time_to_format = time.localtime()
                hours, minutes, seconds = time_to_format[3], time_to_format[4], time_to_format[5]
                if time_zone[0] == '+':
                    hours += int(time_zone[1])
                elif time_zone[0] == '-':
                    hours -= int(time_zone[1])

                if hours < 10:
                    hours = str(hours)
                    hours = '0' + hours

                if minutes < 10:
                    minutes = str(minutes)
                    minutes = '0' + minutes

                if seconds < 10:
                    seconds = str(seconds)
                    seconds = '0' + seconds

                formatted_time = f"{hours}:{minutes}:{seconds}"
                print(formatted_time)
            except Exception as e:
                print(f"Error syncing time: {formatted_time} {e}")
                time.sleep(1)
        return formatted_time

    def get_time(self, time_zone="+0"):

        formatted_time = self.synchronize_time(time_zone)
        return formatted_time

    def main_loop(self, is_connected):
        air_sensors = []

        air_levels = self.save_status(self.configuration['sensors']['sensor1'])
        air_status = get_pm_status(air_levels)
        air_sensors.append([air_levels, air_status])

        if self.configuration['sensors']['sensor2'] is not "":
            air_levels = self.save_status(self.configuration['sensors']['sensor2'])
            air_status = get_pm_status(air_levels)
            air_sensors.append([air_levels, air_status])

        # print(air_levels)
        # print(air_status)
        # air_sensors = [[{'pm2.5': 1, 'pm1': 0, 'pm10': 1}, {'pm1': 'green', 'pm2.5': 'green', 'pm10': 'green'}],[{'pm2.5': 1, 'pm1': 0, 'pm10': 1}, {'pm1': 'green', 'pm2.5': 'green', 'pm10': 'green'}]]
        formatted_time = self.get_time(self.configuration['time_zone'])

        show_pm_interface(formatted_time,air_sensors, image_type=self.configuration['image_type'], image_connection=self.configuration['image_connection'], theme=self.configuration['theme'], is_connected=is_connected)



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