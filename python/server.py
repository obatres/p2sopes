import pika
import time
import redis
import json
import pymongo

credentials = pika.PlainCredentials("sopes1","sopes1")
connection = pika.BlockingConnection(pika.ConnectionParameters("35.225.47.35",5672,credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='proyecto2', durable=True)
print(' Esperando por mensajes')

def convert(data):
    if isinstance(data, bytes):  
        return data.decode('ascii')
    elif isinstance(data, dict):   
        return dict(map(convert, data.items()))
    elif isinstance(data, tuple):  
        return map(convert, data)
    else:
        print("no se que es")
    return data

#MONGODB
db = "CORONAVIRUS"
collection = "PACIENTES" #Mismo valor para mongo y redis
#DEFINICION DE LLAVES PARA EL JSON
NOMBRE = "name"
DEPARTAMENTO = "location"
EDAD = "age"
FORMA = "infectedtype"
ESTADO = "state"

#REDIS
CONTADOR = "CONTADOR"
IPREDIS = "35.225.47.35"

myclient = pymongo.MongoClient(host=IPREDIS, port=5004)
mydb = myclient[convert(db)]
mycol = mydb[convert(collection)]
collist = mydb.list_collection_names()
if convert(collection) in collist:
    print("The collection exists.") 



def callback(ch, method, properties, body):
    
    print("recibido: %r" % body )
    #mongodb
    conversion = convert(body)
    print("CONVERSION " + conversion)
    print("VARIABLE Y ")
    y = json.loads(conversion)
    print(y[NOMBRE])
    x = mycol.insert_one(y)
    #redis
    r = redis.StrictRedis(host=IPREDIS, port=6379,db=0)
    pivote = convert(r.get(CONTADOR))
    print("esto trae el contador    ", pivote)
    r.hset(collection,NOMBRE+"["+pivote+"]", y[NOMBRE])
    r.hset(collection,DEPARTAMENTO+"["+pivote+"]", y[DEPARTAMENTO])
    r.hset(collection,EDAD+"["+pivote+"]", y[EDAD])
    r.hset(collection,FORMA+"["+pivote+"]", y[FORMA])
    r.hset(collection,ESTADO+"["+pivote+"]", y[ESTADO])
    pivateInt = int(pivote) + 1
    r.set(CONTADOR,pivateInt)
    print("Terminado")
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='proyecto2', on_message_callback= callback,no_ack=True)
channel.start_consuming()