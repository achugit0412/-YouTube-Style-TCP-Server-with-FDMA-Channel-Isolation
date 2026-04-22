import socket
import threading
import time
import random

# ─────────────────────────────────────────
# Thread lock (important for shared data)
# ─────────────────────────────────────────
lock = threading.Lock()

# ─────────────────────────────────────────
# FDMA Channel Table (Fixed Bandwidth)
# ─────────────────────────────────────────
FDMA_CHANNELS = {
    "music":  {"freq": "88.1 MHz",  "bw": 200, "users": []},
    "gaming": {"freq": "92.5 MHz",  "bw": 200, "users": []},
    "tech":   {"freq": "97.3 MHz",  "bw": 200, "users": []},
    "sports": {"freq": "101.1 MHz", "bw": 200, "users": []},
    "news":   {"freq": "105.7 MHz", "bw": 200, "users": []},
}

# ─────────────────────────────────────────
# Content Database
# ─────────────────────────────────────────
CONTENT_DB = {
    "music": [
        "Top Guitar Solos 2024",
        "Lo-Fi Beats Study",
        "Beat Making Tutorial",
    ],
    "gaming": [
        "Minecraft 1.21 Update",
        "Valorant Aim Guide",
        "GTA VI Leak Analysis",
    ],
    "tech": [
        "Python Full Course",
        "TCP/IP Explained",
        "Linux Commands Guide",
    ],
    "sports": [
        "IPL Highlights",
        "NBA Finals",
        "Wimbledon Finals",
    ],
    "news": [
        "AI Regulation Update",
        "Mars Mission 2026",
        "Global Economy News",
    ],
}

# ─────────────────────────────────────────
# CLIENT HANDLER
# ─────────────────────────────────────────
def handle_client(conn, addr):
    print(f"[SERVER] Connected: {addr}")

    user_id = f"{addr[0]}:{addr[1]}"
    current_channel = None

    conn.sendall(b"\n=== FDMA YouTube TCP Server ===\n")
    conn.sendall(b"JOIN <channel> | SEARCH <word> | RECOMMEND | LIST | QUIT\n")
    conn.sendall(b">> ")

    while True:
        try:
            data = conn.recv(1024).decode().strip()
            if not data:
                break

            parts = data.split(maxsplit=1)
            cmd = parts[0].upper()
            arg = parts[1].lower() if len(parts) > 1 else ""

            # ─────────────────────────────
            # JOIN CHANNEL
            # ─────────────────────────────
            if cmd == "JOIN":
                if arg not in FDMA_CHANNELS:
                    response = "[ERROR] Unknown channel\n"
                else:
                    with lock:
                        # remove from old channel
                        if current_channel and user_id in FDMA_CHANNELS[current_channel]["users"]:
                            FDMA_CHANNELS[current_channel]["users"].remove(user_id)

                        current_channel = arg
                        channel = FDMA_CHANNELS[arg]

                        # add user safely (no duplicates)
                        if user_id not in channel["users"]:
                            channel["users"].append(user_id)

                        num_users = len(channel["users"])
                        bw_per_user = channel["bw"] / num_users

                    response = (
                        f"\n[FDMA] Tuned → {arg.upper()} | {channel['freq']}\n"
                        f"Total BW: {channel['bw']} kHz\n"
                        f"Users: {num_users}\n"
                        f"Your Share: {bw_per_user:.2f} kHz\n"
                    )

            # ─────────────────────────────
            # SEARCH
            # ─────────────────────────────
            elif cmd == "SEARCH":
                if not current_channel:
                    response = "[ERROR] Join a channel first\n"
                else:
                    results = [
                        v for v in CONTENT_DB[current_channel]
                        if arg in v.lower()
                    ]
                    response = "\n".join(results) if results else "No results found"

            # ─────────────────────────────
            # RECOMMEND
            # ─────────────────────────────
            elif cmd == "RECOMMEND":
                if not current_channel:
                    response = "[ERROR] Join a channel first\n"
                else:
                    picks = random.sample(
                        CONTENT_DB[current_channel],
                        k=min(2, len(CONTENT_DB[current_channel]))
                    )
                    response = "\n".join(picks)

            # ─────────────────────────────
            # LIST CHANNELS
            # ─────────────────────────────
            elif cmd == "LIST":
                response = "\n[CHANNEL STATUS]\n"

                with lock:
                    for name, info in FDMA_CHANNELS.items():
                        users = len(info["users"])
                        bw = info["bw"]
                        bw_share = bw / users if users > 0 else bw

                        active = " ← YOU" if name == current_channel else ""

                        response += (
                            f"{name:<8} | {info['freq']} | "
                            f"Users: {users} | BW/User: {bw_share:.2f} kHz{active}\n"
                        )

            # ─────────────────────────────
            # QUIT
            # ─────────────────────────────
            elif cmd == "QUIT":
                response = "[SERVER] Goodbye!\n"
                conn.sendall(response.encode())
                break

            else:
                response = "[ERROR] Invalid command\n"

            conn.sendall((response + "\n>> ").encode())

        except Exception as e:
            print("[ERROR]", e)
            break

    # ─────────────────────────────
    # CLEANUP
    # ─────────────────────────────
    with lock:
        if current_channel and user_id in FDMA_CHANNELS[current_channel]["users"]:
            FDMA_CHANNELS[current_channel]["users"].remove(user_id)

    conn.close()
    print(f"[SERVER] Disconnected: {addr}")


# ─────────────────────────────────────────
# SERVER
# ─────────────────────────────────────────
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("127.0.0.1", 9090))
    server.listen(5)

    print("[SERVER] Running on port 9090...")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()


# ─────────────────────────────────────────
# CLIENT
# ─────────────────────────────────────────
def start_client():
    time.sleep(0.5)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 9090))

    def receive():
        while True:
            try:
                msg = client.recv(4096).decode()
                if not msg:
                    break
                print(msg, end="")
            except:
                break

    threading.Thread(target=receive, daemon=True).start()

    while True:
        try:
            msg = input()
            client.sendall(msg.encode() + b"\n")
            if msg.upper() == "QUIT":
                break
        except:
            break

    client.close()


# ─────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────
if __name__ == "__main__":
    threading.Thread(target=start_server, daemon=True).start()
    start_client()