from common.db import BaseModel
import uuid
from sqlalchemy import Column, Integer, String, Text

class JobModel(BaseModel):
    __tablename__ = 'job'

    id = Column(Integer, primary_key=True)
    job_name = Column(String(50), nullable=False)
    job_salary = Column(String(50), nullable=False)
    job_place_id = Column(String(50), nullable=False)
    job_exper = Column(String(50), nullable=False)
    job_record = Column(String(10))
    job_type = Column(String(10))
    job_attract = Column(String(500))
    job_descr = Column(Text)
    job_site = Column(String(50), nullable=False)
    job_create_time = Column(String(50))
    job_update_time = Column(String(50))

    @classmethod
    def add(cls,job_name,job_salary,job_place_id,job_exper,job_record,job_type,job_attract,job_descr,job_site,job_create_time,job_update_time,id=uuid.uuid1()):
        job = cls(job_name=job_name,job_salary=job_salary,job_place_id=job_place_id,job_exper=job_exper,job_record=job_record,
                  job_type=job_type,job_attract=job_attract,job_descr=job_descr,job_site=job_site,job_create_time=job_create_time,job_update_time=job_update_time,id=id)
        cls.session.merge(job)
        cls.session.flush()

    @classmethod
    def add_all(cls,jobs):
        cls.session.add_all(jobs)
        cls.session.flush()