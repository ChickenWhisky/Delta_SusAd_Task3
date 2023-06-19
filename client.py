import os
import socket
import zlib

HOST="localhost"
PORT="9999"


s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(HOST,PORT)

# Getting file location from user
file_loc=input("Enter file location(enter full path) :\n")
file=os.open(file_loc,"rb")

# Size of selected file  
file_size=os.path.getsize(file_loc)

# Compresses the file
compressed_file = zlib.compress(file, zlib.Z_BEST_COMPRESSION)  
