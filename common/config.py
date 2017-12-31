# 主要配置文件，db，redis,重要信息写在环境变量里面
import os

DB_USERNAME = os.environ.get("MYSQL_USERNAME","root")
DB_PASSWORD = os.environ.get("MYSQL_PASSWORD","shiyue")
SMTP_HOST = 'smtp.163.com'
SMTP_PORT = '25'

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

# 日志配置
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'default': {
            'format': '%(asctime)s- %(module)s:%(lineno)d [%(levelname)1.1s] %(name)s: %(message)s',
            'datefmt': '%Y/%m/%d %H:%M:%S'
        },
    },

    'filters':{

    },

    # 处理器
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'formatter': 'default',
            'class': 'logging.StreamHandler',
            "stream": "ext://sys.stdout"
        },
        'file': {
            'level': 'INFO',
            'formatter': 'default',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'lagou_spider_log.log',
            'encoding': 'utf8'
        },
        'smtp': {
            'level': 'ERROR',
            'class': 'logging.handlers.SMTPHandler',
            'formatter': 'default',
            'mailhost': (SMTP_HOST, SMTP_PORT),
            'fromaddr': 'XYPFDWY@163.com',
            'toaddrs': ['995270418@qq.com'],
            'subject': '拉勾的爬虫系统出现异常',
            'credentials': ('XYPFDWY', 'steve123')
        },
        'memoryHandler':{
            'capacity': 5,
            'target':'smtp',
            'class':'common.OptmizedMemoryHandler.OptmizedMemoryHandler'
        }
    },
    "loggers": {
        'lagou.tasks':{
            "level": "INFO",
            "handlers": ['file'],
            "propagate":'no'
        },
        'lagou.utils':{
            "level": "INFO",
            "handlers": ['file'],
            "propagate":'no'
        },
        '' : {
            "level": 'ERROR',
            'handlers': ['smtp','memoryHandler'],
            "propagate": 'no'
        }
    },
}
