
""" Database/Server Names """
LOCAL = "local"
PROD = "prod"
SOZIN = 'sozin'
ARCHIVEPI = "archivepi"

"""
docker run --name tiffany-mongo4 -v /mnt/SozinData/docker/TiffanyMongo:/data/db -d mongo:4.4
"""

""" -> SERVER INFO <- """
db_environment = ARCHIVEPI
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

archivepi_mongo_ip = "192.168.1.243"
archivepi_mongo_port = "27017"
archivepi_mongo_password = ""
archivepi_mongo_db_uri = BASE_MONGO_URI(archivepi_mongo_ip, archivepi_mongo_port)

def get_server_environment_uri():
    if db_environment == LOCAL:
        return local_mongo_db_uri
    elif db_environment == SOZIN:
        return sozin_mongo_db_uri
    elif db_environment == ARCHIVEPI:
        return archivepi_mongo_db_uri