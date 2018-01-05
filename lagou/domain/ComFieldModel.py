import uuid

from sqlalchemy import Column, String
from common.db import BaseModel

# 公司行业标签
class ComFieldModel(BaseModel):
    __tablename__ = 'com_field'

    id = Column(String(50), primary_key=True)
    field_name = Column(String(50), nullable=False)
    field_source = Column(String(20), nullable=False)

    @classmethod
    def find_by_name(cls,name):
        result = cls.session.query(cls).filter(cls.field_name ==name).one_or_none()
        if result:
            return result.id
        else:
            id = str(uuid.uuid1())
            cls.session.add(cls(id=id,field_name=name,field_source='拉勾'))
            return id
