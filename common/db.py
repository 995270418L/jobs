
from common import config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import redis

# 创建连接池
engine = create_engine(config.DB_CONF['host'], pool_recycle=3600)
# orm映射对象的基类
_BaseModel = declarative_base()
# 操作数据库表的对象session
_Session = sessionmaker(bind=engine, autoflush=True, autocommit=True)

class BaseModel(_BaseModel):
    __abstract__ = True
    # __metadata__ = MetaData(bind=engine)
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'extend_existing': True,
    }
    session = _Session()

redis_pool = redis.ConnectionPool(host=config.REDIS_CONF['host'],port=config.REDIS_CONF['port'])
redis_instance = redis.Redis(connection_pool=redis_pool)


