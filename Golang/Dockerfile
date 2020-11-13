FROM golang:latest 
RUN mkdir /app 
ADD . /app/ 
WORKDIR /app 
RUN go get -d github.com/gorilla/mux
RUN go get -d github.com/rs/cors
RUN go get -d github.com/streadway/amqp
RUN go build -o main . 
EXPOSE 8081
CMD ["/app/main"]