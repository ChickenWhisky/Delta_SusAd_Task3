FROM python:3.9-alpine

WORKDIR /app 
COPY [ "./scripts/server.py", "." ]

RUN mkdir -p ./data/thomas
RUN mkdir ./data/avishek
RUN pip install --upgrade pip
RUN pip3 install psycopg2-binary
RUN pip3 install pycryptodome   


CMD [ "python3" , "server.py" ] 