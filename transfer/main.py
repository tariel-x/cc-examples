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

ep = reply['result'][0]['services'][0]['address']['endpoint']

f = open('usage.json')
query = f.read()
print(query)
requests.post(sys.argv[1], data=query)

# Register service

f = open('contract.json')
query = f.read()
print(json.dumps(query))
r = requests.post(sys.argv[1], data=query)

print(r.content)
print("Register service")

credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters('localhost', 5672, '/', credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.exchange_declare(exchange='test',
                         exchange_type='topic')

result = channel.queue_declare(exclusive=False)
queue_name = result.method.queue
channel.queue_bind(exchange='test',
                   queue=queue_name,
                   routing_key='test.rk')

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))
    r = requests.post(ep, data=str(body))

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)
channel.start_consuming()
