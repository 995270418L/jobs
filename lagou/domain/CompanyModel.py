# 城市信息

import uuid

from sqlalchemy import Column, Integer, String, Text, func, DateTime

from common.db import BaseModel


class CompanyModel(BaseModel):
    __tablename__ = 'company'

    id = Column(String(50), primary_key=True)
    com_id = Column(String(50), nullable=False)
    com_name = Column(String(50), nullable=False)
    com_process = Column(String(10), nullable=False)
    com_number = Column(String(30))
    com_city_id = Column(String(10), nullable=False)
    com_num_school = Column(Integer)
    com_num_social = Column(Integer)
    com_site = Column(String(50), nullable=False)
    com_source = Column(String(50), nullable=False)
    com_fullname = Column(String(255))
    com_address = Column(String(50))
    com_info = Column(Text)
    com_record_time = Column(DateTime)
    com_resume_rate = Column(Integer)

    @classmethod
    def add(cls,company):
        cls.session.add(company)
        cls.session.flush()

    @classmethod
    def addAll(cls,companies):
        cls.session.add_all(companies)
        cls.session.flush()

    @classmethod
    def count(cls,id):
        query = cls.session.query(func.count(cls.id))
        if id:
            query = query.filter(cls.id == id)
        return query.scalar()

    @classmethod
    def delete_all(cls):
        sql = 'truncate table company'
        cls.session.execute(sql)
        cls.session.flush()