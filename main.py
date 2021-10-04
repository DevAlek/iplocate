#!/usr/bin/env python3
# -*- encoding:utf-8 -*-
from appdirs import user_cache_dir
from functools import lru_cache
from requests import get, post
from os import remove, mkdir
from json import dump, load
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
def request(link: str) -> str:
    if link not in list(cache):
        print(f'connecting to {link}...')
        result = get(link).text
        cache[link] = result
        with open(f'{cache_dir}/cache.json', 'w') as file:
            dump(cache, file)
        return result
    else:
        return cache[link]


@lru_cache
def getLocation(ip: str) -> dict:
    raw = request(f"https://tools.keycdn.com/geo?host={ip}").split('<div class="bg-light medium rounded p-3">')[1].split("</div>")[0]

    return {
    'location':{
        'city':         raw.split('<dt class="col-4">City</dt><dd class="col-8 text-monospace">')[1].split('</dd>')[0],
        'region':       raw.split('<dt class="col-4">Region</dt><dd class="col-8 text-monospace">')[1].split('</dd>')[0],
        'postal code':  raw.split('<dt class="col-4">Postal code</dt><dd class="col-8 text-monospace">')[1].split('</dd>')[0],
        'contry':       raw.split('<dt class="col-4">Country</dt><dd class="col-8 text-monospace">')[1].split('</dd>')[0],
        'continent':    raw.split('<dt class="col-4">Continent</dt><dd class="col-8 text-monospace">')[1].split('</dd>')[0],
        'coordinates':  raw.split('<dt class="col-4">Coordinates</dt><dd class="col-8 text-monospace">')[1].split('</dd>')[0],
        'latitude':     raw.split('<dt class="col-4">Coordinates</dt><dd class="col-8 text-monospace">')[1].split('</dd>')[0].split('/')[0].split()[0],
        'longitude':    raw.split('<dt class="col-4">Coordinates</dt><dd class="col-8 text-monospace">')[1].split('</dd>')[0].split('/')[1].split()[0],
        'time':         raw.split('<dt class="col-4">Time</dt><dd class="col-8 text-monospace">')[1].split('</dd>')[0],
        },
    'network':{
        'ip': raw.split('<dt class="col-4">IP address</dt><dd class="col-8 text-monospace">')[1].split('</dd>')[0],
        'hostname': raw.split('<dt class="col-4">Hostname</dt><dd class="col-8 text-monospace">')[1].split('</dd>')[0],
        'provider': raw.split('<dt class="col-4">Provider</dt><dd class="col-8 text-monospace">')[1].split('</dd>')[0],
        'asn': raw.split('<dt class="col-4">ASN</dt><dd class="col-8 text-monospace">')[1].split('</dd>')[0],
        }
    }

@lru_cache
def getLocationForOutputing(ip: str) -> dict:
    raw = request(f"https://tools.keycdn.com/geo?host={ip}").split('<div class="bg-light medium rounded p-3">')[1].split("</div>")[0]

    return {
    '':'',
    'location':{
        '':'',
        'city':         raw.split('<dt class="col-4">City</dt><dd class="col-8 text-monospace">')[1].split('</dd>')[0],
        'region':       raw.split('<dt class="col-4">Region</dt><dd class="col-8 text-monospace">')[1].split('</dd>')[0],
        'postal code':  raw.split('<dt class="col-4">Postal code</dt><dd class="col-8 text-monospace">')[1].split('</dd>')[0],
        'contry':       raw.split('<dt class="col-4">Country</dt><dd class="col-8 text-monospace">')[1].split('</dd>')[0],
        'continent':    raw.split('<dt class="col-4">Continent</dt><dd class="col-8 text-monospace">')[1].split('</dd>')[0],
        'coordinates':  raw.split('<dt class="col-4">Coordinates</dt><dd class="col-8 text-monospace">')[1].split('</dd>')[0],
        'latitude':     raw.split('<dt class="col-4">Coordinates</dt><dd class="col-8 text-monospace">')[1].split('</dd>')[0].split('/')[0].split()[0],
        'longitude':    raw.split('<dt class="col-4">Coordinates</dt><dd class="col-8 text-monospace">')[1].split('</dd>')[0].split('/')[1].split()[0],
        'time':         raw.split('<dt class="col-4">Time</dt><dd class="col-8 text-monospace">')[1].split('</dd>')[0],
        },
    'network':{
        '':'',
        'ip': raw.split('<dt class="col-4">IP address</dt><dd class="col-8 text-monospace">')[1].split('</dd>')[0],
        'hostname': raw.split('<dt class="col-4">Hostname</dt><dd class="col-8 text-monospace">')[1].split('</dd>')[0],
        'provider': raw.split('<dt class="col-4">Provider</dt><dd class="col-8 text-monospace">')[1].split('</dd>')[0],
        'asn': raw.split('<dt class="col-4">ASN</dt><dd class="col-8 text-monospace">')[1].split('</dd>')[0],
        }
    }

bk = '\n'
if __name__ == "__main__":
    if len(argv)-1 > 0 and not "-h" in argv and not "--help" in argv:
        for ip in argv[1:]:
            try:     location = getLocationForOutputing(ip)
            except:  print(f'{ip} not found.'); continue
            print(f'{bk*2}→ {ip}:{bk}'+f'{bk}  # '.join([f'{category + ":" if category else ""} '+'\n    · '.join([f'{element + ":" if element else ""} {location[category][element]}' for element in location[category]]) for category in location]))
    else:
        print(
'''
Usage: iplocate [ip]...
    -h  --help      show this message.
''')
