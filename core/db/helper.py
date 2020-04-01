import os
import sqlite3
from conf.admin import ConfigManager
import logging


class SqliteHelper(object):
    """
    this class for help user access sqlite database.
    """
    _config = ConfigManager()
    _database_file_name = os.path.join(_config.get_path_value("db"), _config.get_database_value("name"))
    _database_path = _config.get_path_value("db")
    _connection = None

    def __init__(self, db_name=None):

        if db_name is None:
            self._connection = sqlite3.connect(self._database_file_name, timeout=3, isolation_level=None,
                                               check_same_thread=False)
        else:
            db_name = os.path.join(self._database_path, db_name)
            self._connection = sqlite3.connect(db_name, timeout=3, isolation_level=None,
                                               check_same_thread=False)

    def __dict_factory(self, cursor, row):

        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def execute(self, sql, args=[], result_dict=True, commit=True) -> list:

        try:

            if result_dict:
                self._connection.row_factory = self.__dict_factory
            else:
                self._connection.row_factory = None

            _cursor = self._connection.cursor()
            _cursor.execute(sql, args)

            if commit:
                self._connection.commit()

            data = _cursor.fetchall()

            _cursor.close()

        except Exception as error:

            logging.error(error)

        return data
