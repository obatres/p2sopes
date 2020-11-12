package main

import (
	"fmt"
	"log"
	"net/http"

	"github.com/Golang/pkg/server"
	"github.com/streadway/amqp"
)

func failOnError(err error, msg string) {
	if err != nil {
		log.Fatalf("%s: %s", msg, err)
	}
}

func enviarDatos() {
	conn, err := amqp.Dial("amqp://sopes1:sopes1@35.225.47.35:5672/")
	failOnError(err, "Failed to connect to RabbitMQ")
	defer conn.Close()

	ch, err := conn.Channel()
	failOnError(err, "Failed to open a channel")
	defer ch.Close()

	q, err := ch.QueueDeclare(
		"hello", // name
		true,    // durable
		false,   // delete when unused
		false,   // exclusive
		false,   // no-wait
		nil,     // arguments
	)
	failOnError(err, "Failed to declare a queue")

	for i := 0; i < 10; i++ {
		body := fmt.Sprintf("%s", "Mensaje"+string(i))
		err = ch.Publish(
			"",
			q.Name,
			false,
			false,
			amqp.Publishing{
				ContentType: "application/json",
				Body:        []byte(`{"Name":"Alice","Body":"Hello","Time":1294706395881547000}`),
			})
		log.Printf("Sent %s", body)
		failOnError(err, "Fallo en enviar el mensaje")
	}
}
func main() {

	s := server.New()
	log.Fatal(http.ListenAndServe(":8080", s.Router()))
}
