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
