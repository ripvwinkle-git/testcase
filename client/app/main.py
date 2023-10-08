#!/usr/bin/env python3

import sys
from random import randint, choices
from string import digits, ascii_letters
from time import sleep
from threading import Thread, Lock
import requests

ADDRESS = 'http://gideone-testcase-server'

class Counter:

    def __init__(self):
        self.lock = Lock()
        self.counter = 0

    def increment(self):
        with self.lock:
            self.counter += 1

    def report(self):
        with self.lock:
            return self.counter

def post_payload(
        min_records: int = 10,
        max_records: int = 100
) -> list[str]:
    return [
        {'text': ''.join(choices(digits+ascii_letters,k=16))}
        for i in range(randint(min_records, max_records))
    ]

def post_new(path: str, timeout: int=5):
    while True:
        try:
            for payload in post_payload():
                requests.post(path+'/new', params=payload, timeout=1.0)
        except Exception as exception:
            print(exception, file=sys.stdout)
            sleep(timeout)
            continue
        sleep(timeout)

def delete(path: str, counter: Counter, count: int=10, timeout: int=5):
    while True:
        try:
            records = requests.get(path+f'/{count}', timeout=1.0)
            for record in records.json():
                requests.delete(path+f'/{record["uuid"]}', timeout=1.0)
                counter.increment()
        except Exception as exception:
            print(exception, file=sys.stdout)
            sleep(timeout)
            continue
        sleep(timeout)

def report_deleted(counter: Counter):
    counted = 0
    while True:
        new_counted = counter.report()
        print(
            f'records deleted: {new_counted-counted:3d}, ',
            f'total records deleted: {new_counted}',
            file=sys.stdout
        )
        counted = new_counted
        sleep(10)

if __name__ == '__main__':
    deleted = Counter()
    Thread(target=post_new, args=[ADDRESS]).start()
    Thread(target=delete, args=[ADDRESS, deleted]).start()
    Thread(target=report_deleted, args=[deleted]).start()
