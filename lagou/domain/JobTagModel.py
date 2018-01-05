from common.db import BaseModel
import uuid
from sqlalchemy import Column, Integer, String, Text

class JobTagModel(BaseModel):
    __tablename__ = 'job_tag'

    id = Column(String(50), primary_key=True)
    tag_name = Column(String(20), nullable=False)
    tag_source = Column(String(20), nullable=False)

    @classmethod
    def find_by_name(cls,name):
        result = cls.session.query(cls).filter(cls.tag_name== name).one_or_none()
        if result:
            return result.id
        else:
            id = str(uuid.uuid1())
            cls.session.add(cls(id=id,tag_name=name,tag_source='拉勾'))
            return id