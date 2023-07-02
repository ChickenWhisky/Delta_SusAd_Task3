FROM ubuntu
RUN apt update
RUN apt -y upgrade
RUN apt install -y sudo acl wget git netcat
RUN apt-get -y install at
RUN useradd -m -d /home/SERVER SERVER
COPY [ "./server.py", "/home/SERVER" ]