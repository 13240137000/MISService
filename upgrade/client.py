import socket


class UpgradeClient:

    __host = "127.0.0.1"
    __port = 10000
    __address = (__host, __port)

    def __init__(self):
        self.client = socket.socket()
        self.client.connect(self.__address)

    def start(self):

        try:

            data = '{"version":"v1.0.0"}'.encode(encoding="utf-8")
            self.client.sendall(data)
            print(self.client.recv(2).decode(encoding="utf-8"))

        except socket.error as error:
            print("Sorry, we got an error - {}".format(error))

    def close(self):
        self.client.close()


if __name__ == '__main__':

    client = UpgradeClient()
    client.start()
    # client.close()
