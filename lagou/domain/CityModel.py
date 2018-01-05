# 城市Model

import uuid

from sqlalchemy import Column, String

from common.db import BaseModel


class CityModel(BaseModel):

    __tablename__ = 'city'

    id = Column(String(50), primary_key=True)
    city_name = Column(String(30), nullable=False)
    city_id = Column(String(50))
    city_source = Column(String(50))

    @classmethod
    def add(cls,city_id,city_name,id=uuid.uuid1(),source = "拉勾"):
        city = cls(id = id, city_id=int(city_id),city_name=city_name,city_source=source)
        cls.session.merge(city)
        cls.session.flush()

    @classmethod
    def add_all(cls,cities):
        cls.session.add_all(cities)
        cls.session.flush()

    @classmethod
    def get_city_id_by_name(cls,name):
        if name:
            result = cls.session.query(cls).filter(cls.city_name==name,cls.city_source=='拉勾').one_or_none()
            if result:
                return result.city_id
        else:
            return None

    @classmethod
    def gat_all(cls):
        return cls.session.query(cls).all()