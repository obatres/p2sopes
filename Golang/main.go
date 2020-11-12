package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"

	"github.com/gorilla/mux"
	"github.com/rs/cors"
	"github.com/streadway/amqp"
)

func failOnError(err error, msg string) {
	if err != nil {
		log.Fatalf("%s: %s", msg, err)
	}
}

func info(w http.ResponseWriter, r *http.Request) {
	var result map[string]interface{}
	body, err := ioutil.ReadAll(r.Body)
	if err != nil {
		fmt.Println(err)
	}
	json.Unmarshal([]byte(body), &result)
	fmt.Println(result)

	/**
	 *rabbit
	 */
	//conn, err := amqp.Dial("amqp://guest:guest@138.68.230.101:5672/")
	conn, err := amqp.Dial("amqp://sopes1:sopes1@35.225.47.35:5672/")
	failOnError(err, "Fallo al conectar RabbitMQ")
	defer conn.Close()

	ch, err := conn.Channel()
	failOnError(err, "Fallo al abrir el canal de conexion ")
	defer ch.Close()

	q, err := ch.QueueDeclare(
		"proyecto2", // name
		true,        // durable
		false,       // delete when unused
		false,       // exclusive
		false,       // no-wait
		nil,         // arguments
	)
	failOnError(err, "Fallo al crear la cola")

	err = ch.Publish(
		"",     // exchange
		q.Name, // routing key
		false,  // mandatory
		false,  // immediate
		amqp.Publishing{
			DeliveryMode: amqp.Persistent,
			ContentType:  "application/json",
			Body:         []byte(body),
		})
	//log.Printf(" [x] Sent %s", result)
	failOnError(err, "Fallo al publicar el mensaje")
	/**
	 *rabbit
	 */
	fmt.Fprintf(w, "%s", "termino")
}

func main() {
	router := mux.NewRouter().StrictSlash(true)
	fmt.Println("Server Running on port: 8081")
	router.HandleFunc("/", info).Methods("POST")

	// cors.Default() setup the middleware with default options being
	// all origins accepted with simple methods (GET, POST). See
	// documentation below for more options.
	handler := cors.Default().Handler(router)
	http.ListenAndServe(":8081", handler)

	log.Fatal(http.ListenAndServe(":8081", router))
}
