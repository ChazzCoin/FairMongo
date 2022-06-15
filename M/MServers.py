import os
from pathlib import Path

# -> MASTER PATH <- #
MASTER_PATH = os.getcwd()

def get_parent_directory():
    path = Path(os.getcwd())
    return path.parent.absolute().__str__()

""" Database/Server Names """
LOCAL = "local"
PROD = "prod"
SOZIN = 'sozin'
SOZINREMOTE = 'sozinremote'
HARK = "hark"
ARCHIVEPI = "archivepi"

ERROR = 0  # -> Show ERROR only
INFO = 1  # -> Show ERROR and INFO
DEBUG = 2  # -> Show ERROR, INFO and DEBUG
VERBOSE = 3  # -> Show ERROR, INFO, DEBUG AND VERBOSE
LOG_LEVEL = DEBUG

"""
SOZIN:
-> docker run --name tiffany-mongo4 -v /mnt/SozinData/docker/TiffanyMongo:/data/db -d mongo:4.4

HARK:
-> docker run --name hark-mongodb -p 27017:27017 -v /home/hark/bin/docker/mongodb:/data/db -d mongo:4.4
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
db_environment_name = SOZIN
db_name = "research"

BASE_MONGO_URI = lambda mongo_ip, mongo_port: f"mongodb://{mongo_ip}:{mongo_port}"

local_mongo_ip = "localhost"
local_mongo_port = "27017"
local_mongo_db_uri = BASE_MONGO_URI(local_mongo_ip, local_mongo_port)

# prod_mongo_ip = env.get_env("PROD_MONGO_IP")
# prod_mongo_port = env.get_env("PROD_MONGO_PORT")
# prod_mongo_password = env.get_env("PROD_MONGO_PASSWORD")
# prod_mongo_db_uri = BASE_MONGO_URI(prod_mongo_ip, prod_mongo_port)
#
sozin_mongo_ip = "192.168.1.180"
sozin_mongo_port = "27017"
sozin_mongo_password = ""
sozin_mongo_db_uri = BASE_MONGO_URI(sozin_mongo_ip, sozin_mongo_port)

sozin_remote_mongo_ip = "aokiromeo.duckdns.org"
sozin_remote_mongo_port = "1214"
sozin_remote_mongo_password = ""
sozin_remote_mongo_db_uri = BASE_MONGO_URI(sozin_remote_mongo_ip, sozin_remote_mongo_port)

archivepi_mongo_ip = "192.168.1.243"
archivepi_mongo_port = "27017"
archivepi_mongo_password = ""
archivepi_mongo_db_uri = BASE_MONGO_URI(archivepi_mongo_ip, archivepi_mongo_port)

hark_mongo_ip = "192.168.1.166"
hark_mongo_port = "27017"
hark_mongo_password = ""
hark_mongo_db_uri = BASE_MONGO_URI(hark_mongo_ip, hark_mongo_port)

def get_server_environment_uri_for_host_name(hostName):
    if hostName == LOCAL:
        return local_mongo_db_uri
    elif hostName == SOZIN:
        return sozin_mongo_db_uri
    elif hostName == ARCHIVEPI:
        return archivepi_mongo_db_uri
    elif hostName == HARK:
        return hark_mongo_db_uri
    return False

def get_server_environment_uri():
    if db_environment_name == LOCAL:
        return local_mongo_db_uri
    elif db_environment_name == SOZIN:
        return sozin_mongo_db_uri
    elif db_environment_name == SOZINREMOTE:
        return sozin_remote_mongo_db_uri
    elif db_environment_name == ARCHIVEPI:
        return archivepi_mongo_db_uri
    elif db_environment_name == HARK:
        return hark_mongo_db_uri
