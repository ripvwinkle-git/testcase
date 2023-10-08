#!/usr/bin/env python3

import sys
from random import randint, choices
from string import digits, ascii_letters
from time import sleep
from threading import Thread
import requests

ADDRESS = 'http://server'

def post_payload(
        min_records: int = 10,
        max_records: int = 100
) -> list[str]:
    return [
        {'text': ''.join(choices(digits+ascii_letters,k=16))}
        for i in range(randint(min_records, max_records))
    ]

def post_new(path: str, timeout: int=10):
    while True:
        try:
            for payload in post_payload():
                requests.post(path+'/new', params=payload, timeout=0.1)
        except Exception as exception:
            print(exception, file=sys.stdout)
            sleep(timeout)
            continue
        sleep(timeout)

def delete(path: str, count: int=10, timeout: int=10):
    while True:
        try:
            records = requests.get(path+f'/{count}', timeout=0.1)
            n = 0
            for record in records.json():
                requests.delete(path+f'/{record["uuid"]}', timeout=0.1)
                n+=1
            print(n, ' records deleted', file=sys.stdout)
        except Exception as exception:
            print(exception, file=sys.stdout)
            sleep(timeout)
            continue
        sleep(timeout)

if __name__ == '__main__':
    Thread(target=post_new, args=[ADDRESS]).start()
    Thread(target=delete, args=[ADDRESS]).start()
