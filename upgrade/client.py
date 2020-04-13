import socket
import ast
import logging
from conf.admin import ConfigManager
import os
import hashlib
import json


def main():

    host = "127.0.0.1"
    port = 10000
    address = (host, port)
    download_path = r"./download/"
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:

        client.connect(address)

        # send hello package
        message = '{"action":"hello"}'.encode("utf-8")
        client.send(message)
        result = client.recv(1024)
        if result != b"hello":
            client.close()
            return None

        # send search version to server
        message = str({"action": "search", "version": ConfigManager().get_app_value("version")}).encode("utf-8")
        client.send(message)
        result = client.recv(1024)
        if result == b"NotFound":
            client.close()
            return None
        else:
            info = Utility.get_message_info(result)

        # request download latest file.
        message = str({"action": "download", "name": info.get("version") + ".tar.gz"}).encode("utf-8")
        client.send(message)

        file_name = "{}.{}".format(info.get("version"), "tar.gz")
        file_size = int(info.get("size"))
        file_path = os.path.join(download_path, file_name)
        file_hash_code = info.get("hash")

        if os.path.exists(file_path):
            os.remove(file_path)

        with open(file_path, "wb") as f:
            if 0 < file_size <= 1024:
                f.write(client.recv(1024))
            else:
                total_size = file_size
                while True:
                    if total_size > 1024:
                        f.write(client.recv(1024))
                        total_size = total_size - 1024
                    else:
                        f.write(client.recv(file_size - total_size))
                        break

        hash_code = Utility.get_hash_code(file_path)

        if hash_code == file_hash_code:
            print("Congratulations, download complete!")

    except socket.error as error:
        print("Sorry, we got an error from main - {}".format(error))
    finally:
        client.close()


class MISHelper:

    def __init__(self):
        pass

    def remove(self):
        pass

    def start(self):
        pass

    def stop(self):
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
                # size = os.stat("./source/{}.tar.gz".format(version)).st_size
                size = os.path.getsize("./source/{}.tar.gz".format(version))
                info.update({"size": size})
        except Exception as error:
            info = {}
            logging.error("Sorry, we got an error from get_version_info - {}".format(error))

        return info


if __name__ == '__main__':
    main()
