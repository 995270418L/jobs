from sqlalchemy import Column, String
from common.db import BaseModel
import uuid

class ComTagModel(BaseModel):
    __tablename__ = 'com_tag'

    id = Column(String(50), primary_key=True)
    tag_name = Column(String(20))
    tag_source = Column(String(20), nullable=False)

    @classmethod
    def find_by_name(cls,name):
        comTagModel = cls.session.query(cls).filter(cls.tag_name==name).one_or_none()
        if comTagModel:
            return comTagModel.id
        else:
            id = str(uuid.uuid1())
            cls.session.add(ComTagModel(id=id,tag_name=name,tag_source='拉勾'))
            return  id


