# 主要配置文件，db，redis,重要信息写在环境变量里面
import os

DB_USERNAME = os.environ.get("MYSQL_USERNAME","root")
DB_PASSWORD = os.environ.get("MYSQL_PASSWORD","shiyue")

# MYSQL 配置
DB_CONF = {
    "host" : "mysql+mysqldb://{username}:{password}@{ipaddress}:{port}/job?charset=utf8mb4".format(
        username=DB_USERNAME,
        password=DB_PASSWORD,
        ipaddress="localhost",
        port=3306
    )
}

# REDIS 配置
REDIS_CONF = {
    "host" : "localhost",
    "port" : 6379,
    "db" : 0
}
