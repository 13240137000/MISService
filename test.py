import os
import sqlite3
from common.utility import GlobalVariable
from conf.admin import ConfigManager
from core.db.business import Student
from core.db.script import StudentScript
import numpy as np


# manager = ConfigManager()
#
# database_file_name = os.path.join(manager.get_path_value("db"), manager.get_database_value("name"))

# conn = sqlite3.connect(database_file_name)
# c = conn.cursor()
# c.execute('insert into class (Name) values (?)', [('Jack2')])
# conn.commit()
# conn.close()
#
# conn1 = sqlite3.connect(database_file_name)
# d = conn1.cursor()
# d.execute('SELECT * FROM Class ORDER BY Id')
# data = d.fetchall()
# print(data)

# conn = sqlite3.connect(database_file_name)
# c = conn.cursor()
# c.execute("delete from class where id >= 41")
# conn.commit()
# conn.close()


# conn = sqlite3.connect(database_file_name)
# c = conn.cursor()
# c.execute("insert into student (Name, Gender, StudentNo, ParentName, ParentMobile, Note, IsExtractFeature) values ("
#           "'Jack1', 0, '123', '1234','123123','abc',0)")
# conn.commit()
# conn.close()

# s = Student()
# result = s.get_student_by_picture(r'/Users/jack/Desktop/MISService/MISService/images/jack.jpg')
# print(result)
