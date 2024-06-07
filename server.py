import socket
import threading
import time
import redis
import json

# Function to handle client connection
def handle_client(client_socket, addr, redis_client):
    print(f"Got a connection from {addr}")

    # Send initial message to the client
    initial_message = 'Welcome! server says hi'
    client_socket.send(initial_message.encode('ascii'))

    # Receive data from the client and save to Redis
    while True:
        try:
            data = client_socket.recv(1024).decode('ascii')
            if not data:
                print("Connection closed by client")
                break
            print("Data from client:", data)

            # Parse JSON data
            try:
                json_data = json.loads(data)
                id = json_data["id"]
                name = json_data["name"]
                vital_sign = json_data["vital_sign"]
                value = json_data["value"]
                num = float(value)
            except ValueError:
                client_socket.send("Invalid JSON format. Please send JSON object with fields 'id', 'name', 'vital_sign', and 'value'.".encode('ascii'))
                continue

            # Construct the Redis key
            redis_key = f"{id}_{name}_{vital_sign}"

            # Save the value to Redis under the constructed key
            redis_client.rpush(redis_key, num)

            # Retrieve the list of values from Redis under the constructed key
            values = redis_client.lrange(redis_key, 0, -1)

            # Construct JSON response with the list of values
            response = {
                "id": id,
                "name": name,
                "vitalSign": vital_sign,
                "values": [float(value) for value in values]  # Convert values to float and include in the response
            }

            # Send JSON response to the client
            json_response = json.dumps(response)
            client_socket.send(json_response.encode('ascii'))

            time.sleep(1)  # Wait for 1 second before receiving the next data
        except ConnectionResetError:
            print(f"Connection with {addr} was closed.")
            break

# Server setup
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '0.0.0.0'  # Listen on all interfaces
port = 12345
server_socket.bind((host, port))
server_socket.listen(5)

# Connect to Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Print the IP address the server is working on
print("Server is running on IP:", socket.gethostbyname(socket.gethostname()))
print(f"Listening on {host}:{port}...")

# Accept connections and handle them in separate threads
while True:
    client_socket, addr = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket, addr, redis_client))
    client_thread.start()
