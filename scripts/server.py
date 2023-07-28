#  SERVER SIDE

import os                                                                           # To use various functions like finding paths and getting basenames...etc.
import socket                                                                       # To be able to send data across 
import threading                                                                    # To accept multiple users simultaneously
import zipfile                                                                      # For compression and decompression
import shutil                                                                       # To move files around
import psycopg2                                                                     # To access postgress db for authentication of user
import time
import logging                                                                       

IP = socket.gethostbyname(socket.gethostname())
PORT = 9876
ADDR = ( IP , PORT )
SIZE = 1024
FORMAT = "utf-8"
global SERVER_DATA_PATH



#______________________________________________________________________________________________________________________________________________________________________________________

def authentication_server(username, password):                                      # Function to check wether the given user exists and if user has valid credentials
                                                                                    # Connect to the PostgreSQL database
    conn = psycopg2.connect(                                                        
            host=socket.gethostbyname("db"),
            database="postgres",
            user="postgres",
            password="postgres",
            port=5432

    )
    
    cursor = conn.cursor()
    
                                                                                    # Execute a SELECT query to check the credentials
    cursor.execute("SELECT * FROM userDetails WHERE name = %s AND password = %s",(username, password))
    
    result = cursor.fetchone()                                                      # Fetch the result
    
    # Return True if the user credentials are found, else False
    if result is not None:
        if  result[1]== password and result[0] == username:
            return True
        else:
            return False
    else:
        return False
        

def compress_file(file_path):                                                       # Function that compresses a give file    
    
    base_name = os.path.basename(file_path)                                         # Extracts the base name of the file eg /delta/take/me.in basename is me.in
    file_name, _ = os.path.splitext(base_name)                                      # Splits the base name into name of file and extension eg me.in is split into me and .in 
    zip_file_name = file_name + '.zip'                                              # Adds .zip extension to the zip file name

    with zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(file_path, base_name)                                            # Compression takes place
    
    new_file_path = os.path.join(os.path.dirname(file_path), zip_file_name)       
    shutil.move(zip_file_name, new_file_path)                                       # Moves the data from the main directory to the server data directory

    return zip_file_name

def find_file(file_name,current_directory):                                                           # Function to check if a file exists in that directory
    
    file_path = os.path.join(current_directory, file_name)

    if os.path.isfile(file_path):               
        return file_path
    
    else:
        return None

def decompress_file(file_path):
    
    with zipfile.ZipFile(file_path, 'r') as zipf:
        extracted_files = zipf.namelist()
        zipf.extractall(os.path.dirname(file_path))
    
    return extracted_files

def handle_client(conn,addr):
    
    logging.info(f"[NEW CONNECTION] {addr} connected.")
    conn.send("\t\tWelcome to the File Server.\n\nPlease enter user info".encode(FORMAT))                      # Sends the user a welcome message
    
    auth_data = conn.recv(SIZE).decode(FORMAT)
    auth_data = auth_data.split("@")
    userName , passWord = auth_data[0] , auth_data[1]    
    verification_checker = authentication_server(userName , passWord)

    while True:
        
        if verification_checker:
            SERVER_DATA_PATH = "/app/data/"+userName
            conn.send(f"AUTHDONE@Welcome back {userName}.Type HELP to read about the list of avaliable commands".encode(FORMAT))            
            # time.sleep(0.10)
            while True :
                data = conn.recv(SIZE).decode(FORMAT)
                data = data.split("@")
                cmd = data[0]
                if cmd == "LIST":
                    files = os.listdir(SERVER_DATA_PATH)
                    send_data = "OK@"

                    if len(files) == 0:
                            send_data += "The server directory is empty"
                    else:
                        send_data += "\n".join(f for f in files)
                    conn.send(send_data.encode(FORMAT))

                elif cmd == "UPLOAD_FILE":
                    name, text = data[1], data[2]
                    filepath = os.path.join(SERVER_DATA_PATH, name)
                    with open(filepath, "w") as f:
                        f.write(text)
                    compressed_file_name=compress_file(filepath)
                    logging.info(f"New file {compressed_file_name} created\n")    
                    os.system(f"rm {filepath}")

                    send_data = "OK@File uploaded successfully."
                    conn.send(send_data.encode(FORMAT))

                elif cmd == "DOWNLOAD" :
                    name = data[1]
                    send_data = "OK@"
                    file_path=find_file(name,SERVER_DATA_PATH)
                    
                    if file_path is None :
                        send_data += "File not found."
                        conn.send(send_data.encode(FORMAT))

                    else:
                        list_of_file_names_in_zip_folder=decompress_file(file_path)
                        for i in list_of_file_names_in_zip_folder:
                            with open(f"{SERVER_DATA_PATH}/{i}", "r") as f:
                                data = f.read()
                            send_data += f"{i}@{data}"
                            conn.send(send_data.encode(FORMAT))
                            os.system(f"rm {SERVER_DATA_PATH}/{i}")                                           
                            ok="OK@"
                            conn.send(ok.encode(FORMAT))
                            
                elif cmd == "FILE_DOESNT_EXIST" :
                    ok="OK@"
                    conn.send(ok.encode(FORMAT))

                elif cmd == "DELETE":
                    files = os.listdir(SERVER_DATA_PATH)
                    send_data = "OK@"
                    filename = data[1]

                    if len(files) == 0:
                        send_data += "The server directory is empty"
                    else:
                        if filename in files:
                            os.system(f"rm {SERVER_DATA_PATH}/{filename}")
                            send_data += "File deleted successfully."
                        else:
                            send_data += "File not found."

                    conn.send(send_data.encode(FORMAT))

                elif cmd == "LOGOUT":
                    break

                elif cmd == "HELP":
                    data = "OK@"
                    data += "LIST: List all the files from the server.\n"
                    data += "DOWNLOAD <filename> Downloads a file from the server.\n"
                    data += "UPLOAD_FILE <path>: Upload a file to the server.\n"
                    data += "UPLOAD_FOLDER <path>: Upload a folder to the server.\n"
                    data += "DELETE <filename>: Delete a file from the server.\n"
                    data += "LOGOUT: Disconnect from the server.\n"
                    data += "HELP: List all the commands."

                    conn.send(data.encode(FORMAT))
                    
                elif cmd == '':
                    data="OK@Invalid command. Type HELP to veiw all commands"
                    conn.send(data.encode(FORMAT))
                
                else:
                    data="OK@Invalid command. Type HELP to veiw all commands"
                    conn.send(data.encode(FORMAT))
                    
            logging.info(f"[DISCONNECTED]@{addr} disconnected\n")
            conn.close()
        
        else :

            conn.send("OK@Invalid Username or Password. Please enter valid credentials.".encode(FORMAT))
            conn.close()
            logging.info(f"[DISCONNECTED]@{addr} disconnected\n")
            break
        

    



def main():
    logging.info("[STARTING] Server is starting")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    logging.info(f"[LISTENING] Server is listening on {IP}:{PORT}.")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        logging.info(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}\n")

if __name__ == "__main__":
    main()