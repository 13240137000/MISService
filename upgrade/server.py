import os
import socket
import hashlib
import json


class UpgradeServer:

    __base_directory = os.path.dirname(os.path.abspath(__file__))
    __download_directory = os.path.join(__base_directory, 'download')
    __host = "127.0.0.1"
    __port = 10000
    __address = (__host, __port)

    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def bind(self):
        self.server.bind(self.__address)
        self.server.listen()

    def start(self):

        try:

            self.bind()
            print("The upgrade server has been started.")
            while True:
                client, address = self.server.accept()
                print("{} has been connection to client".format(address))
                res = client.recv(2)
                print(res.decode(encoding="utf-8"))
                client.sendall('{"status":"success"}'.encode(encoding="utf-8"))

        except Exception as error:
            print("Sorry, we got an error - {}".format(error))

    def download(self):
        pass

    def close(self):
        pass


class Utility:

    def __init__(self):
        pass

    @staticmethod
    def get_hash_code(file):

        try:
            if os.path.exists(file):
                with open(file, "rb") as f:
                    instance = hashlib.sha256()
                    instance.update(f.read())
                    return instance.hexdigest()

        except Exception as error:
            print("Sorry, we got an error {}".format(error))

    @staticmethod
    def load_data():
        file = r'db.json'
        result = []
        try:
            if os.path.exists(file):
                with open(file, "r") as f:
                    result = json.load(f)
        except Exception as error:
            print("Sorry, we got an error {}".format(error))
        return result

    @staticmethod
    def get_data(value):
        result = {}
        try:
            versions = Utility.load_data()
            for version in versions:
                if version.get("version") == value.lower():
                    result = version
                    break
        except Exception as error:
            print("Sorry, we got an error {}".format(error))
        return result


if __name__ == '__main__':

    server = UpgradeServer()
    server.start()

