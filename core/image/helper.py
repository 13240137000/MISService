from conf.admin import ConfigManager
from PIL import Image
import os
import logging


class ImageHelper(object):

    __config = ConfigManager()
    __origin_path = __config.get_path_value("picture")
    __target_path = __config.get_path_value("thumbnail")
    __width = __config.get_picture_value("weight")
    __height = __config.get_picture_value("height")

    def resize(self, name) -> bool:

        result = True

        try:

            image = os.path.join(self.__origin_path, name)
            target_image = os.path.join(self.__target_path, name)
            instance = Image.open(image)
            thumbnail_image = instance.resize((int(self.__width), int(self.__height)), resample=Image.LANCZOS)
            thumbnail_image.save(target_image)

        except Exception as error:
            result = False
            logging.error("resize picture {}".format(error))

        return result
