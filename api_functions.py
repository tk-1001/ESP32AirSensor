import time

import urequests
import json

def format_air_levels(air_status):
    formatted_air_status = air_status['air']['sensors']
    new_formatted_air_status = {}
    for sensor in formatted_air_status:
        pm_type = sensor['type']
        pm_value = sensor['value']
        new_formatted_air_status.update({pm_type: pm_value})
    return new_formatted_air_status

def get_pm_status(pm_levels):
    return {'pm1': get_pm1_status(pm_levels['pm1']), 'pm2.5': get_pm25_status(pm_levels['pm2.5']), 'pm10': get_pm10_status(pm_levels['pm10'])}

def get_pm1_status(pm1_level):
    if pm1_level <= 10:
        return "green"
    elif 10 < pm1_level <= 20:
        return "yellow"
    elif 20 < pm1_level <= 35:
        return "orange"
    elif 55 <= pm1_level:
        return "red"

def get_pm25_status(pm25_level):
    if pm25_level <= 12:
        return "green"
    elif 12 < pm25_level <= 35:
        return "yellow"
    elif 35 < pm25_level <= 55:
        return "orange"
    elif 55 <= pm25_level:
        return "red"

def get_pm10_status(pm10_level):
    if pm10_level <= 54:
        return "green"
    elif 54 < pm10_level <= 154:
        return "yellow"
    elif 154 < pm10_level <= 254:
        return "orange"
    elif 255 <= pm10_level:
        return "red"

def get_air_status(ip_address):
    r = None
    while r is None or r.json() is None or r is '':
        try:
            r = urequests.get(f'http://{ip_address}/api/air/extended/state')
        except Exception as e:
            print(e)
            time.sleep(0.5)
    # print(r.json())
    # except Exception as e:
    #     print(urequests.__file__)
    #     print(e)
    #     return None
    time.sleep(1)
    return r.json()

def get_pm1_norm_percent(pm1_level):
    return int(pm1_level/15 * 100)

def get_pm25_norm_percent(pm25_level):
    return int(pm25_level/20 * 100)

def get_pm10_norm_percent(pm10_level):
    return int(pm10_level/40 * 100)


