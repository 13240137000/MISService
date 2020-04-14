import socketserver
import json
import ast
import os
import hashlib
import logging
from decimal import Decimal
import setproctitle


class UpgradeServer(socketserver.BaseRequestHandler):

    def handle(self):

        base_path = r"/Users/jack/Desktop/MISService/Source/"

        try:
            while True:

                message = self.request.recv(1024)
                if message == b'':
                    continue

                message = Utility.get_message_info(message)

                if len(message) == 0:
                    action = "exit"
                else:
                    action = message.get("action")

                if action == "exit":
                    break

                if action == "hello":
                    self.request.send('hello'.encode("utf-8"))
                    continue

                if action == "search":
                    version = message.get("version")
                    version = str(Decimal(version) + Decimal('0.1'))
                    info = Utility.get_version_info(version)
                    if len(info) == 0:
                        info = "NotFound".encode("utf-8")
                    else:
                        info = str(info).encode("utf-8")
                    self.request.send(info)
                    continue

                if action == "download":
                    file_info = ast.literal_eval(info.decode("utf-8"))
                    file_name = "{}.{}".format(file_info.get("version"), "tar.gz")
                    file_size = int(file_info.get("size"))
                    file_path = os.path.join(base_path, file_name)
                    try:
                        with open(file_path, "rb") as f:
                            if 0 < file_size <= 1024:
                                self.request.send(f.read())
                            else:
                                total_size = file_size
                                while True:
                                    if total_size > 1024:
                                        self.request.send(f.read(1024))
                                        total_size = total_size - 1024
                                    else:
                                        self.request.send(f.read(file_size - total_size))
                                        break

                    except IOError as error:
                        pass

        except Exception as error:
            logging.error("Sorry, we got an error from handle - {}".format(error))
        finally:
            self.request.close()


class Utility:

    base_path = r"/Users/jack/Desktop/MISService/Source/"

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

    @staticmethod
    def get_message_info(message):

        try:
            info = message.decode("utf-8")
            info = ast.literal_eval(info)
        except Exception as error:
            info = {}
            logging.error("Sorry, we got an error from get_message_info - {}".format(error))
        return info

    @staticmethod
    def get_version_info(version):

        try:

            info = Utility.get_data(version)

            if len(info) > 0:
                name = Utility.base_path + "{}.tar.gz".format(version)
                size = os.path.getsize(name)
                info.update({"size": size})
        except Exception as error:
            info = {}
            logging.error("Sorry, we got an error from get_version_info - {}".format(error))

        return info


if __name__ == '__main__':

    setproctitle.setproctitle("MISUpgradeServer")

    try:

        host = "127.0.0.1"
        port = 10000
        address = (host, port)
        server = socketserver.ThreadingTCPServer(address, UpgradeServer)
        server.serve_forever()

    except KeyboardInterrupt:
        pass

