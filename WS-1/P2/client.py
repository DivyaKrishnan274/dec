import socket
HOST = '127.0.0.1'
PORT = 4000
def upload_file(filename):
with open(filename, "rb") as f:
file_data = f.read()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as
client_socket:

client_socket.connect((HOST, PORT))

client_socket.sendall(f"UPLOAD|{filename}".encode())
client_socket.sendall(file_data)
response = client_socket.recv(1024).decode()
print(response)

def download_file(filename, num_parts):
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as
client_socket:

client_socket.connect((HOST, PORT))

client_socket.sendall(f"DOWNLOAD|{filename}|{num_parts}".encode())

with open(f"downloaded_{filename}", "wb") as f:
while True:
data = client_socket.recv(1024)
if not data:
break
f.write(data)

print(f"File {filename} downloaded successfully.")

if __name__ == "__main__":
choice = input("Do you want to upload or download a file?
(upload/download): ")
filename = input("Enter the file name: ")
if choice == "upload":
upload_file(filename)
elif choice == "download":
num_parts = int(input("Enter the number of parts: "))
download_file(filename, num_parts)