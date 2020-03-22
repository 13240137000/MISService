import os


class GlobalVariable:

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_file_name = os.path.join(base_dir, "config.ini")
