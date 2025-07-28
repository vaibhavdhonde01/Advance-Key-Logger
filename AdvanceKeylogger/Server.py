import socket
import threading
import os

# === CONFIG ===
HOST = '0.0.0.0'       # Accept connections from any IP
PORT = 12345
LOG_FOLDER = "received_logs"

# === Ensure logs folder exists ===
if not os.path.exists(LOG_FOLDER):
    os.makedirs(LOG_FOLDER)

# === Handle each client ===
def handle_client(conn, addr):
    print(f"[+] Connection from {addr}")
    session_file = os.path.join(LOG_FOLDER, f"log_{addr[0].replace('.', '_')}.txt")

    with conn:
        with open(session_file, "a") as f:
            while True:
                try:
                    data = conn.recv(1024)
                    if not data:
                        break
                    decoded = data.decode("utf-8")
                    print(f"{addr}: {decoded}")
                    f.write(decoded)
                except ConnectionResetError:
                    break
    print(f"[-] Disconnected from {addr}")

# === Start the server ===
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"[+] Server listening on port {PORT}...")

    while True:
        conn, addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()

if __name__ == "__main__":
    start_server()
