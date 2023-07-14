import sys
import threading

from backend import Backend
import tkinter as tk
from hamming import Hamming


class GUI:
    def __init__(self):
        self.backend = Backend()
        root = tk.Tk()

        my_ip_address_label = tk.Label(root, text='My host: ' + self.backend.host, width=30).grid(row=0, column=0,
                                                                                                  columnspan=2)
        ip_address_label = tk.Label(root, text='Enter IP address', width=16).grid(row=1, column=0)
        self.ip_address = tk.Entry(root, width=30)
        self.ip_address.grid(row=1, column=1, columnspan=2)

        txt = tk.Text(root, width=60)
        txt.grid(row=2, column=0, columnspan=2)

        self.receiving_thread = threading.Thread(target=self.backend.run_receiving, args=(txt,))

        ip_connect = tk.Button(root, text='Connect', command=self._connect).grid(row=1, column=2)

        # threading.Thread(target=self.load_history, args=(txt,)).start()
        self._load_history(txt)

        text_message_label = tk.Label(root, text='Сообщение', width=10).grid(row=3, column=0)
        hamming_message_label = tk.Label(root, text='Код Хэмминга', width=15).grid(row=4, column=0)
        mistake_label = tk.Label(root, text='Ошибка', width=10)
        mistake_label.grid(row=5, column=0)
        self.text_message = tk.Entry(root, width=40)
        self.text_message.grid(row=3, column=1)
        self.hamming_message = tk.Label(root, width=40, justify=tk.LEFT)
        self.hamming_message.grid(row=4, column=1)
        self.text_message.bind('<KeyRelease>', self._encode_hamming)
        self.mistake = tk.Entry(root, width=10, justify=tk.LEFT, text='0')
        self.mistake.grid(row=5, column=1)
        self.mistake.insert(0, '0')
        self.mistake.bind('<KeyRelease>', self._encode_hamming)
        # text_message

        send = tk.Button(root, text="Send", command=lambda: self.backend.send(self.text_message, txt,
                                                                              self.hamming_message, self.mistake))
        send.grid(row=3, column=2, rowspan=2)

        # root.protocol("WM_DELETE_WINDOW", self.on_closing)
        root.mainloop()

    def _connect(self):
        self.backend.host2 = self.ip_address.get()
        self.backend.is_running = True
        self.receiving_thread.start()

    def _load_history(self, text_widget):
        for message in self.backend.history_dict['messages']:
            message = f'{message["sender"]}: {message["text"]}\n\n'
            text_widget.insert(tk.END, message)

    def on_closing(self):
        print('Closing...')
        sys.exit()

    def _encode_hamming(self, event):
        text = self.text_message.get()
        mistake = self.mistake.get()
        hamming_message = Hamming.encode(text, mistake)
        self.hamming_message.config(text=hamming_message)
