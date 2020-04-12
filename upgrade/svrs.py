import socketserver
import json
import struct
import os
import threading
import hashlib
import logging


class UpgradeServer(socketserver.BaseRequestHandler):

    def handle(self):

        try:
            while True:

                data = self.request.recv(1024)

                if data.decode("utf-8") == "exit":
                    break

                if str(data.decode("utf-8")).lower() == "hello":
                    self.request.send('hello'.encode("utf-8"))

                data = self.request.recv(1024)
                version = str(float(data.decode("utf-8")) + 0.1)[0:3]
                info = self.get_info_by_version(version)
                if len(info) == 0:
                    info = "none".encode("utf-8")
                else:
                    info = str(info).encode("utf-8")
                self.request.send(info)

        except Exception as error:
            logging.error("Sorry, we got an error from handle - {}".format(error))
        finally:
            print('quit')
            self.request.close()

    def get_info_by_version(self, version):

        try:

            info = Utility.get_data(version)

            if len(info) > 0:
                size = os.stat("./download/{}.tar.gz".format(version)).st_size
                info.update({"size": size})
        except Exception as error:
            info = {}
            logging.error("Sorry, we got an error from get version - {}".format(error))


        return info

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

    try:

        host = "127.0.0.1"
        port = 10007
        address = (host, port)
        server = socketserver.ThreadingTCPServer(address, UpgradeServer)
        server.serve_forever()

    except KeyboardInterrupt:
        pass

