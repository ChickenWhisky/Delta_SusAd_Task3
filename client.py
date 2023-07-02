import os
import socket
import zipfile
import getpass


IP = socket.gethostbyname(socket.gethostname())
PORT = 6969
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024
CLIENT_DATA_PATH = "client_data"

# Functions for the program

def decompress_file(file_path):
    with zipfile.ZipFile(file_path, 'r') as zipf:
        zipf.extractall(os.path.dirname(file_path))

    extracted_files_names = zipf.namelist()
    return extracted_files_names

def rename_file_to_zip(file_name):
    new_file_name = os.path.splitext(file_name)[0] + ".zip"

    return new_file_name

def input_as_stars(prompt):
    # Use getpass to get user input without displaying it
    password = getpass.getpass(prompt=prompt)
    
    # Return the input as stars
    return "*" * len(password)



# Main function

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    while True:
        data = client.recv(SIZE).decode(FORMAT)
        cmd, msg = data.split("@")

        if cmd == "DISCONNECTED":
            print(f"[SERVER]: {msg}")
            break
        elif cmd == "OK":
            print(f"{msg}")
        
        elif cmd == "AUTH_CHECK" :
            print(f"{msg}")
            userName=input("Username   :")
            passWord=input_as_stars("Password   :")
            client.send(f"{userName}@{passWord}")

        data = input("$ ") or "random string so that program doesnt break"
        data = data.split(" ")
        cmd = data[0]

        if cmd == "HELP":
            client.send(cmd.encode(FORMAT))

        elif cmd == "LOGOUT":
            client.send(cmd.encode(FORMAT))
            break

        elif cmd == "LIST":
            client.send(cmd.encode(FORMAT))

        elif cmd == "DELETE":
            client.send(f"{cmd}@{data[1]}".encode(FORMAT))

        elif cmd == "UPLOAD":
            path = os.path.join(CLIENT_DATA_PATH, data[1])
            if os.path.isfile(path) :
                with open(f"{path}", "r") as f:
                    text = f.read()
                filename = path.split("/")[-1]
                send_data = f"{cmd}@{filename}@{text}"
                client.send(send_data.encode(FORMAT))
            else :
                print("File doesnt exist")
                send_data="FILE_DOESNT_EXIST"
                client.send(send_data.encode(FORMAT))
            
        elif cmd == "DOWNLOAD" :
            client.send(f"{cmd}@{data[1]}".encode(FORMAT))
            data1 = client.recv(SIZE).decode(FORMAT)
            data1 = data1.split("@")
            name = data1[1]
            
            if name == "File not found." :
                print(name)
            else :
                text = data1[2]
                filepath = os.path.join(CLIENT_DATA_PATH, name)
                with open(filepath, "w") as f:
                    f.write(text)
                print(f"New file {name} created")    

            
        else:
            client.send(cmd.encode(FORMAT))

    print("Disconnected from the server.")
    client.close()

if __name__ == "__main__":
    main()