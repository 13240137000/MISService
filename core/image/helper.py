from conf.admin import ConfigManager
from PIL import Image


class ImageHelper(object):


    __config = ConfigManager()
    __origin_path = __config.get_path_value("picture")
    __target_path = __config.get_path_value("thumbnail")
    __width = __config.get_picture_value("weight")
    __height = __config.get_picture_value("height")

    def __get_image_extension_name(self):
        pass

    def resize(self, name):
        pass
