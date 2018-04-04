import requests
import sys
import json
import time
import pika

scheme = {'properties':{'random':{'type':'string'}},'type':'object'}
query = {'jsonrpc':'2.0','method':'resolve','params':{'schemes':[{'in':True,'scheme':scheme,'type':'json-schema'}]},'id':1}

reply = {
    'result': []
}

while len(reply['result']) == 0:
    r = requests.post(sys.argv[1], data=json.dumps(query))

    reply = json.loads(r.content.decode("utf-8"))
    print(reply)
    if len(reply['result']) == 0:
        print("contract not found")
        time.sleep(5)

print("found server")

ep = reply['result'][0]['services'][0]['address']['endpoint']

# Register service

params = {"schemes":[{"in":True,"scheme":{"properties":{"data":{"type":"string"},"time":{"type":"integer"}},"type":"object"},"type":"json-schema"}],"service":{"name":"provider","address":{"rk":"test.rk","ex":"test"},"check_url":"http://localhost:8881/provider.json"}}
query = {'jsonrpc':'2.0','method':'registerContract','params':params,'id':1}
print(json.dumps(query))
r = requests.post(sys.argv[1], data=json.dumps(query))

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
