import threading

from client import Client
import tkinter as tk


class GUI:
    def __init__(self):
        self.client = Client()
        root = tk.Tk()

        my_ip_address_label = tk.Label(root, text='My host: ' + self.client.host, width=30).grid(row=0, column=0, columnspan=2)
        ip_address_label = tk.Label(root, text='Enter IP address', width=16).grid(row=1, column=0)
        self.ip_address = tk.Entry(root, width=30)
        self.ip_address.grid(row=1, column=1, columnspan=2)
        # self.ip_address.bind('<Return>', self.connect)

        txt = tk.Text(root, width=60)
        txt.grid(row=2, column=0, columnspan=2)

        scrollbar = tk.Scrollbar(txt)
        scrollbar.place(relheight=1, relx=0.974)

        # threading.Thread(target=self.load_history, args=(txt,)).start()
        self.load_history(txt)
        threading.Thread(target=self.client.run_receiving, args=(txt,)).start()

        text_message_label = tk.Label(root, text='Сообщение', width=10).grid(row=3, column=0)
        hamming_message_label = tk.Label(root, text='Код Хэмминга', width=15).grid(row=4, column=0)
        mistake_label = tk.Label(root, text='Ошибка', width=10)
        mistake_label.grid(row=5, column=0)
        self.text_message = tk.Entry(root, width=40)
        self.text_message.grid(row=3, column=1)
        self.hamming_message = tk.Label(root, width=40, justify=tk.LEFT)
        self.hamming_message.grid(row=4, column=1)
        self.text_message.bind('<KeyRelease>', self.encode_hamming)
        mistake = tk.Entry(root, width=10, justify=tk.LEFT).grid(row=5, column=1)
        make_mistake = tk.Button(root, text="Применить").grid(row=5, column=2, rowspan=2)
        # text_message

        send = tk.Button(root, text="Send", command=lambda: self.client.send(self.text_message, txt))
        send.grid(row=4, column=2, rowspan=2)

        root.mainloop()

    def load_history(self, text_widget):
        for message in self.client.history_dict['messages']:
            message = f'{message["sender"]}: {message["text"]}\n\n'
            text_widget.insert(tk.END, message)

    def encode_hamming(self, event):
        text = self.text_message.get()
        # hamming_message = self.client.hamming_encode(text)
        hamming_message = text
        self.hamming_message.config(text=hamming_message)

    # def connect(self, event):
    #     host = self.ip_address.get()
    #     self.client.run_client(host)

    # def start(self):
    #     self.root.mainloop()
