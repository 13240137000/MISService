import sys
import os
import getopt
import hashlib


class Utility:

    def get_hash_code(self, file) -> str:

        try:
            if os.path.exists(file):
                with open(file, "rb") as f:
                    instance = hashlib.sha256()
                    instance.update(f.read())
                    return instance.hexdigest()

        except Exception as error:
            print("Sorry, we got an error {}".format(error))


if __name__ == "__main__":

    opts, args = getopt.getopt(sys.argv[1:], '-f:', ['file='])
    utility = Utility()

    for name, value in opts:

        if name in ('-f', '--file'):
            print(utility.get_hash_code(value))
            sys.exit()
