from common.db import BaseModel

from sqlalchemy import Column, String, Text,func

class JobModel(BaseModel):
    __tablename__ = 'job'

    id = Column(String(50), primary_key=True)
    job_id = Column(String(50),nullable=False)
    job_name = Column(String(50), nullable=False)
    job_salary = Column(String(50), nullable=False)
    # 工作所在城市id
    job_place_id = Column(String(50), nullable=False)
    # 工作经验
    job_exper = Column(String(50), nullable=False)
    # 学历要求
    job_record = Column(String(10))
    # 职位诱惑
    job_attract = Column(String(500))
    # 职位描述
    job_descr = Column(Text)
    # 工作详情地址
    job_site = Column(String(50), nullable=False)
    # 工作创建时间
    job_create_time = Column(String(50))
    com_id = Column(String(50),nullable=False)

    @classmethod
    def add(cls,job):
        cls.session.add(job)
        cls.session.flush()

    @classmethod
    def add_all(cls,jobs):
        cls.session.add_all(jobs)
        cls.session.flush()

    @classmethod
    def count(cls,job_id):
        query = cls.session.query(func.count(cls.id))
        if job_id:
            query = query.filter(cls.job_id==job_id)
        return query.scalar()