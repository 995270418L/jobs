
from sqlalchemy import Column, String
import uuid
from common.db import BaseModel

class ComFieldRModel(BaseModel):
    __tablename__ = 'com_field_r'

    id = Column(String(50), String(50), primary_key=True)
    com_id = Column(String(50))
    field_id = Column(String(50))

    @classmethod
    def add(cls,com_id,field_id,id=uuid.uuid1()):
        comField = cls(id=id,com_id=com_id,field_id=field_id)
        cls.session.add(comField)
        cls.session.flush()

    @classmethod
    def add_all(cls,comFields):
        cls.session.add_all(comFields)
        cls.session.flush()
