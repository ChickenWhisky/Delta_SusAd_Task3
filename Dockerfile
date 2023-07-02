FROM python:3.9-alpine
WORKDIR /app
COPY [ "./server.py", "/app" ]

RUN mkdir /app/thomas
RUN mkdir /app/avishek


RUN pip3 install psycopg2-binary

COPY [ "./server.py", "/app" ]
COPY [ "./add_data_to_db.py", "/app" ]