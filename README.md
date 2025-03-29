# ESP32AirSensor

>Built with Inkplate6COLOR and usign API Type: airSensor (20200831)
Two modes of showing images ascii mode and bitmap mode
added characters to gfx_standard_font_01.py for inkplate 6 color  
upgraded exception for sd card

---

## Installation  
- [About](#about)
- Installation of micropython from Inkplate's github
- Copying all necessary files from Inkplate's github for display to work
- Copy example_config.json as config.json and change all necessary values
- Put files: main.py, api_functions.py, monitor_functions.py, config.json, emojis_in_bitmaps.py, emojis_in_bitmaps_black.py, angry_face.ascii, happy_face.ascii, medium_face.ascii
- Power device on (pyboard for moving files recommended, picocom recommended for possible debugging of config values at the first start)
  (For usage of splash_screen image with format 448x600 has to be processed through convert_images_to_bin_file.py and added to sd card)
## Example commands
 python3 -m pyboard --device /dev/ttyUSB0 -f cp ../../main.py ../../monitor_functions.py ../../config.json :  
 picocom /dev/ttyUSB0 -b 115200  
 in case of problems with permissions:  chmod 777 /dev/ttyUSB
## JSON
Change example_config.json to config.json  
arguments in json  
- Network (ssid) (pass)
- logging (debug, release) (not implemented)
- theme (light,dark)
- sensors (ip_addresses)# Support up to two sensors.
- image_connection (pm1, pm2.5, pm10, all) # Sets to what pm level is image (emoji) connected. All is the default state even if not set.
- image_type (bitmap, ascii) # Sets image (emoji) to be bitmap type or ascii type
- splash_screen (y,n) # Shows splash screen
- time_zone (+1,-1 (any number)) sets timezone
- refresh_time (1-(maxint)) set refresh time to be every x amount of minutes

TODO:  
add colors to faces (to test)  
add json (to test)
connect faces to the value set in config (to test)
add light and dark mode (to test)

[//]: # (add logging)
optional - add logging to external file on sd card