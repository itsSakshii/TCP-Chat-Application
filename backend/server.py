# server.py
# ─────────────────────────────────────────────────────────────────────────────
# TCP Chat Server — handles multiple clients simultaneously using threads
# Each client gets its own thread; messages are broadcast to all other clients
# ─────────────────────────────────────────────────────────────────────────────

import socket
import threading

# ── Configuration ──────────────────────────────────────────────────────────
HOST = '127.0.0.1'   # localhost — change to '0.0.0.0' to allow LAN connections
PORT = 12345         # port number (must match what clients use)

# ── Shared state ───────────────────────────────────────────────────────────
# clients: list of (socket, username) tuples for every connected client
clients = []
# lock: prevents two threads from modifying the clients list at the same time
lock = threading.Lock()


def broadcast(message: str, sender_socket=None):
    """
    Send a message to every connected client EXCEPT the sender.
    Uses the lock so the clients list isn't modified mid-loop.
    """
    with lock:
        for client_socket, username in clients:
            if client_socket != sender_socket:   # don't echo back to sender
                try:
                    client_socket.send(message.encode('utf-8'))
                except Exception:
                    # If sending fails the client probably disconnected — ignore here,
                    # the handle_client thread will clean it up
                    pass


def handle_client(client_socket: socket.socket, addr):
    """
    Runs in its own thread, one per connected client.
    1. Ask the client for a username
    2. Loop: receive messages and broadcast them
    3. On disconnect, remove client from the list and notify others
    """
    print(f"[+] New connection from {addr}")

    # ── Step 1: receive username ──────────────────────────────────────────
    try:
        client_socket.send("Enter your username: ".encode('utf-8'))
        username = client_socket.recv(1024).decode('utf-8').strip()
        if not username:
            username = str(addr)   # fallback if client sends nothing
    except Exception:
        client_socket.close()
        return

    # ── Register client ───────────────────────────────────────────────────
    with lock:
        clients.append((client_socket, username))

    join_msg = f"[SERVER] {username} has joined the chat!"
    print(join_msg)
    broadcast(join_msg, sender_socket=client_socket)

    # ── Step 2: message receive loop ──────────────────────────────────────
    while True:
        try:
            data = client_socket.recv(4096)      # receive up to 4 KB
            if not data:                          # empty = client closed connection
                break
            message = data.decode('utf-8')
            full_msg = f"[{username}]: {message}"
            print(full_msg)
            broadcast(full_msg, sender_socket=client_socket)

        except ConnectionResetError:
            # Windows raises this when the client closes abruptly
            break
        except Exception as e:
            print(f"[ERROR] {addr}: {e}")
            break

    # ── Step 3: clean up on disconnect ────────────────────────────────────
    with lock:
        clients[:] = [(s, u) for s, u in clients if s != client_socket]

    client_socket.close()
    leave_msg = f"[SERVER] {username} has left the chat."
    print(leave_msg)
    broadcast(leave_msg)


def start_server():
    """
    Create the listening socket and accept incoming connections forever.
    TCP three-way handshake happens automatically when a client calls connect().
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # AF_INET  = IPv4
    # SOCK_STREAM = TCP (reliable, ordered, connection-oriented)

    # SO_REUSEADDR lets us restart the server quickly without "Address in use" error
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((HOST, PORT))   # bind socket to IP:PORT
    server_socket.listen(10)           # allow up to 10 queued connections

    print(f"[SERVER STARTED] Listening on {HOST}:{PORT}")
    print("Waiting for clients to connect... (Ctrl+C to stop)")

    try:
        while True:
            # accept() BLOCKS here until a client connects
            # TCP three-way handshake (SYN → SYN-ACK → ACK) happens during accept()
            client_socket, addr = server_socket.accept()

            # Spin up a new thread so this client doesn't block others
            thread = threading.Thread(
                target=handle_client,
                args=(client_socket, addr),
                daemon=True    # daemon=True: thread dies automatically if server exits
            )
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {len(clients) + 1}")

    except KeyboardInterrupt:
        print("\n[SERVER STOPPED]")
    finally:
        server_socket.close()


if __name__ == "__main__":
    start_server()