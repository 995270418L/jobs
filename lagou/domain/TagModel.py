
from common.db import BaseModel
import uuid
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR,INTEGER


class TagModel(BaseModel):
    __tablename__ = 'tag'

    id = Column(VARCHAR(50),primary_key=True)
    tag_name = Column(VARCHAR(20),doc="标签名")

    @classmethod
    def add(cls,tag_name,id=uuid.uuid1()):
        tag = cls(id=id,tag_name=tag_name)
        cls.session.merge(tag)
        cls.session.flush()

    @classmethod
    def add_all(cls,tags):
        cls.session.add_all(tags)
        cls.session.flush()