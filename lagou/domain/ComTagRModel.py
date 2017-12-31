from sqlalchemy import Column, String
from common.db import BaseModel

class ComTagRModel(BaseModel):
    __tablename__ = 'com_tag_r'

    id = Column(String(50), primary_key=True)
    com_id = Column(String(50))
    tag_id = Column(String(50))

    @classmethod
    def add_all(cls,com_tags):
        cls.session.add_all(com_tags)
        cls.session.flush()