import os
import socket
import zipfile
import getpass


IP = socket.gethostbyname("localhost")
PORT = 9876
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024
CLIENT_DATA_PATH = os.getcwd()                    # Gets Current directory of client                   
# Functions for the program

def decompress_file(file_path):
    with zipfile.ZipFile(file_path, 'r') as zipf:
        zipf.extractall(os.path.dirname(file_path))

    extracted_files_names = zipf.namelist()
    return extracted_files_names

def rename_file_to_zip(file_name):
    new_file_name = os.path.splitext(file_name)[0] + ".zip"

    return new_file_name

def input_as_stars():
    # Use getpass to get user input without displaying it
    password = getpass.getpass()
    
    return password


# Main function

def main():
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    
    
    data = client.recv(SIZE).decode(FORMAT)                                         # Please enter user info
    data = data.split("@")
    msg = data[0]
    print(f"{msg}")
    
    userName=input("Username:   ")                                                  # User enters credentials
    passWord=input_as_stars()
    client.send(f"{userName}@{passWord}".encode(FORMAT))
    
    data = client.recv(SIZE).decode(FORMAT)
    data = data.split("@")
    cmd , display_msg = data[0] , data[1] 

    if cmd == "AUTHDONE":
        print(display_msg)
        while True:
            
            data = input("$ ") or "random string so that program doesnt break"
            data = data.split(" ")
            cmd = data[0]
            cmd_to_be_sent = cmd+"@@"

            if cmd == "HELP" or cmd == "help":
                client.send(cmd_to_be_sent.encode(FORMAT))
                
            elif cmd == "LOGOUT" or cmd == "logout":
                client.send(cmd_to_be_sent.encode(FORMAT))
                break

            elif cmd == "LIST" or cmd == "list":
                client.send(cmd_to_be_sent.encode(FORMAT))
                
            elif cmd == "DELETE" or cmd == "delete":
                client.send(f"{cmd}@{data[1]}@".encode(FORMAT))
                
            elif cmd == "UPLOAD" or cmd == "upload":
                path = os.path.join(CLIENT_DATA_PATH, data[1])
                if os.path.isfile(path) :
                    with open(f"{path}", "r") as f:
                        text = f.read()
                    filename = path.split("/")[-1]
                    send_data = f"{cmd}@{filename}@{text}"
                    client.send(send_data.encode(FORMAT))
                    
                # else :
                #     print("File doesnt exist")
                #     send_data="FILE_DOESNT_EXIST@@"
                #     client.send(send_data.encode(FORMAT))
                
            elif cmd == "DOWNLOAD" or cmd == "download":
                try:
                    client.send(f"{cmd}@{data[1]}@".encode(FORMAT))
                    data1 = client.recv(SIZE).decode(FORMAT)
                    data1 = data1.split("@")
                    name = data1[1]
                    
                    if name == "File not found." :
                        print(f"<{name}>")
                    else :
                        text = data1[2]
                        filepath = os.path.join(CLIENT_DATA_PATH, name)
                        with open(filepath, "w") as f:
                            f.write(text)
                        print(f"New file {name} created")    
                except:
                    print("<No path entered>")
                
            else:
                client.send(cmd_to_be_sent.encode(FORMAT))
            
            
            data = client.recv(SIZE).decode(FORMAT)
            data = data.split("@")
            cmd , msg = data[0] , data[1]
            
            if cmd == "DISCONNECTED":                                               
                print(f"[SERVER]: {msg}")
                break
            elif cmd == "OK":
                print(f"{msg}")
            elif cmd == "ERROR":
                print(f"<{msg}>")
                
        print("Disconnected from the server.")
        client.close()
    else:
        client.close()
        print(display_msg)
        
        
if __name__ == "__main__":
    main()