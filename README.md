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
