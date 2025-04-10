# apple-bssid-geoloc
get bssid geolocation (lat, lon) from apple

## Installation
```
./setup-env.sh
./install.sh
```

## Usage
```
abgl <BSSID>
```
```
usage: abgl.py [-h] bssid

geolocate bssid using apple's servers

positional arguments:
  bssid       bssid in XX:XX:XX:XX:XX:XX format

options:
  -h, --help  show this help message and exit
```

## Output
```
XX:XX:XX:XX:XX:XX,lat,lon
```
