

from common.db import BaseModel
import uuid
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR,INTEGER

class TagComRModel(BaseModel):
    __tablename__ = 'com_tag_r'

    id = Column(VARCHAR(50),primary_key=True)
    com_id = Column(VARCHAR(50),doc="公司id")
    tag_id = Column(VARCHAR(50),doc="标签id")

    @classmethod
    def add(cls,com_id,tag_id,id=uuid.uuid1()):
        tag_com_r = cls(id=id,com_id=com_id,tag_id=tag_id)
        cls.session.merge(tag_com_r)
        cls.session.flush()

    @classmethod
    def add_all(cls,tag_com_rs):
        cls.session.add_all(tag_com_rs)
        cls.session.flush()