# Delta SUSad Task-3

To begin open up the terminal and enter the following commands

## Setup

```bash
$ docker compose up --build
```

## Client Usage
```bash
$ cd to/path/where/repo/exists
$ python3 client.py
```

## Check List

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

## Would Like to add in the future

- [ ] Client should be able to specify a folder to upload.
- [ ] They should be able to search for files using regex.
- [X] Add feature to be able to remove files.
- [ ] Encrypt the files being transferred (using AES-256).
