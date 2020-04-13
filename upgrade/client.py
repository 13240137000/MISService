import socket
import ast
import logging
from conf.admin import ConfigManager
import os


def main():

    host = "127.0.0.1"
    port = 10003
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
            info = get_message_info(result)
            print(info)

        # request download latest file.
        message = str({"action": "download", "name": info.get("version") + ".tar.gz"}).encode("utf-8")
        client.send(message)

        file_name = "{}.{}".format(info.get("version"), "tar.gz")
        file_size = int(info.get("size"))
        file_path = os.path.join(download_path, file_name)

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

        client.close()

    except socket.error as error:
        print("Sorry, we got an error from main - {}".format(error))
    finally:
        client.close()


def get_message_info(message):

    try:
        info = message.decode("utf-8")
        info = ast.literal_eval(info)
    except Exception as error:
        info = {}
        logging.error("Sorry, we got an error from get_message_info - {}".format(error))
    return info


if __name__ == '__main__':
    main()
