import socket
import ast
import logging
import configparser
import os
import hashlib
import tarfile
import subprocess as sp
import setproctitle
import shutil


def main():

    host = "127.0.0.1"
    port = 10000
    address = (host, port)
    download_path = r"/Users/jack/Desktop/MISService/download/"
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

        # send search package and get file info
        message = str({"action": "search", "version": Utility.get_config_value("APP", "version")}).encode("utf-8")
        client.send(message)
        result = client.recv(1024)
        if result == b"NotFound":
            client.close()
            return None
        else:
            info = Utility.get_message_info(result)

        # send download command
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

        # check hash and replace prod
        hash_code = Utility.get_hash_code(file_path)

        if hash_code == file_hash_code:
            if Utility.decompress(file_path):
                source_path = os.path.dirname(file_path) + "/MISService/"
                MISHelper(source_path)
                print("Congratulations, download complete!")
            else:
                pass

    except socket.error as error:
        print("Sorry, we got an error from main - {}".format(error))
    finally:
        client.close()


class MISHelper:

    Application_Path = r"/Users/jack/Desktop/MISService/download/Code/"

    def __init__(self, source_path):

        self.stop()
        Utility.remove_folder(self.Application_Path)
        Utility.move_folder(source_path, self.Application_Path)
        self.start()

    def start(self):
        pass
        # sp.getoutput("python3 MISApplication.py")

    def stop(self):
        pass
        # process = sp.getoutput("ps aux | grep 'MISApplication' | awk '{print $2}'")
        # if len(process) > 0:
        #     for p in process:
        #         sp.getoutput("kill -9 {}".format(p))


class Utility:

    base_path = r"/Users/jack/Desktop/MISService/Source/"
    download_path = r"/Users/jack/Desktop/MISService/download/"
    config_path = r"/Users/jack/Desktop/MISService/MISService/config.ini"

    @staticmethod
    def get_config_value(section, key):
        try:
            config = configparser.ConfigParser()
            config.read(Utility.config_path)
            value = config.get(section, key)
        except Exception as error:
            value = ""
            logging.error("ConfigManager Error {}".format(error))
        return value

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
    def get_message_info(message):

        try:
            info = message.decode("utf-8")
            info = ast.literal_eval(info)
        except Exception as error:
            info = {}
            logging.error("Sorry, we got an error from get_message_info - {}".format(error))
        return info

    @staticmethod
    def decompress(file) -> bool:

        result = False

        try:
            if os.path.exists(file):
                t = tarfile.open(file)
                t.extractall(path=Utility.download_path)
                result = True
        except IOError as error:
            logging.error("Sorry, we got an error from decompress - {}".format(error))

        return result

    @staticmethod
    def remove_folder(folder) -> bool:
        result = False

        try:
            if os.path.exists(folder):
                shutil.rmtree(folder, ignore_errors=False)
                result = True
        except IOError as error:
            logging.error("Sorry, we got an error from decompress - {}".format(error))

        return result

    @staticmethod
    def move_folder(source, target) -> bool:
        result = False

        try:
            if os.path.exists(source):
                shutil.move(source, target)
                result = True
        except IOError as error:
            logging.error("Sorry, we got an error from decompress - {}".format(error))

        return result


if __name__ == '__main__':
    setproctitle.setproctitle("MISUpgradeClient")
    main()

