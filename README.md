Hue Weather
=============

Changes the color of your Hue lights based on current weather conditions.


## Setup

 * Get a [Weather Underground API key](https://www.wunderground.com/weather/api/d/pricing.html)
 * Install the requirements (`pip install -r requirements.txt`)
 * Run the script!

## Usage

```
usage: hue-weather.py [-h] --state STATE --city CITY --bridge-ip BRIDGE_IP
                      --light-names [LIGHT_NAMES [LIGHT_NAMES ...]]
                      [--poll POLL] [--fork] [--log-filename LOG_FILENAME]

Changes your Hue light(s) based on the weather

optional arguments:
  -h, --help            show this help message and exit
  --state STATE, -s STATE
                        two letter postal code for your state
  --city CITY, -c CITY  the name of the city
  --bridge-ip BRIDGE_IP, -b BRIDGE_IP
                        the hue bridge ip address
  --light-names [LIGHT_NAMES [LIGHT_NAMES ...]], -l [LIGHT_NAMES [LIGHT_NAMES ...]]
                        the name of the light to change
  --poll POLL, -p POLL  the polling interval (seconds)
  --fork, -f            fork the process into the background
  --log-filename LOG_FILENAME, -log LOG_FILENAME
                        save logging information to file
```
