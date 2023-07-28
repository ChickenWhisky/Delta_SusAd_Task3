FROM python:3.9-alpine

WORKDIR /app 
COPY [ "./scripts/server.py", "." ]

RUN mkdir -p ./data/thomas
RUN mkdir ./data/avishek

RUN pip3 install psycopg2-binary

CMD [ "python3" , "server.py" ] 