FROM python:latest

WORKDIR /app
COPY /requirements.txt /app
RUN pip3 install -r requirements.txt
COPY ["server.py", "/app"]
ENTRYPOINT [ "python3" ]
CMD ["app.py"]