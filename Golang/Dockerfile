FROM golang:latest 
RUN mkdir /app 
ADD . /app/ 
WORKDIR /app 
RUN go build -o main . 
EXPOSE 8081
CMD ["/app/main"]