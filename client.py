import random
import socket
import threading


class Client:
    def __init__(self):
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = random.randint(6000, 10000)
        self.host2 = None
        self.port2 = None

    # @staticmethod
    def receive_data(self, sock):
        while True:
            try:
                data, addr = sock.recvfrom(1024)
                print(addr, data.decode('utf-8'))
            except:
                pass

    def run_client(self):
        print('Is hosting on IP-> ' + str(self.host) + ':' + str(self.port))

        self.host2 = input('Enter host: ')
        self.port2 = int(input('Enter port: '))

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((self.host, self.port))

        threading.Thread(target=self.receive_data, args=(s,)).start()

        while True:
            data = input()
            if not data: break
            s.sendto(data.encode('utf-8'), (self.host2, self.port2))
        s.close()
        # os.exit(1)


if __name__ == '__main__':
    client = Client()
    client.run_client()
