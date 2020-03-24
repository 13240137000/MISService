import sys, getopt, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import logging
from core.db.business import Student
from conf.admin import ConfigManager


def init_feature() -> str:
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
    return result


def error_feature() -> list:
    result = ""
    try:
        s = Student()
        result = s.get_error_feature()
    except Exception as error:
        logging.error(error)

    print(result)
    return result


def compare(picture) -> list:
    result = []
    try:
        s = Student()
        result = s.get_student_by_picture(picture)
    except Exception as error:
        logging.error(error)

    print(result)
    return result


if __name__ == "__main__":

    opts, args = getopt.getopt(sys.argv[1:], '-v-i-e-c:', ['version', 'init', 'error', 'compare='])

    for opt_name, opt_value in opts:

        if opt_name in ('-v', '--version'):
            config = ConfigManager()
            print(config.get_app_value("version"))
            sys.exit()
        elif opt_name in ('-i', '--init'):
            init_feature()
            sys.exit()
        elif opt_name in ('-e', '--error'):
            error_feature()
            sys.exit()
        elif opt_name in ('-c', '--compare'):
            compare(opt_value)
            sys.exit()

