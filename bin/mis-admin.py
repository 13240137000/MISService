import sys, getopt
sys.path.append('/Users/jack/Desktop/MISService/MISService')
import logging
from core.db.business import Student
from conf.admin import ConfigManager


def init_feature():
    result = ""
    try:
        s = Student()
        if s.init_feature():
            result = 'Feature initialization completed!'
        else:
            result = 'Feature initialization failed!'
    except Exception as error:
        logging.error(error)

    print(result)


def compare():
    print("starting compare face, please waiting a moment!")


if __name__ == "__main__":

    opts, args = getopt.getopt(sys.argv[1:], '-i-v-c', ['init', 'version', 'compare'])

    for opt_name, opt_value in opts:
        if opt_name in ('-i', '--init'):
            init_feature()
            sys.exit()
        elif opt_name in ('-v', '--version'):
            config = ConfigManager()
            print(config.get_app_value("version"))
            sys.exit()
        elif opt_name in ('-c', '--compare'):
            compare()
            sys.exit()
