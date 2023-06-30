# Delta SysAd Task-3

Hello and welcome to my Delta Inductions Task 3 for the Sysad domain.
To begin open up the terminal and enter the following commands

## Setup

Will be updated Soon

## Normal Mode

- [ ] Make a File Server and client
    - [X] Implement Listing out all the available files
    - [ ] Implement Download files
    - [X] Implement Upload files
    - [X] Implement Download files
    - [X] Implement Logout 
    - [X] Implement HELP command
    - [ ] Implement compression

- [ ] Add authentication

    - [ ] Implement user authentication while conecting to the server. You can add the user entries (password and username) in db beforehand, a dedicated signup page is not necessary.
    - [ ] A user should only be able to access their own files.

- [ ] Dockerise the server
    - [ ] Using docker-compose, Dockerise the server and the db.
    - [ ] The files should be persistent.

## Superuser Mode

- [ ] Client should be able to specify a folder to upload.
- [ ] They should be able to search for files using regex.
- [X] Add feature to be able to remove files.
- [ ] Encrypt the files being transferred (using AES-256).

## Notes
For Upload Purposes
    Figure out the threading process.(DONE)
    Figure out how to save the file as required in the according user directory
For download purposes
    Figure out what input should we take from the user and how to use it to find the file in the server
    Figure out where to download the decompressed files