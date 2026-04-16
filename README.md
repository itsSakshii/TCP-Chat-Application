# 💬 Client–Server Chat Application using TCP & Streamlit

## 📌 Project Overview

This project is a **Client–Server Chat Application** built using **TCP Socket Programming** with a **Streamlit-based UI**. It demonstrates real-time communication between multiple clients connected to a centralized server.

The application showcases core **Computer Networks concepts** such as TCP handshake, reliable data transmission, and socket-based communication, along with a simple and interactive user interface.

---

## 🎯 Objectives

- Implement **Client–Server architecture**
- Enable **real-time chat between multiple users**
- Use **TCP sockets for reliable communication**
- Build an interactive **web UI using Streamlit**
- Visualize network communication using **Wireshark**

---

## 🛠️ Tech Stack

- **Python**
- **Socket Programming (TCP)**
- **Streamlit (Frontend UI)**
- **Threading / Multi-client Handling**
- **Wireshark (Network Analysis)**

---

## 📂 Project Structure
client-server-chat/
│
├── server.py # Server-side code (handles multiple clients)
├── client.py # Basic socket client
├── streamlit_app.py # Streamlit UI client
├── requirements.txt # Dependencies
└── README.md # Project documentation


---

## ⚙️ Features

- ✅ Multi-client chat support
- ✅ Real-time messaging
- ✅ TCP-based reliable communication
- ✅ Streamlit UI for user interaction
- ✅ Broadcast messaging (Client ↔ Client)
- ✅ Graceful connection handling
- ✅ Easy to understand and beginner-friendly

---

## 🔄 How It Works

1. The server starts and listens for incoming connections.
2. Multiple clients connect using IP address and port.
3. A TCP connection is established (3-way handshake).
4. Messages sent by one client are **broadcasted** to all connected clients.
5. The Streamlit UI displays messages dynamically.
6. Wireshark can be used to monitor packet flow.

---



🔧 Future Enhancements
🔐 User authentication system
💾 Chat history storage (database)
👤 Username support
🔒 Private messaging
🌐 Deployment on cloud




Wireshark Capture (Network Proof)

Your Wireshark filter:

tcp.port == 12345

This means you are capturing traffic for your chat server port (12345).

Packets visible:

[SYN]
[SYN, ACK]
[ACK]

This is the TCP 3-way handshake:

1️⃣ Client → Server

SYN

2️⃣ Server → Client

SYN ACK

3️⃣ Client → Server

ACK

✅ This proves TCP connection establishment is working.

Then you also see:

PSH, ACK

Example from screenshot:

[PSH, ACK] Len=21
[PSH, ACK] Len=6

PSH = Push data immediately to application

Meaning:

➡ Actual chat messages are being transmitted

So Wireshark confirms:

✔ TCP connection established
✔ Data packets transferred
✔ Acknowledgements received

3️⃣ Why Source and Destination are 127.0.0.1

You see:

Source: 127.0.0.1
Destination: 127.0.0.1

That means:

Both clients are running on the same computer.

This is called:

Loopback interface

So traffic goes:

Client → localhost → Server → localhost → Client

Which is totally normal during testing.

4️⃣ Port Numbers in Screenshot

Example packet:

Src Port: 12345
Dst Port: 55523
12345 → your server port
55523 / 60403 → client ephemeral ports
