import os


class GlobalVariable:

    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_file_name = os.path.join(base_path, "config.ini")
