#! /usr/bin/python2.7

import requests


def getTaskSize():
    data = requests.get('https://trouble.physics.byu.edu/api/tasks').json()
    ids = [x['id'] for x in data]
    return len(ids)


print(getTaskSize())
