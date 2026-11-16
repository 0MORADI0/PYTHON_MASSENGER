import tkinter as tk
from tkinter import messagebox
import webbrowser
import socket, threading, json, queue

HOST = '127.0.0.1'  # برای دستگاه دیگر، IP کامپیوتر میزبان را اینجا بنویسید
PORT = 5000
BG = '#17212b'
PANEL = '#202d3a'
ACCENT = '#3390ec'
TEXT = '#f1f5f9'

class Messenger:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('NOVA Messenger - Offline Edition')
        self.root.geometry('760x700')
        self.root.minsize(520, 420)
        self.root.configure(bg=BG)
        self.sock = None
        self.incoming = queue.Queue()
        self.username = ''
        self.build_login()
        self.root.protocol('WM_DELETE_WINDOW', self.close)
        self.root.after(100, self.process_queue)
        self.root.mainloop()

    def build_login(self):
        self.login_frame = tk.Frame(self.root, bg=BG)
        self.login_frame.pack(expand=True)
        tk.Label(self.login_frame, text='NOVA', font=('Segoe UI', 30, 'bold'), fg=ACCENT, bg=BG).pack(pady=12)
        tk.Label(self.login_frame, text='نام نمایشی خود را وارد کنید', font=('Segoe UI', 12), fg=TEXT, bg=BG).pack(pady=8)
        self.name_entry = tk.Entry(self.login_frame, font=('Segoe UI', 13), justify='center', bg=PANEL, fg=TEXT, insertbackground=TEXT, relief='flat', width=28)
        self.name_entry.pack(ipady=10, pady=8)
        self.name_entry.bind('<Return>', lambda event: self.connect())
        tk.Button(self.login_frame, text='اتصال به گفتگو', command=self.connect, bg=ACCENT, fg='white', relief='flat', font=('Segoe UI', 11, 'bold'), padx=20, pady=9).pack(pady=12)

    def connect(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning('نام کاربری', 'یک نام نمایشی وارد کنید')
            return
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((HOST, PORT))
            self.username = name[:24]
            self.send({'type': 'join', 'username': self.username})
            threading.Thread(target=self.receive_loop, daemon=True).start()
        except OSError as exc:
            messagebox.showerror('خطای اتصال', f'اتصال به سرور برقرار نشد.\n{exc}\n\nابتدا server.py را اجرا کنید.')
            if self.sock:
                self.sock.close()
                self.sock = None

    def send(self, packet):
        if self.sock:
            try:
                self.sock.sendall((json.dumps(packet, ensure_ascii=False) + '\n').encode('utf-8'))
            except OSError:
                self.incoming.put({'type': 'system', 'text': 'ارتباط با سرور قطع شد'})

    def receive_loop(self):
        buffer = ''
        try:
            while True:
                data = self.sock.recv(4096)
                if not data:
                    break
                buffer += data.decode('utf-8', errors='replace')
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    if line.strip():
                        try:
                            self.incoming.put(json.loads(line))
                        except json.JSONDecodeError:
                            pass
        except OSError:
            pass
        self.incoming.put({'type': 'disconnected'})

    def build_chat(self):
        self.login_frame.destroy()
        top = tk.Frame(self.root, bg=PANEL)
        top.pack(fill='x')
        def github_button():
            webbrowser.open("https://github.com/0MORADI0")
            return
        github_btn=tk.Button(top, text='see other projects',command=github_button, bg=PANEL, fg=ACCENT, font=('Segoe UI', 17, 'bold')).pack(side='bottom', padx=16, pady=10)
        tk.Label(top, text='NOVA', bg=PANEL, fg=ACCENT, font=('Segoe UI', 17, 'bold')).pack(side='left', padx=16, pady=10)
        self.status = tk.Label(top, text='متصل به سرور', bg=PANEL, fg='#35c995', font=('Segoe UI', 10))
        self.status.pack(side='right', padx=16)
        body = tk.Frame(self.root, bg=BG)
        body.pack(fill='both', expand=True, padx=12, pady=12)
        self.chat = tk.Text(body, bg='#0e1621', fg=TEXT, insertbackground=TEXT, font=('Segoe UI', 11), wrap='word', relief='flat', state='disabled')
        self.chat.pack(side='left', fill='both', expand=True)
        side = tk.Frame(body, bg=PANEL, width=150)
        side.pack(side='right', fill='y', padx=(10, 0))
        side.pack_propagate(False)
        tk.Label(side, text='کاربران آنلاین', bg=PANEL, fg=TEXT, font=('Segoe UI', 11, 'bold')).pack(pady=10)
        self.users = tk.Listbox(side, bg=PANEL, fg=TEXT, selectbackground=ACCENT, relief='flat', highlightthickness=0)
        self.users.pack(fill='both', expand=True, padx=6, pady=6)
        bottom = tk.Frame(self.root, bg=PANEL)
        bottom.pack(fill='x', padx=12, pady=(0, 12))
        self.entry = tk.Entry(bottom, bg='#0e1621', fg=TEXT, insertbackground=TEXT, relief='flat', font=('Segoe UI', 12))
        self.entry.pack(side='left', fill='x', expand=True, ipady=10, padx=6, pady=6)
        self.entry.bind('<Return>', lambda event: self.send_message())
        tk.Button(bottom, text='ارسال', command=self.send_message, bg=ACCENT, fg='white', relief='flat', font=('Segoe UI', 10, 'bold'), padx=18).pack(side='right', padx=6)

    def add_line(self, text, color=TEXT):
        self.chat.configure(state='normal')
        self.chat.insert('end', text + '\n')
        self.chat.tag_add('last', 'end-2l', 'end-1l')
        self.chat.tag_config('last', foreground=color)
        self.chat.see('end')
        self.chat.configure(state='disabled')

    def send_message(self):
        text = self.entry.get().strip()
        if text:
            self.send({'type': 'message', 'text': text})
            self.entry.delete(0, 'end')

    def process_queue(self):
        while not self.incoming.empty():
            packet = self.incoming.get()
            kind = packet.get('type')
            if kind == 'joined':
                if hasattr(self, 'login_frame') and self.login_frame.winfo_exists():
                    self.build_chat()
                self.add_line(f'به گفتگو خوش آمدی، {self.username}', '#35c995')
            elif kind == 'message':
                self.add_line(f"{packet.get('username')}: {packet.get('text')}")
            elif kind == 'system':
                if hasattr(self, 'chat'):
                    self.add_line(packet.get('text', ''), '#9aa9ba')
            elif kind == 'users':
                if hasattr(self, 'users'):
                    self.users.delete(0, 'end')
                    for name in packet.get('users', []):
                        self.users.insert('end', name)
            elif kind == 'error':
                messagebox.showerror('خطا', packet.get('text', 'خطای نامشخص'))
            elif kind == 'disconnected':
                if hasattr(self, 'status'):
                    self.status.config(text='ارتباط قطع شد', fg='#ff6b6b')
        self.root.after(100, self.process_queue)

    def close(self):
        try:
            if self.sock:
                self.sock.shutdown(socket.SHUT_RDWR)
                self.sock.close()
        except OSError:
            pass
        self.root.destroy()

if __name__ == '__main__':
    Messenger()
