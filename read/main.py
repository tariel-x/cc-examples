import requests
import sys
import json
import time
import pika

f = open('require.json')
query = f.read()

reply = {
    'result': []
}

while len(reply['result']) == 0:
    r = requests.post(sys.argv[1], data=query)

    reply = json.loads(r.content.decode("utf-8"))
    print(reply)
    if len(reply['result']) == 0:
        print("contract not found")
        time.sleep(5)

print("found server")

rk = reply['result'][0]['services'][0]['address']['rk']
ex = reply['result'][0]['services'][0]['address']['ex']

f = open('usage.json')
query = f.read()
requests.post(sys.argv[1], data=query)

print("registered usage")

credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters('localhost', 5672, '/', credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

with open("/dev/random", 'rb') as f:
    while True:
        request = f.read(1)
        print("Sending request %s ..." % request)
        channel.basic_publish(exchange=ex, routing_key=rk, body=str(request))
        time.sleep(1)