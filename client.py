import datetime
import json
import os
import socket
from math import log2, ceil
from typing import List
import tkinter as tk
from tkinter import messagebox as mb
from hamming import Hamming


class Client:
    def __init__(self):
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = 80
        self.host2 = None
        self.filename = f'history_{self.host}_{self.port}.json'
        self.history_dict = self.load_history()
        self.is_running = False
        # self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def load_history(self):
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
                self.write_to_history(hamming_decoded_message, hamming_message, addr[0], text)
                print(addr, hamming_decoded_message)
            except:
                print('Exception')
                pass

    def send(self, text_message_entry, text_widget):
        # test
        text_message = text_message_entry.get()
        hamming_message = Hamming.encode(text_message)
        text_message_entry.delete("0", tk.END)

        if hamming_message:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                # s.sendto(hamming_message.encode('utf-8'), (self.host2, self.port))
                s.sendto(hamming_message.encode('utf-8'), (self.host2, 88))
                self.write_to_history(text_message, hamming_message, self.host, text_widget)
            except TypeError:
                mb.showinfo('Заголовок', 'Введите хост!')

    def write_to_history(self, text_message, hamming_message, address, txt_widget):
        data = {
            'time': str(datetime.datetime.now()),
            'sender': self.host,
            'receiver': ':'.join((self.host2, str(self.port))),
            'text': text_message,
            'hamming_code': hamming_message,
        }
        self.history_dict['messages'].append(data)
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(self.history_dict, file)
            file.write('\n')
        message = f'{address}: {text_message}\n\n'
        txt_widget.insert(tk.END, message)

    def str_to_binary(self, string):
        binary_list = []
        for char in string:
            binary_list.append(bin(ord(char))[2:].zfill(8))
        return ''.join(binary_list)



# if __name__ == '__main__':
#     client = Client()
#     client.run_client()
