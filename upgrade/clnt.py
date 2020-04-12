import socket
import json
from conf.admin import ConfigManager


def main():

    version = ConfigManager().get_app_value("version")
    host = "127.0.0.1"
    port = 10007
    address = (host, port)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:

        client.connect(address)

        # send hello package
        data = "hello".encode("utf-8")
        client.send(data)
        result = client.recv(1024)
        if result != b"hello":
            client.close()
            return None

        # send version package
        data = version.encode("utf-8")
        client.send(data)
        result = client.recv(1024)
        if result == b"none":
            client.close()
            return None
        else:
            print(result)

    except socket.error as error:
        print("Sorry, we got an error from main - {}".format(error))
    finally:
        client.close()


if __name__ == '__main__':
    main()
