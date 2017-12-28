# 城市Model

from common.db import BaseModel
import uuid
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR,INTEGER

class CityModel(BaseModel):
    __tablename__ = 'city'

    id = Column(VARCHAR(36),primary_key=True,doc="UUID生成主键")
    city_name = Column(VARCHAR(50),nullable=False,doc='城市名')
    city_id = Column(INTEGER,nullable= False, doc="城市id")
    city_source = Column(VARCHAR(10),nullable=False,doc="平台信息来源")

    @classmethod
    def add(cls,city_id,city_name,id=uuid.uuid1(),source = "拉勾"):
        city = cls(id = id, city_id=int(city_id),city_name=city_name,city_source=source)
        cls.session.merge(city)
        cls.session.flush()

    @classmethod
    def add_all(cls,cities):
        cls.session.add_all(cities)
        cls.session.flush()