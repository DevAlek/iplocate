#!/usr/bin/env python3
# -*- encoding:utf-8 -*-
from appdirs import user_cache_dir
from json import dump, dumps, load
from functools import lru_cache
from requests import get, post
from os import remove, mkdir
from os.path import exists
from sys import argv

cache_dir = user_cache_dir('iplocate')

if not exists(cache_dir): mkdir(cache_dir)
if not exists(f'{cache_dir}/cache.json'):
    with open(f'{cache_dir}/cache.json', 'w') as file:
        dump({}, file)

with open(f'{cache_dir}/cache.json') as file:
    cache = load(file)

@lru_cache
def assureData(raw: str, slice: str) -> str:
    try:    return raw.split(slice)[1].split('</dd>')[0]
    except: return "Not found."

def assureCoordinates(result: str, num: int) -> str:
    try:    return result.split('/')[num].split()[0]
    except: return "Not found."


@lru_cache
def request(link: str) -> str:
    return get(link).text

@lru_cache
def getLocation(ip: str, ignore_cache = False, reset_cache = False, save_json = False) -> dict:
    global cache

    if reset_cache:
        cache = {}

    if ip in list(cache) and not ignore_cache:
        return cache[ip]

    else:
        print(f"Connecting to https://tools.keycdn.com/geo?host={ip}...")
        raw = request(f"https://tools.keycdn.com/geo?host={ip}").split('<div class="bg-light medium rounded p-3">')[1].split("</div>")[0]

        result = {
            '':'',
            'location':{
                '':'',
                'city':         assureData(raw, '<dt class="col-4">City</dt><dd class="col-8 text-monospace">'),
                'region':       assureData(raw, '<dt class="col-4">Region</dt><dd class="col-8 text-monospace">'),
                'postal code':  assureData(raw, '<dt class="col-4">Postal code</dt><dd class="col-8 text-monospace">'),
                'contry':       assureData(raw, '<dt class="col-4">Country</dt><dd class="col-8 text-monospace">'),
                'continent':    assureData(raw, '<dt class="col-4">Continent</dt><dd class="col-8 text-monospace">'),
                'coordinates':  assureData(raw, '<dt class="col-4">Coordinates</dt><dd class="col-8 text-monospace">'),
                'latitude':     assureCoordinates(assureData(raw, '<dt class="col-4">Coordinates</dt><dd class="col-8 text-monospace">'), 0),
                'longitude':    assureCoordinates(assureData(raw, '<dt class="col-4">Coordinates</dt><dd class="col-8 text-monospace">'), 1),
                'time':         assureData(raw, '<dt class="col-4">Time</dt><dd class="col-8 text-monospace">'),
            },
            'network':{
                '':'',
                'ip':           assureData(raw, '<dt class="col-4">IP address</dt><dd class="col-8 text-monospace">'),
                'hostname':     assureData(raw, '<dt class="col-4">Hostname</dt><dd class="col-8 text-monospace">'),
                'provider':     assureData(raw, '<dt class="col-4">Provider</dt><dd class="col-8 text-monospace">'),
                'asn':          assureData(raw, '<dt class="col-4">ASN</dt><dd class="col-8 text-monospace">'),
            },
        }

        del raw

        cache[ip] = result
        with open(f'{cache_dir}/cache.json', 'w') as file:
            dump(cache, file)

        return result if not save_json else dumps(result)

bk = '\n'
if __name__ == "__main__":
    ignore_cache = True if "-f" in argv or "--force" in argv else  False
    reset_cache = True if "-r" in argv or "--reset-cache" in argv else  False
    ignore_not_found = True if "-i" in argv or "--ignore-not-found" in argv else  False
    save_json = True if "-o" in argv or "--output" in argv else  False


    if len(argv)-1 > 0 and not "-h" in argv and not "--help" in argv:
        for ip in argv[1:]:
            if "-" in ip: continue
            try:     location = getLocation(ip, ignore_cache, reset_cache, save_json)
            except:  print(f'{ip} not found.'); continue

            if not save_json:
                print(
                f'{bk*1}??? {ip}:{bk}'+f'{bk}  # '.join(
                [f'{category + ":" if category else ""} '+'\n    ?? '.join(
                [f'{element + ":" if element else ""} {location[category][element]}'
                for element in location[category] if not (location[category][element] == "Not found." and ignore_not_found)])
                for category in location])+'\n')
            else:
                print(location)
    else:
        print(
'''
Usage: iplocate [ip]...
    -h  --help      show this message.
''')

