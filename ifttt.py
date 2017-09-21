import requests

key = 'eusNIu1EsTDCwSBRwh4-m3_UfoPvkN2eVfYfaNIEZ4Z'

def send_text(message):
    requests.get('https://maker.ifttt.com/trigger/{}/with/key/{}'.format('send_text',key), data={'value1':message})


def send_email(subject, message):
    requests.get('https://maker.ifttt.com/trigger/{}/with/key/{}'.format('send_email',key), data={'value1':subject, 'value2':message})


