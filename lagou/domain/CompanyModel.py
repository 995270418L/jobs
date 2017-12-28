# 城市信息

import uuid
from sqlalchemy import Column, Integer, String, Text,func
from common.db import BaseModel

class CompanyModel(BaseModel):
    __tablename__ = 'company'

    id = Column(String(50), primary_key=True)
    com_id = Column(String(50))
    # short name
    com_name = Column(String(50), nullable=False)
    com_keyword = Column(String(225))
    com_type = Column(String(50), nullable=False)
    com_process = Column(String, nullable=False)
    com_number = Column(String(30))
    com_city_id = Column(Integer, nullable=False)
    com_num_school = Column(Integer)
    com_num_social = Column(Integer)
    com_site = Column(String(50), nullable=False)
    com_source = Column(String(50), nullable=False)
    com_fullname = Column(String(255))
    com_address = Column(String(50))
    com_info = Column(Text)
    com_lastupdate = Column(String(50))
    com_resume_rate = Column(Integer)
    com_tag_id = Column(String(50))

    @classmethod
    def add(cls, com_city_id,com_fullname,com_process,com_number,com_address,com_info,com_lastupdate,com_site,com_type,com_tag_id,com_keyword='',
            com_num_school=0,com_num_social=0,com_source='拉勾',com_name='',com_resume_info=0,id=uuid.uuid1()):
        company = cls(id=id,com_city_id = com_city_id,com_name=com_name,com_fullname= com_fullname,com_process=com_process,com_number=com_number,com_address=com_address,
                      com_info=com_info,com_lastupdate=com_lastupdate,com_site=com_site,com_type=com_type,com_keyword=com_keyword,com_num_school=int(com_num_school),
                      com_num_social=int(com_num_social),com_source=com_source,com_resume_info=com_resume_info,com_tag_id=com_tag_id)
        cls.session.merge(company)
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
