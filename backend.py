import datetime
import json
import os
import socket
import tkinter as tk
from tkinter import messagebox as mb
from hamming import Hamming


class Backend:
    def __init__(self):
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = 80
        self.host2 = None
        self.filename = f'history_{self.host}_{self.port}.json'
        self.history_dict = self._load_history_to_dict()

    def _load_history_to_dict(self):
        if not os.path.exists(self.filename):
            history_json = {'messages': []}
            with open(self.filename, 'w', encoding='utf-8') as file:
                json.dump(history_json, file)
        else:
            with open(self.filename, "r", encoding='utf-8') as file:
                history_json = json.loads(file.read())
        return history_json

    def run_receiving(self, text):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((self.host, self.port))
        print('Binded')

        while True:
            print('In while')
            try:
                print('Waiting for receive...')
                data, addr = s.recvfrom(1024)
                print('Got!')
                hamming_message = data.decode('utf-8')
                # hamming_decoded_message = self.hamming_decode(hamming_message)
                hamming_decoded_message = Hamming.decode(hamming_message)
                self._write_to_history(hamming_decoded_message, hamming_message, addr[0], self.host, text)
                print(addr, hamming_decoded_message)
            except:
                print('Exception')
                pass

    def send(self, text_message_entry, text_widget, hamming_widget, mistake_widget):
        text_message = text_message_entry.get()
        hamming_message = hamming_widget['text']
        if not text_message:
            return

        text_message_entry.delete("0", tk.END)
        mistake_widget.insert(0, '0')
        # hamming_widget.delete("0", tk.END)
        # mistake_widget.delete("0", tk.END)

        if hamming_message:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.sendto(hamming_message.encode('utf-8'), (self.host2, self.port))
                self._write_to_history(text_message, hamming_message, self.host, self.host2, text_widget)
            except TypeError:
                mb.showinfo('Заголовок', 'Введите хост!')

    def _write_to_history(self, text_message, hamming_message, sender, receiver, txt_widget):
        data = {
            'time': str(datetime.datetime.now()),
            'sender': sender,
            'receiver': receiver,
            'text': text_message,
            'hamming_code': hamming_message,
        }
        self.history_dict['messages'].append(data)
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(self.history_dict, file)
            file.write('\n')
        message = f'{sender}: {text_message}\n\n'
        txt_widget.insert(tk.END, message)
