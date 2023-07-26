# Delta SysAd Task-3

Hello and welcome to my Delta Inductions Task 3 for the Sysad domain.
To begin open up the terminal and enter the following commands

## Setup

```bash
$ docker compose up --build
```

To add data to the Postgress database
```bash
$ python3 ./add_data_to_db.py
```

## Normal Mode

- [X] Make a File Server and client
    - [X] Implement Listing out all the available files
    - [X] Implement Download files
    - [X] Implement Upload files
    - [X] Implement Download files
    - [X] Implement Logout 
    - [X] Implement HELP command
    - [X] Implement compression

- [X] Add authentication

    - [X] Implement user authentication while conecting to the server. You can add the user entries (password and username) in db beforehand, a dedicated signup page is not necessary.
    - [X] A user should only be able to access their own files.

- [X] Dockerise the server
    - [X] Using docker-compose, Dockerise the server and the db.
    - [X] The files should be persistent.

## Superuser Mode

- [ ] Client should be able to specify a folder to upload.
- [ ] They should be able to search for files using regex.
- [X] Add feature to be able to remove files.
- [ ] Encrypt the files being transferred (using AES-256).
