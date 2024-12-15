import socket
import os
HOST = '127.0.0.1'

PORT = 4000
STORAGE_DIR = './fragments/'
FRAGMENT_SIZE = 1024
def handle_client(client_socket):
command = client_socket.recv(1024).decode()
if command.startswith("UPLOAD"):
_, filename = command.split("|")
print(f"Receiving file: {filename}")
file_data = b""
while True:
chunk = client_socket.recv(1024)
if not chunk:
break
file_data += chunk
fragments = [file_data[i:i + FRAGMENT_SIZE] for i in

range(0, len(file_data), FRAGMENT_SIZE)]
if not os.path.exists(STORAGE_DIR):
os.makedirs(STORAGE_DIR)
for i, fragment in enumerate(fragments):
with open(os.path.join(STORAGE_DIR,

f"{filename}.part{i+1}"), "wb") as f:
f.write(fragment)

print(f"File {filename} stored as {len(fragments)}
fragments.")

client_socket.sendall(b"File uploaded and stored as

fragments.")
elif command.startswith("DOWNLOAD"):
_, filename, num_parts = command.split("|")
num_parts = int(num_parts)
print(f"Reassembling file: {filename}")
file_data = b""
for i in range(1, num_parts + 1):

fragment_path = os.path.join(STORAGE_DIR,

f"{filename}.part{i}")

with open(fragment_path, "rb") as f:
file_data += f.read()
client_socket.sendall(file_data)
print(f"File {filename} sent to client.")
client_socket.close()
def start_server():
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as
server_socket:

server_socket.bind((HOST, PORT))
server_socket.listen()
print(f"Server listening on {HOST}:{PORT}")
while True:
client_socket, address = server_socket.accept()
print(f"Client connected from {address}")
handle_client(client_socket)

if __name__ == "__main__":
start_server()