from common.db import BaseModel

from sqlalchemy import Column, Integer, String, Text

class JobTagRModel(BaseModel):
    __tablename__ = 'job_tag_r'

    id = Column(String(50), primary_key=True)
    job_id = Column(String(50))
    tag_id = Column(String(50))

    @classmethod
    def add_all(cls,job_tag_rs):
        cls.session.add_all(job_tag_rs)
        cls.session.flush()