#!/usr/bin/env python
import sys
import re
import requests
import argparse
from google.protobuf.message import DecodeError
from helpers.BSSIDApple_pb2 import BSSIDResp

parser = argparse.ArgumentParser(description="geolocate bssid using apple's servers")
parser.add_argument("bssid", help='bssid in XX:XX:XX:XX:XX:XX format', type=str)
args = parser.parse_args()

requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning
)

if __name__ == "__main__":

    # Set up the HTTP headers
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "*/*",
        "Accept-Charset": "utf-8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-us",
        "User-Agent": "locationd/1753.17 CFNetwork/711.1.12 Darwin/14.0.0",
    }

    # Set up the POST data
    data_bssid = f"\x12\x13\n\x11{args.bssid}\x18\x00\x20\01"
    data = (
        "\x00\x01\x00\x05en_US\x00\x13com.apple.locationd\x00\x0a"
        + "8.1.12B411\x00\x00\x00\x01\x00\x00\x00"
        + chr(len(data_bssid))
        + data_bssid
    )
    # Set the endpoint for the request
    endpoint = "https://gs-loc.apple.com/clls/wloc"
    # Make the HTTP POST request using the requests library
    response = requests.post(endpoint, headers=headers, data=data, verify=False)

    # Parse the binary content of the response into a BSSIDResp protobuf object.
    bssid_response = BSSIDResp()
    try:
        bssid_response.ParseFromString(response.content[10:])
    except DecodeError as e:
        print(f"Failed to decode response: {e}")
    lat_match = re.search(r"lat: (\S*)", str(bssid_response))
    lon_match = re.search(r"lon: (\S*)", str(bssid_response))
    try:
        # Extract the latitude and longitude values from the response
        lat = lat_match.group(1)
        lon = lon_match.group(1)

        if "18000000000" not in lat:
            # format the latitude and longitude values
            lat = float(lat[:-8] + "." + lat[-8:])
            lon = float(lon[:-8] + "." + lon[-8:])
            # create the output dictionary
            data = {"bssid": args.bssid, "latitude": lat, "longitude": lon}
            print(f"{args.bssid},{lat},{lon}")
        else:
            print(
                f"{args.bssid} -- ERROR: Latitude or longitude value not found in response"
            )
    except Exception as e:
        print(f"bssid -- ERROR: {str(e)}")
