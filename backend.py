import datetime
import json
import os
import socket
from hamming import Hamming


class Backend:
    def __init__(self):
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = 5000
        self.host2 = None
        self.filename = f'history_{self.host}.json'
        self.history_dict = self._load_history_to_dict()
        self.receiving_socket = None

    def _load_history_to_dict(self):
        if not os.path.exists(self.filename):
            history_json = {'messages': []}
            with open(self.filename, 'w', encoding='utf-8') as file:
                json.dump(history_json, file)
        else:
            with open(self.filename, "r", encoding='utf-8') as file:
                history_json = json.loads(file.read())
        return history_json

    def run_receiving(self):
        self.receiving_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receiving_socket.bind((self.host, self.port))

        while True:
            try:
                data, addr = self.receiving_socket.recvfrom(1024)
            except OSError:
                return

            hamming_message = data.decode('utf-8')
            hamming_decoded_message = Hamming.decode(hamming_message)
            self._write_to_history(hamming_decoded_message, hamming_message, addr[0], self.host)

    def send(self, text_message, hamming_message):

        if hamming_message:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                s.sendto(hamming_message.encode('utf-8'), (self.host2, self.port))
            except TypeError:
                return 1
            except socket.gaierror:
                return 2
            self._write_to_history(text_message, hamming_message, self.host, self.host2)

    def _write_to_history(self, text_message, hamming_message, sender, receiver):
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
