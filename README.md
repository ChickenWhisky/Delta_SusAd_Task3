# Delta SysAd Task-3

Hello and welcome to my Delta Inductions Task 3 for the Sysad domain.
To begin open up the terminal and enter the following commands

## Setup

To initialise the reverse proxy and server mess.txt 
```bash
$ chmod +x ./initialise.sh
$ ./initialise.sh
```

To activate the server and setup phpadmin and the userdetails website
```bash
$ docker compose up --build
```

To add data to the Postgress database
```bash
$ python3 ./add_data_to_db.py
```
To run the cronjob to back up data periodically
```bash
$ ./cronjob_setter.sh
```

## Normal Mode

- [ ] Make a File Server and client
    - [ ] Use any Programming language of choice (Python recommended) to create a Client-Server architecture with sockets. The server should accept multiple clients at the same time.
    - [ ] Implement compression while uploading and decompression while downloading the files (any compression format can be used). Whenever a user uploads any file to the server, it should be compressed and stored on the server and the server should return the file name with which it is stored (for example, if dummy.txt is uploaded, it will return "file stored as dummy.zip"). While downloading, the user will specify the file and that file will be decompressed and sent to the client.
- [ ] Add authentication

    - [ ] Implement user authentication while conecting to the server. You can add the user entries (password and username) in db beforehand, a dedicated signup page is not necessary.
    - [ ] A user should only be able to access their own files.
- [ ] Dockerise the server
    - [ ] Using docker-compose, Dockerise the server and the db.
    - [ ] The files should be persistent.

## Superuser Mode

- [ ] Client should be able to specify a folder to upload.
- [ ] They should be able to search for files using regex.
- [ ] Add feature to be able to remove files.
- [ ] Encrypt the files being transferred (using AES-256).