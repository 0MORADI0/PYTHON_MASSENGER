import socket, threading, json
HOST = '0.0.0.0'
PORT = 5000
clients = {}
lock = threading.Lock()

def send_packet(sock, packet):
    try:
        sock.sendall((json.dumps(packet, ensure_ascii=False) + '\n').encode('utf-8'))
        return True
    except OSError:
        return False

def broadcast(packet, exclude=None):
    with lock:
        targets = list(clients.items())
    dead = []
    for sock, username in targets:
        if sock is not exclude and not send_packet(sock, packet):
            dead.append(sock)
    for sock in dead:
        remove_client(sock)

def remove_client(sock):
    with lock:
        username = clients.pop(sock, None)
    try:
        sock.close()
    except OSError:
        pass
    if username:
        broadcast({'type': 'system', 'text': f'{username} از گفتگو خارج شد'})
        send_users()

def send_users():
    with lock:
        names = list(clients.values())
        targets = list(clients.keys())
    for sock in targets:
        send_packet(sock, {'type': 'users', 'users': names})

def handle_client(sock, address):
    username = None
    buffer = ''
    try:
        while True:
            raw = sock.recv(4096)
            if not raw:
                break
            buffer += raw.decode('utf-8', errors='replace')
            while '\n' in buffer:
                line, buffer = buffer.split('\n', 1)
                if not line.strip():
                    continue
                try:
                    packet = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if packet.get('type') == 'join':
                    wanted = str(packet.get('username', '')).strip()[:24]
                    if not wanted:
                        send_packet(sock, {'type': 'error', 'text': 'نام کاربری را وارد کنید'})
                        continue
                    with lock:
                        if wanted in clients.values():
                            send_packet(sock, {'type': 'error', 'text': 'این نام کاربری در حال حاضر آنلاین است'})
                            continue
                        clients[sock] = wanted
                    username = wanted
                    send_packet(sock, {'type': 'joined', 'username': username})
                    broadcast({'type': 'system', 'text': f'{username} وارد گفتگو شد'}, exclude=sock)
                    send_users()
                elif packet.get('type') == 'message' and username:
                    text = str(packet.get('text', '')).strip()[:4000]
                    if text:
                        broadcast({'type': 'message', 'username': username, 'text': text})
    except (OSError, ConnectionError):
        pass
    finally:
        remove_client(sock)

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(50)
    print(f'Server running on {HOST}:{PORT}')
    print('برای توقف سرور Ctrl+C را بزنید.')
    try:
        while True:
            sock, address = server.accept()
            threading.Thread(target=handle_client, args=(sock, address), daemon=True).start()
    except KeyboardInterrupt:
        print('\nServer stopped.')
    finally:
        server.close()

if __name__ == '__main__':
    main()
