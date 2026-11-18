<img width="931" height="895" alt="Screenshot 2026-11-18 040603" src="https://github.com/user-attachments/assets/7362abc2-c61d-4e3c-aa34-cb5a3b34ff6a" />
<img width="934" height="892" alt="Screenshot 2026-11-18 040625" src="https://github.com/user-attachments/assets/c459c4aa-fc31-4e61-ab8a-8e43ab0ebaf8" />
<img width="938" height="896" alt="Screenshot 2026-11-18 040646" src="https://github.com/user-attachments/assets/677ed5d8-08c2-44f9-b27c-6d6388ac83ee" />




# NOVA Messenger

A lightweight Python desktop messaging application built with Tkinter and socket programming.

## Features

- Modern graphical user interface using Tkinter.
- Client-server architecture.
- Real-time messaging between connected clients.
- Multiple simultaneous users.
- Online users list.
- Unique display names for active users.
- Multi-threaded server and client communication.
- JSON-based message exchange.
- Connection status monitoring.
- Offline-style local network communication.

## Technologies

- Python
- Tkinter
- Socket Programming
- Threading
- JSON
- Queue

## Project Structure

```text
PYTHON_MASSENGER/
│
├── client.py
└── server.py
```

## Installation

No external Python packages are required.

Python 3.x is required.

## How to Run

**1. Start the server:**

```bash
python server.py
```

**2. Start the client:**

```bash
python client.py
```

**3. Connect using a display name and start chatting!**

## Network Configuration

By default, the client connects to:

```python
HOST = '127.0.0.1'
PORT = 5000
```

This configuration is intended for connections on the same computer.

To connect from other devices on the same network, change the client's HOST to the server computer's local IP address.

## Notes

- Start the server before launching clients.
- The server supports multiple simultaneous connections.
- This project is intended for local network communication and does not currently implement end-to-end encryption.

## Author

0MORADI0

GitHub: https://github.com/0MORADI0
