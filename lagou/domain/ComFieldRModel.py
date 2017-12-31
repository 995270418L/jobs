
import uuid

from sqlalchemy import Column, String

from common.db import BaseModel


class ComFieldRModel(BaseModel):
    __tablename__ = 'com_field_r'

    id = Column(String(50), primary_key=True)
    com_id = Column(String(50))
    field_id = Column(String(50))

    @classmethod
    def add_all(cls,comFields):
        cls.session.add_all(comFields)
        cls.session.flush()
