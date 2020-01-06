#!/usr/bin/env python3

import urllib.request
import urllib.parse
import time
import argparse
from statistics import mean
import os.path
import re


def evaluate_download_speed(file_url, timeout=60):

    start = time.perf_counter()

    # filesize in byte [B]
    filesize = 0

    with urllib.request.urlopen(file_url, timeout=timeout) as response:
        data = response.read()

        filesize = int(response.info()["Content-Length"])

    end = time.perf_counter()

    # download duration in seconds [s]
    duration = end - start

    # download speed in byte/second [B/s]
    speed = filesize / duration

    return speed, duration, filesize


def is_valid_url(url):
    try:
        result = urllib.parse.urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def read_mirror_list(file_path):

    mirror_urls = []

    with open(file_path) as file_handle:
        for line in file_handle:
            stripped_line = line.strip()
            if stripped_line.startswith("#"):
                continue

            if is_valid_url(stripped_line) and stripped_line.endswith("/"):
                mirror_urls.append(stripped_line)
            else:
                raise Exception("URL error in {}".format(stripped_line))

    return mirror_urls


def valid_mirror_list(path):
    if os.path.isfile(path):
        return path

    raise Exception("Not a valid mirror list file: {}".format(path))


def valid_filekey_list(filekeys):
    if re.match(r"^[\w\+]+$", filekeys):
        return filekeys.split("+")

    raise Exception("Not a valid file key list: {}".format(filekeys))


def main():

    parser = argparse.ArgumentParser(
        description="Test the download speed of different mirrors.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--filekeys",
        type=valid_filekey_list,
        help="the files to download, e.g. small+large",
        default="all",
    )
    parser.add_argument(
        "--timeout", type=int, help="timeout per download in seconds", default=60,
    )
    parser.add_argument(
        "mirror_list", type=valid_mirror_list, help="text file containing mirror list"
    )
    args = parser.parse_args()

    # TODO: move this to config file
    files = dict(
        {
            "large": "indices/override.bionic.extra.universe",  # approx. 10MB
            "medium": "indices/override.bionic.universe",  # approx. 2MB
            "small": "indices/override.bionic.universe.src",  # approx. 900kB
        }
    )

    mirror_list_path = args.mirror_list
    download_timeout = args.timeout

    files_to_test = args.filekeys

    if "all" in args.filekeys:
        files_to_test = files.keys()

    mirrors = read_mirror_list(mirror_list_path)

    mirror_speeds = dict().fromkeys(mirrors)

    for mirror in mirrors:

        print("Testing mirror {}".format(mirror))

        speeds = []
        avg_speed = 0

        try:
            for file_key in files_to_test:

                file_path = files[file_key]

                download_url = mirror + file_path

                speed, duration, filesize = evaluate_download_speed(
                    download_url, download_timeout
                )

                print(
                    "  Speed for '{}' file: {:.1f} kB/s".format(
                        file_key, speed / 1024.0
                    )
                )

                speeds.append(speed)

            avg_speed = mean(speeds)

            print("  Average: {:.1f} kB/s".format(avg_speed / 1024.0))
        except Exception as e:
            print("  An error occured while testing: {}".format(str(e)))

        mirror_speeds[mirror] = avg_speed

    sorted_mirror_speeds = sorted(
        mirror_speeds.items(), key=lambda item: item[1], reverse=True
    )

    print("Mirror speed ranking:")
    for mirror, speed in sorted_mirror_speeds:
        print("  {} at {:.1f} kB/s".format(mirror, speed / 1024.0))


if __name__ == "__main__":
    main()
