from conf.admin import ConfigManager

manager = ConfigManager()

name = manager.get_author_value("name")

print(name)
