FROM alpine

RUN apk add py3-pip --no-cache python3-dev && pip3 install --upgrade pip

WORKDIR /app
COPY /requirements.txt /app
RUN pip3 install -r requirements.txt
COPY ["server.py", "/app"]
ENTRYPOINT [ "python3" ]
CMD ["app.py"]