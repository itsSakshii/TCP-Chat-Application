# client_socket.py
# ─────────────────────────────────────────────────────────────────────────────
# Simple console-based TCP client for testing the server
# Run this in a terminal AFTER starting server.py
# ─────────────────────────────────────────────────────────────────────────────

import socket
import threading
import sys

HOST = '127.0.0.1'
PORT = 12345


def receive_messages(sock: socket.socket):
    """
    Runs in a background thread — continuously listens for incoming messages
    from the server and prints them.  Running this in a thread means we can
    type AND receive at the same time (non-blocking).
    """
    while True:
        try:
            data = sock.recv(4096)
            if not data:
                print("[DISCONNECTED from server]")
                break
            print(data.decode('utf-8'))   # print message from server/other clients
        except Exception:
            break


def start_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((HOST, PORT))
        # TCP three-way handshake happens here:
        # Client sends SYN  →  Server responds SYN-ACK  →  Client sends ACK
        print(f"[CONNECTED] to {HOST}:{PORT}")
    except ConnectionRefusedError:
        print("[ERROR] Cannot connect — is server.py running?")
        sys.exit(1)

    # Handle the username prompt from the server
    prompt = sock.recv(1024).decode('utf-8')
    username = input(prompt).strip()
    sock.send(username.encode('utf-8'))

    # Start background receive thread BEFORE entering the send loop
    recv_thread = threading.Thread(target=receive_messages, args=(sock,), daemon=True)
    recv_thread.start()

    # Main thread handles user input (send loop)
    print("Type your message and press Enter.  Type 'quit' to exit.")
    while True:
        try:
            msg = input()
            if msg.lower() == 'quit':
                break
            if msg.strip():                     # don't send empty lines
                sock.send(msg.encode('utf-8'))
        except (EOFError, KeyboardInterrupt):
            break

    sock.close()
    print("[DISCONNECTED]")


if __name__ == "__main__":
    start_client()