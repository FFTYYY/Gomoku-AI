import configparser

a = configparser.ConfigParser()


a.read("config.ini")


print (a.sections())
print (a.options("init_val"))
print (a.items("init_val"))
print (a.get("init_val","玩家0"))
print (a.get("init_val","玩家1"))