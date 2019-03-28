# -*- coding: utf-8 -*-
# @Time : 2019/3/28 12:13
# @Author : Allen
# @Site :
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Text, Integer, DATETIME, Boolean
from datetime import datetime

base = declarative_base()


class TimeStampCreateUpdate(object):
    create_time = Column(DATETIME, nullable=False, default=datetime.now)
    update_time = Column(DATETIME, onupdate=datetime.now)


class GetUUID(object):
    id = Column(Integer, primary_key=True, autoincrement=True)


class MaiZiCourse(base, GetUUID, TimeStampCreateUpdate):
    __tablename__ = 'maizi_course'
    course_name = Column(String(200))
    course_url = Column(String(200))
    flag = Column(Boolean)


class MaiziLesson(base, GetUUID, TimeStampCreateUpdate):
    __tablename__ = 'maizi_lesson'
    c_id = Column(Integer)
    lesson_name = Column(String(200))
    lesson_url = Column(String(2000))
    flag = Column(Boolean)
