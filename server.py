
import os
import socket
import threading
import zipfile
import shutil


IP = socket.gethostbyname(socket.gethostname())
PORT = 9996
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_DATA_PATH = "server_data"                                                    # Temporarily for testing sake we add all the users data in here

def compress_file(file_path):
    base_name = os.path.basename(file_path)                                         # Extracts the base name of the file eg /delta/take/me.in basename is me.in
    file_name, _ = os.path.splitext(base_name)                                      # Splits the base name into name of file and extension eg me.in is split into me and .in 
    zip_file_name = file_name + '.zip'                                              # Adds .zip extension to the zip file name

    with zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(file_path, base_name)                                            # Compression takes place
    new_file_path = os.path.join(os.path.dirname(file_path), zip_file_name)       
    shutil.move(zip_file_name, new_file_path)                                       # Moves the data from the main directory to the server data directory

    return zip_file_name

        
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    conn.send("OK@Welcome to the File Server. \
    Type HELP to read about the list of avaliable commands".encode(FORMAT))         # Sends the user a welcome message
    
    while True:
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

        elif cmd == "UPLOAD":
            name, text = data[1], data[2]
            filepath = os.path.join(SERVER_DATA_PATH, name)
            print(filepath)
            with open(filepath, "w") as f:
                f.write(text)
            compressed_file_name=compress_file(filepath)
            print(f"New file {compressed_file_name} created")    
            os.system(f"rm {filepath}")

            send_data = "OK@File uploaded successfully."
            conn.send(send_data.encode(FORMAT))

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
            data += "UPLOAD <path>: Upload a file to the server.\n"
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
            


    print(f"[DISCONNECTED] {addr} disconnected")
    conn.close()

def main():
    print("[STARTING] Server is starting")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}.")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    main()