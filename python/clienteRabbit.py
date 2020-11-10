import pika

credentials = pika.PlainCredentials("sopes1","sopes1")
connection = pika.BlockingConnection(pika.ConnectionParameters("35.225.47.35",5672,credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue="hello", durable=True)



def callback(ch, method,properties, body):
    print("Recibe mensaje %r" % body)


channel.basic_consume(queue="hello",on_message_callback=callback,auto_ack=True)

print("esperando mensajes")

channel.start_consuming()