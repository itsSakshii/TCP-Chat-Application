
import socket
import threading
import queue
import time
import streamlit as st

HOST = '127.0.0.1'
PORT = 12345

# ── Page config ────────────────────────────────────────────────────────────
st.set_page_config(page_title="TCP Chat", page_icon="💬", layout="centered")
st.title("💬 TCP Chat Application")
st.caption("MCA Project — Computer Networks | JIIT Noida")

# ── Session state init ─────────────────────────────────────────────────────
defaults = {
    'connected': False,
    'sock': None,
    'username': '',
    'messages': [],         
    'msg_queue': None,      
    'recv_started': False,
     'input_key': 0,  
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Step 1: drain queue into messages list ─────────────────────────────────
# This runs at the TOP of every rerun (interaction OR timer).
# The background thread never touches st.session_state directly —
# it only puts items into the queue. This avoids all race conditions.
if st.session_state.msg_queue is not None:
    q: queue.Queue = st.session_state.msg_queue
    while not q.empty():
        try:
            item = q.get_nowait()
            st.session_state.messages.append(item)
        except queue.Empty:
            break

# ── Background receive thread ──────────────────────────────────────────────
def receive_loop(sock: socket.socket, msg_queue: queue.Queue):
    """
    Runs in a daemon thread. ONLY writes to msg_queue — never to session_state.
    queue.Queue is thread-safe by design; session_state is NOT.
    """
    while True:
        try:
            data = sock.recv(4096)
            if not data:
                msg_queue.put({"sender": "SERVER", "text": "Disconnected from server."})
                break
            text = data.decode('utf-8')
            if ']: ' in text:
                sender, msg = text.split(']: ', 1)
                sender = sender.lstrip('[')
            else:
                sender = "SERVER"
                msg = text
            msg_queue.put({"sender": sender, "text": msg})
        except Exception:
            break

# ── Helper: render a single chat bubble ───────────────────────────────────
def render_bubble(msg: dict, my_username: str):
    sender = msg["sender"]
    text   = msg["text"]
    if sender == "SERVER":
        st.markdown(
            f'<div style="text-align:center;color:var(--text-color,#888);'
            f'font-size:0.8em;margin:4px 0;opacity:0.7;">ℹ️ {text}</div>',
            unsafe_allow_html=True
        )
    elif sender == my_username:
        st.markdown(
            f'<div style="text-align:right;margin:4px 0;">'
            f'<span style="background:#0078d4;color:#fff;padding:7px 13px;'
            f'border-radius:16px 16px 3px 16px;display:inline-block;'
            f'max-width:75%;word-wrap:break-word;">'
            f'<span style="font-size:0.75em;opacity:0.85;">You</span>'
            f'<br>{text}</span></div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div style="text-align:left;margin:4px 0;">'
            f'<span style="background:#e8e8e8;color:#1a1a1a;padding:7px 13px;'
            f'border-radius:16px 16px 16px 3px;display:inline-block;'
            f'max-width:75%;word-wrap:break-word;">'
            f'<span style="font-size:0.75em;color:#555;">{sender}</span>'
            f'<br>{text}</span></div>',
            unsafe_allow_html=True
        )

# ══════════════════════════════════════════════════════════════════════════
#  NOT CONNECTED — show login form
# ══════════════════════════════════════════════════════════════════════════
if not st.session_state.connected:
    st.subheader("Connect to Server")
    col1, col2 = st.columns(2)
    with col1:
        username = st.text_input("Username", placeholder="e.g. Alice")
    with col2:
        server_ip = st.text_input("Server IP", value="127.0.0.1")

    if st.button("🔌 Connect", type="primary"):
        if not username.strip():
            st.error("Please enter a username.")
        else:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((server_ip, PORT))

                # Handle server's username prompt
                sock.recv(1024)                          # "Enter your username: "
                sock.send(username.strip().encode('utf-8'))

                # Build queue and start receive thread
                msg_queue = queue.Queue()
                t = threading.Thread(
                    target=receive_loop,
                    args=(sock, msg_queue),
                    daemon=True
                )
                t.start()

                st.session_state.sock         = sock
                st.session_state.username     = username.strip()
                st.session_state.connected    = True
                st.session_state.messages     = []
                st.session_state.msg_queue    = msg_queue
                st.session_state.recv_started = True
                st.rerun()

            except ConnectionRefusedError:
                st.error("❌ Cannot connect — is server.py running?")
            except Exception as e:
                st.error(f"❌ {e}")

# ══════════════════════════════════════════════════════════════════════════
#  CONNECTED — chat interface
# ══════════════════════════════════════════════════════════════════════════
else:
    # ── Top bar ────────────────────────────────────────────────────────────
    col1, col2 = st.columns([5, 1])
    with col1:
        st.success(f"✅ Connected as **{st.session_state.username}**")
    with col2:
        if st.button("Disconnect"):
            try:
                st.session_state.sock.close()
            except Exception:
                pass
            for k, v in defaults.items():
                st.session_state[k] = v
            st.rerun()

    st.markdown("---")

    # ── Chat display (fragment = re-renders on its own timer) ──────────────
    @st.fragment(run_every=1)          # poll every 1 second — only THIS block reruns
    def chat_display():
        # Drain queue again inside fragment so new messages appear every second
        if st.session_state.msg_queue is not None:
            q: queue.Queue = st.session_state.msg_queue
            while not q.empty():
                try:
                    st.session_state.messages.append(q.get_nowait())
                except queue.Empty:
                    break

        st.subheader("Chat")
        chat_box = st.container(height=420)
        with chat_box:
            if not st.session_state.messages:
                st.info("No messages yet. Say hello! 👋")
            else:
                for msg in st.session_state.messages:
                    render_bubble(msg, st.session_state.username)

    chat_display()

    # ── Message input (outside fragment so it isn't wiped every second) ────
    # ── Message input ──────────────────────────────────────────────────────────
st.markdown("---")
col1, col2 = st.columns([5, 1])
with col1:
    message = st.text_input(
        "msg",
        placeholder="Type a message…",
        label_visibility="collapsed",
        key=f"msg_input_{st.session_state.input_key}",
    )
with col2:
    send = st.button("Send 📤", type="primary")

if send and message.strip():
    try:
        st.session_state.sock.send(message.strip().encode('utf-8'))
        st.session_state.messages.append({
            "sender": st.session_state.username,
            "text": message.strip()
        })
        st.session_state.input_key += 1
        st.rerun()
    except Exception as e:
        st.error(f"Send failed: {e}")