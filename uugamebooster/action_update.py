import hashlib
import json
import os
from pathlib import Path
import re
import requests


def request_url(url):
    retry_times = 0
    while True:
        print(f"request url={url}...")
        try:
            response = requests.get(url)
            return response
        except Exception as e:
            if retry_times < 5:
                retry_times += 1
                print(f"request error: {e}, retry times={retry_times}")
                continue
            else:
                print(f"request error: {e}, ignore")
                break

    return None


def sha256_from_url(url):
    retry_times = 0
    while True:
        print(f"sha256 form url={url}...")
        try:
            sha256 = hashlib.sha256()
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        sha256.update(chunk)
            return sha256.hexdigest()
        except Exception as e:
            if retry_times < 5:
                retry_times += 1
                print(f"request error: {e}, retry times={retry_times}")
                continue
            else:
                print(f"request error: {e}, ignore")
                break

    return None


if __name__ == "__main__":
    env_dir = Path(__file__).resolve().parent
    os.chdir(env_dir)

    latest_response = request_url(
        "http://router.uu.163.com/api/plugin?type=openwrt-x86_64"
    )
    if not latest_response:
        exit()

    latest_json = json.loads(latest_response.text)
    latest_download_url = latest_json["url"]
    latest_download_url = re.sub(r"\?.*$", "?", latest_download_url)
    latest_version = re.search(r"\/v(\d+\.\d+\.\d+)\/", latest_download_url).group(1)
    with open("Makefile", "r", encoding="utf-8") as file:
        lines = file.readlines()

    for index in range(len(lines)):
        line = lines[index]
        match = re.search(r"^PKG_VERSION:=(\d+\.\d+\.\d+)", line)
        if match:
            curr_version = match.group(1)
            if curr_version == latest_version:
                print(f"Version={latest_version} not change, exit")
                exit()

            print(f"Current version={curr_version}, new version={latest_version}")
            lines[index] = f"PKG_VERSION:={latest_version}\n"
            continue

        match = re.search(r"^PKG_SOURCE_URL:=", line)
        if match:
            pkg_source_url = re.sub(
                r"aarch64|arm|mipsel|x86_64", r"$(ARCH)", latest_download_url
            )
            pkg_source_url = re.sub(
                f"{latest_version}", r"$(PKG_VERSION)", pkg_source_url
            )
            lines[index] = f"PKG_SOURCE_URL:={pkg_source_url}\n"
            continue

        match = re.search(r"^HASH_aarch64:=", line)
        if match:
            latest_arch_url = re.sub(
                r"aarch64|arm|mipsel|x86_64", r"aarch64", latest_download_url
            )
            latest_sha256 = sha256_from_url(latest_arch_url)
            lines[index] = f"HASH_aarch64:={latest_sha256}\n"
            continue

        match = re.search(r"^HASH_arm:=", line)
        if match:
            latest_arch_url = re.sub(
                r"aarch64|arm|mipsel|x86_64", r"arm", latest_download_url
            )
            latest_sha256 = sha256_from_url(latest_arch_url)
            lines[index] = f"HASH_arm:={latest_sha256}\n"
            continue

        match = re.search(r"^HASH_mipsel:=", line)
        if match:
            latest_arch_url = re.sub(
                r"aarch64|arm|mipsel|x86_64", r"mipsel", latest_download_url
            )
            latest_sha256 = sha256_from_url(latest_arch_url)
            lines[index] = f"HASH_mipsel:={latest_sha256}\n"
            continue

        match = re.search(r"^HASH_x86_64:=", line)
        if match:
            latest_arch_url = re.sub(
                r"aarch64|arm|mipsel|x86_64", r"x86_64", latest_download_url
            )
            latest_sha256 = sha256_from_url(latest_arch_url)
            lines[index] = f"HASH_x86_64:={latest_sha256}\n"
            continue

    with open("Makefile", "w", encoding="utf-8") as file:
        file.writelines(lines)
