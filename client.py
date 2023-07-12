import datetime
import json
import os
import random
import socket
import threading
from math import log2, ceil
from typing import List
import tkinter as tk


class Client:
    def __init__(self):
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = 80
        self.host2 = None
        self.filename = f'history_{self.host}_{self.port}.json'
        self.history_dict = self.load_history()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def load_history(self):
        if not os.path.exists(self.filename):
            history_json = {'messages': []}
            with open(self.filename, 'w', encoding='utf-8') as file:
                json.dump(history_json, file)
        else:
            with open(self.filename, "r", encoding='utf-8') as file:
                history_json = json.loads(file.read())
        return history_json

    # @staticmethod
    def receive_data(self):
        while True:
            try:
                data, addr = self.socket.recvfrom(1024)
                hamming_message = data.decode('utf-8')
                # hamming_decoded_message = self.hamming_decode(hamming_message)
                hamming_decoded_message = hamming_message
                self.write_to_history(hamming_decoded_message, hamming_message)
                print(addr, hamming_decoded_message)
            except:
                pass

    def run_receiving(self, text):
        self.host2 = self.host
        self.socket.bind((self.host, self.port))

        while True:
            try:
                data, addr = self.socket.recvfrom(1024)
                hamming_message = data.decode('utf-8')
                # hamming_decoded_message = self.hamming_decode(hamming_message)
                hamming_decoded_message = hamming_message
                self.write_to_history(hamming_decoded_message, hamming_message, addr[0], text)
                print(addr, hamming_decoded_message)
            except:
                pass

        # print('here')
        # s.close()
        # os.exit(1)

    def send(self, text_message_entry, text_widget):
        # test
        self.host2 = self.host
        text_message = text_message_entry.get()
        hamming_message = text_message
        text_message_entry.delete("0", tk.END)
        # тут нужно закодировать Хэммингом

        if hamming_message:
            try:
                self.socket.sendto(hamming_message.encode('utf-8'), (self.host2, 81))
                self.write_to_history(text_message, hamming_message, self.host, text_widget)
            except TypeError:
                print('Enter IP of host2')

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

    def __hamming_common(self, src: List[List[int]], s_num: int, encode=True) -> None:
        """
        Here's the real magic =)
        """
        s_range = range(s_num)

        for i in src:
            sindrome = 0
            for s in s_range:
                sind = 0
                for p in range(2 ** s, len(i) + 1, 2 ** (s + 1)):
                    for j in range(2 ** s):
                        if (p + j) > len(i):
                            break
                        sind ^= i[p + j - 1]

                if encode:
                    i[2 ** s - 1] = sind
                else:
                    sindrome += (2 ** s * sind)

            if (not encode) and sindrome:
                i[sindrome - 1] = int(not i[sindrome - 1])

    def hamming_encode(self, msg: str, mode: int = 8) -> str:
        """
        Encoding the message with Hamming code.
        :param msg: Message string to encode
        :param mode: number of significant bits
        :return:
        """

        result = ""

        msg_b = msg.encode("utf-8")
        s_num = ceil(log2(log2(mode + 1) + mode + 1))  # number of control bits
        bit_seq = []
        for byte in msg_b:  # get bytes to binary values; every bits store to sublist
            bit_seq += list(map(int, f"{byte:08b}"))

        res_len = ceil((len(msg_b) * 8) / mode)  # length of result (bytes)
        bit_seq += [0] * (res_len * mode - len(bit_seq))  # filling zeros

        to_hamming = []

        for i in range(res_len):  # insert control bits into specified positions
            code = bit_seq[i * mode:i * mode + mode]
            for j in range(s_num):
                code.insert(2 ** j - 1, 0)
            to_hamming.append(code)

        self.__hamming_common(to_hamming, s_num, True)  # process

        for i in to_hamming:
            result += "".join(map(str, i))

        return result

    def hamming_decode(self, msg: str, mode: int = 8) -> str:
        """
        Decoding the message with Hamming code.
        :param msg: Message string to decode
        :param mode: number of significant bits
        :return:
        """

        result = ""

        s_num = ceil(log2(log2(mode + 1) + mode + 1))  # number of control bits
        res_len = len(msg) // (mode + s_num)  # length of result (bytes)
        code_len = mode + s_num  # length of one code sequence

        to_hamming = []

        for i in range(res_len):  # convert binary-like string to int-list
            code = list(map(int, msg[i * code_len:i * code_len + code_len]))
            to_hamming.append(code)

        self.__hamming_common(to_hamming, s_num, False)  # process

        for i in to_hamming:  # delete control bits
            for j in range(s_num):
                i.pop(2 ** j - 1 - j)
            result += "".join(map(str, i))

        msg_l = []

        for i in range(len(result) // 8):  # convert from binary-sring value to integer
            val = "".join(result[i * 8:i * 8 + 8])
            msg_l.append(int(val, 2))

        result = bytes(msg_l).decode("utf-8")  # finally decode to a regular string

        return result

    def make_mistake(self, byte):
        ...


if __name__ == '__main__':
    client = Client()
    client.run_client()
