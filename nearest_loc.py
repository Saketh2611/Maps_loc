import argparse
import math
import os
import sys

import requests
from dotenv import load_dotenv

load_dotenv()

GEOAPIFY_API_KEY = os.getenv("GEOAPIFY_API_KEY")


def get_nearest_residences(latitude, longitude):
    if not GEOAPIFY_API_KEY:
        raise ValueError(
            "GEOAPIFY_API_KEY is not set. Add it to a .env file or your environment."
        )

    url = "https://api.geoapify.com/v2/places"
    params = {
        "categories": "building.residential",
        "filter": f"circle:{longitude},{latitude},2000",
        "bias": f"proximity:{longitude},{latitude}",
        "limit": 4,
        "apiKey": GEOAPIFY_API_KEY,
    }

    response = requests.get(url, params=params, timeout=15)
    response.raise_for_status()

    results = []
    for feature in response.json().get("features", []):
        properties = feature["properties"]
        results.append(
            {
                "address": properties.get("formatted"),
                "latitude": properties.get("lat"),
                "longitude": properties.get("lon"),
                "distance_meters": properties.get("distance"),
            }
        )

    results.sort(
        key=lambda residence: (
            residence["distance_meters"]
            if isinstance(residence["distance_meters"], (int, float))
            else math.inf
        )
    )
    return results


def _coordinate(value, label, minimum, maximum):
    try:
        coordinate_value = float(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"{label} must be a number") from exc

    if not minimum <= coordinate_value <= maximum:
        raise argparse.ArgumentTypeError(
            f"{label} must be between {minimum} and {maximum}"
        )
    return coordinate_value


def _latitude(value):
    return _coordinate(value, "latitude", -90, 90)


def _longitude(value):
    return _coordinate(value, "longitude", -180, 180)


def main(argv=None):
    parser = argparse.ArgumentParser(prog="nearest")
    commands = parser.add_subparsers(dest="command", required=True)
    resident_parser = commands.add_parser("resident")
    resident_commands = resident_parser.add_subparsers(
        dest="resident_command", required=True
    )
    run_parser = resident_commands.add_parser("run")
    run_parser.add_argument("latitude", type=_latitude)
    run_parser.add_argument("longitude", type=_longitude)

    args = parser.parse_args(argv)

    try:
        residences = get_nearest_residences(args.latitude, args.longitude)
    except (ValueError, requests.RequestException) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    addresses = [
        residence["address"]
        for residence in residences
        if residence.get("address")
    ]
    if not addresses:
        print("No nearby residences found.")
        return 0

    for index, address in enumerate(addresses, start=1):
        print(f"{index}. {address}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
