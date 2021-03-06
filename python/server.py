import pika
import time
import redis
import json
import pymongo
import ast

credentials = pika.PlainCredentials("sopes1","sopes1")
connection = pika.BlockingConnection(pika.ConnectionParameters("35.225.47.35",5672,credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='proyecto2', durable=True)
print(' Esperando por mensajes')

def convert(data):
    if isinstance(data, bytes):  return str(data.decode('UTF-8'))
    if isinstance(data, dict):   return dict(map(convert, data.items()))
    if isinstance(data, tuple):  return map(convert, data)

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
IPREDIS = "35.224.249.130"

myclient = pymongo.MongoClient(host=IPREDIS, port=27017)

mydb = myclient["CORONAVIRUS"]
mycol = mydb["PACIENTES"]
collist = mydb.list_collection_names()
if convert(collection) in collist:
    print("The collection exists.") 



def callback(ch, method, properties, body):
    
    print("recibido: %r" % body )
    try:
        #mongodb

        conversion = convert(body)
        print("CONVERSION " + str(conversion))
        print("VARIABLE Y ")
        y = json.loads(conversion)
        print(y)

        for x in y["Casos"]:
            mycol.insert_one(x)

        #redis
        r = redis.StrictRedis(host=IPREDIS, port=6379,db=0)

        pivote = convert(r.get(CONTADOR))
        print("esto trae el contador    ", pivote)
        for y in y["Casos"]:
            r.hset(collection,NOMBRE+"["+pivote+"]", x[NOMBRE])
            r.hset(collection,DEPARTAMENTO+"["+pivote+"]", x[DEPARTAMENTO])
            r.hset(collection,EDAD+"["+pivote+"]", x[EDAD])
            r.hset(collection,FORMA+"["+pivote+"]", x[FORMA])
            r.hset(collection,ESTADO+"["+pivote+"]", x[ESTADO])
            pivateInt = int(pivote) + 1
            r.set(CONTADOR,pivateInt)

        print("Terminado")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except:
        err="Error en la insercion de datos   "
        return(err)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='proyecto2', on_message_callback= callback,auto_ack=False)
channel.start_consuming()