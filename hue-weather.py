#!/usr/bin/env python

import os
import time
import pyhue
import logging
import requests
import argparse

from furl import furl
from rgb import Converter

HUE_USERNAME = "newdeveloper"
MAX_ERRORS = 50

# RGB Color Tuples
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


def get_color_for(weather):
    """ Converts weather into arbitrary colors """
    colors = Converter()
    if "rain" in weather.lower():
        return colors.rgbToCIE1931(*BLUE)
    elif "cloudy" in weather.lower():
        return colors.rgbToCIE1931(*GREEN)
    else:
        return colors.rgbToCIE1931(*RED)


def get_weather_url(api_key, state, city):
    """ Constructs API URLs """
    url = furl()
    url.scheme = "https"
    url.host = "api.wunderground.com"
    url.path.segments = ["api", api_key, "forecast", "geolookup",
                         "conditions", "q", state, city]
    return str(url) + ".json"


def hue_weather_loop(api_key, state, city, bridge_ip, light_names, poll):
    """ Main loop, queries the WU API, and updates lights """
    logging.debug("Logging into bridge at: %s" % bridge_ip)
    bridge = pyhue.Bridge(bridge_ip, HUE_USERNAME)
    lights = filter(lambda light: light.name in light_names, bridge.lights)
    if not len(lights):
        raise ValueError("No lights found with names: %s" % light_names)
    logging.debug("Starting main loop...")
    errors = 0
    while True:
        try:
            if MAX_ERRORS < errors:
                os._exit(1)
            url = get_weather_url(api_key, state, city)
            conditions = requests.get(url).json()
            weather = conditions["current_observation"]["weather"]
            for light in lights:
                light.on = True
                light.xy = get_color_for(weather)
        except:
            errors += 1
        finally:
            time.sleep(poll)


def main(args):
    """ Just some quick setup code """
    if args.fork:
        pid = os.fork()
        if pid:
            print("[*] Forking into background %s" % pid)
            os._exit(0)
    # Setup logging
    logging.basicConfig(format="[%(levelname)s] %(asctime)s: %(message)s",
                        filename=args.log_filename,
                        level=logging.DEBUG)
    # Starts the main loop
    hue_weather_loop(args.api_key, args.state, args.city, args.bridge_ip,
                     args.light_names, args.poll)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Changes your Hue light(s) based on the weather',
    )
    parser.add_argument('--api-key', '-k',
                        help='weather underground api key',
                        dest='api_key',
                        required=True)
    parser.add_argument('--state', '-s',
                        help='two letter postal code for your state',
                        dest='state',
                        required=True)
    parser.add_argument('--city', '-c',
                        help='the name of the city',
                        dest='city',
                        required=True)
    parser.add_argument('--bridge-ip', '-b',
                        help='the hue bridge ip address',
                        dest='bridge_ip',
                        required=True)
    parser.add_argument('--light-names', '-l',
                        help='the name of the light to change',
                        dest='light_names',
                        nargs='*',
                        required=True)
    parser.add_argument('--poll', '-p',
                        help='the polling interval (seconds)',
                        dest='poll',
                        default=300.0,
                        type=float)
    parser.add_argument('--fork', '-f',
                        help='fork the process into the background',
                        action='store_true',
                        dest='fork')
    parser.add_argument('--log-filename', '-log',
                        help='save logging information to file',
                        dest='log_filename',
                        default="hue-weather.log")
    try:
        main(parser.parse_args())
    except KeyboardInterrupt:
        print("\r[!] User stop, have a nice day!")
