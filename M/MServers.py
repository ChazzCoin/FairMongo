import os
from pathlib import Path
import FENV

# -> MASTER PATH <- #
MASTER_PATH = os.getcwd()

def get_parent_directory():
    path = Path(os.getcwd())
    return path.parent.absolute().__str__()

"""
SOZIN:
-> docker run --name mongo4 -v /Mongo:/data/db -d mongo:4.4

HARK:
-> docker run --name mongodb -p 27017:27017 -v /home/hark/bin/docker/mongodb:/data/db -d mongo:4.4
"""

"""
BACKUP: ( -o path/for/export )
-> sudo mongodump --forceTableScan --db research --collection articles -o /home/sozin/bin
SEND TO HARK:
-> scp -r research/ hark@192.168.1.166:/home/hark/bin/docker

RESTORE:
-> mongorestore --db research --collection articles articles.bson
"""

""" -> SERVER INFO <- """
db_environment_name = FENV.get_os_variable("ARTICLE_DATABASE_NAME", default="research")
db_name = db_environment_name
db_host = FENV.get_os_variable("ARTICLE_DATABASE_HOST", default='localhost')
db_port = FENV.get_os_variable("ARTICLE_DATABASE_PORT", default=27017)
db_user = FENV.get_os_variable("ARTICLE_DATABASE_USER", default=False)
db_password = FENV.get_os_variable("ARTICLE_DATABASE_PASSWORD", default=False)

BASE_MONGO_URI = lambda mongo_ip, mongo_port: f"mongodb://{mongo_ip}:{mongo_port}"
BASE_MONGO_AUTH_URI = lambda mongo_ip, mongo_port, user, pw: f"mongodb://{user}:{pw}@{mongo_ip}:{mongo_port}"

if not db_user or db_user == "":
    MONGO_DATABASE_URI = BASE_MONGO_URI(db_host, db_port)
else:
    MONGO_DATABASE_URI = BASE_MONGO_AUTH_URI(db_host, db_port, db_user, db_password)
