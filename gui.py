import threading
from backend import Backend
import tkinter as tk
from hamming import Hamming
from tkinter import messagebox as mb


class GUI:
    def __init__(self):
        self.backend = Backend()
        self.root = tk.Tk()

        my_ip_address_label = tk.Label(self.root, text='My host: ' + self.backend.host, width=30).grid(row=0, column=0,
                                                                                                       columnspan=2)
        ip_address_label = tk.Label(self.root, text='Enter the paired host:', width=20).grid(row=1, column=0)
        self.ip_address = tk.Entry(self.root, width=30)
        self.ip_address.grid(row=1, column=1, columnspan=2)
        self.ip_address.bind('<KeyRelease>', self._enter_host2)

        self.txt = tk.Text(self.root, width=70)
        self.txt.grid(row=2, column=0, columnspan=3)

        self.receiving_thread = threading.Thread(target=self.backend.run_receiving)
        self.receiving_thread.start()

        self._load_history()

        text_message_label = tk.Label(self.root, text='Message', width=10).grid(row=3, column=0)
        hamming_message_label = tk.Label(self.root, text='Hamming code', width=15).grid(row=4, column=0)
        mistake_label = tk.Label(self.root, text='Mistake', width=10)
        mistake_label.grid(row=5, column=0)
        self.text_message = tk.Entry(self.root, width=55)
        self.text_message.grid(row=3, column=1)
        self.hamming_message = tk.Label(self.root, width=60, justify=tk.LEFT)
        self.hamming_message.grid(row=4, column=1)
        self.text_message.bind('<KeyRelease>', self._encode_hamming)
        self.mistake = tk.Entry(self.root, width=10, justify=tk.LEFT, text='0')
        self.mistake.grid(row=5, column=1)
        self.mistake.insert(0, '0')
        self.mistake.bind('<KeyRelease>', self._encode_hamming)

        send = tk.Button(self.root, text="Send", command=lambda: self._send(), padx=20, pady=10)
        send.grid(row=3, column=2, rowspan=2)

        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.root.mainloop()

    def _enter_host2(self, event):
        self.backend.host2 = self.ip_address.get()

    def _insert_message(self, message):
        message = f'''
[{message['time'][:-7]}] {message["sender"]}: 
    message: {message['text']}
    hamming_code: {message['hamming_code']}
 {'-' * 68} '''
        self.txt.insert(tk.END, message)

    def _send(self):
        text_message = self.text_message.get()
        if not text_message:
            return
        hamming_message = self.hamming_message['text']
        ret = self.backend.send(text_message, hamming_message)
        if ret == 1:
            mb.showinfo('', 'Введите хост!')
            return
        elif ret == 2:
            mb.showinfo('', 'Неверный хост!')
            return
        self._clear_message_data()
        self._insert_message(self.backend.history_dict['messages'][-1])

    def _clear_message_data(self):
        self.text_message.delete("0", tk.END)
        self.hamming_message.config(text="")
        self.mistake.delete("0", tk.END)
        self.mistake.insert(0, '0')

    def _load_history(self):
        for message in self.backend.history_dict['messages']:
            self._insert_message(message)

    def _on_closing(self):
        if self.backend.receiving_socket:
            self.backend.receiving_socket.close()
        self.root.destroy()

    def _encode_hamming(self, event):
        text = self.text_message.get().strip()
        mistake = self.mistake.get().strip()
        if not text:
            return
        mistake = '0' if mistake == '' else mistake
        hamming_message = Hamming.encode(text, mistake)
        self.hamming_message.config(text=hamming_message)
