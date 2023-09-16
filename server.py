from base64 import encode  # Import the `encode` function from the `base64` module
from tarfile import ENCODING  # Import the `ENCODING` variable from the `tarfile` module
import threading  # Import the `threading` module for handling concurrent operations
import socket  # Import the `socket` module for networking

host = "127.0.0.1"  # Server host (local machine in this case)
port = 3000  # Server port number
ENCODING = "ascii"  # Default encoding for data communication (redefined from the tarfile import, which is not necessary)

# Create a socket object using IPv4 address family (AF_INET) and TCP protocol (SOCK_STREAM)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the specified host and port
server.bind((host, port))

# Start listening for incoming connections
server.listen()

clients = []  # List to hold all connected client sockets
nicknames = []  # List to hold nicknames of connected clients

# Function to broadcast a message to all connected clients
def broadcast(message, sender=None, is_notification=False):
    for client in clients:
        if is_notification and client != sender:
            client.send(message)
        elif not is_notification:
            client.send(message)

# Function to handle individual client connections
def handle(client):
    while True:
        try:
            # Receive messages from the client
            message = client.recv(1024)

            # Broadcast the received message to all other clients
            broadcast(message, client)
        except:
            # If an error occurs during message handling (client disconnection), clean up and notify other clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f"{nickname} left the chat!".encode(ENCODING), is_notification=True)
            nicknames.remove(nickname)
            break

# Function to accept and handle incoming client connections
def receive():
    while True:
        # Accept a new client connection
        client, address = server.accept()

        # Display connection information
        print(f"Connected with {str(address)}")

        # Prompt the client to send its nickname and decode it
        client.send('NICK'.encode(ENCODING))
        nickname = client.recv(1024).decode(ENCODING)

        # Store the client's nickname and socket in appropriate lists
        nicknames.append(nickname)
        clients.append(client)

        # Notify all other clients about the new client's joining
        print(f"Nickname of the client is {nickname}!")
        broadcast(f'{nickname} joined the chat'.encode(ENCODING), sender=client, is_notification=True)
        client.send('Connected to the server!'.encode(ENCODING))

        # Start a new thread to handle messages from this client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

# Main server code execution
print(f"Server started on {port}")
server_thread = threading.Thread(target=receive)
server_thread.start()
