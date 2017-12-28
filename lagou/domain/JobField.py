
from sqlalchemy import Column, String
import uuid
from common.db import BaseModel


class JobField(BaseModel):
    __tablename__ = 'job_field'

    id = Column(String(50), primary_key=True)
    field_id = Column(String(30), nullable=False)
    field_name = Column(String(50))

    @classmethod
    def add(cls,field_id,field_name,id=uuid.uuid1()):
        jobField = cls(id=id,field_id=field_id,field_name=field_name)
        cls.session.merge(jobField)
        cls.session.flush()

    @classmethod
    def add_all(cls,jobFields):
        cls.session.add_all(jobFields)
        cls.session.flush()

