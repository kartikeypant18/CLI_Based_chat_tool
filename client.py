from tarfile import ENCODING  # Import the `ENCODING` variable from the `tarfile` module
import threading  # Import the `threading` module for handling concurrent operations
import socket  # Import the `socket` module for networking

nickname = input("Enter nickname: ")  # Get the user's nickname as input

ENCODING = "ascii"  # Default encoding for data communication

# Create a socket object using IPv4 address family (AF_INET) and TCP protocol (SOCK_STREAM)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server with the specified IP address and port number
client.connect(('127.0.0.1', 3000))

# Function to receive messages from the server
def receive():
    while True:
        try:
            # Receive messages from the server and decode them using the specified encoding
            message = client.recv(1024).decode(ENCODING)

            # If the received message is 'NICK', send the user's nickname to the server
            if message == 'NICK':
                client.send(nickname.encode(ENCODING))
            else:
                # Otherwise, print the received message
                print(message)
        except:
            # If an error occurs during message reception, handle the error and close the client
            print("An error occurred!")
            client.close()
            break

# Function to write and send messages to the server
def write():
    while True:
        # Get user input for the message to be sent to the server
        message = f'{nickname}: {input("")}'

        # Send the message to the server, encoded using the specified encoding
        client.send(message.encode(ENCODING))

# Create a thread to receive messages from the server concurrently
receive_thread = threading.Thread(target=receive)
receive_thread.start()

# Create a thread to write and send messages to the server concurrently
write_thread = threading.Thread(target=write)
write_thread.start()
