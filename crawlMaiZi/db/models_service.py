from setting import db_config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from crawlMaiZi.db.models import MaiZiCourse, MaiziLesson, base


class ModelService(object):
    def __init__(self):
        self.engine = create_engine('mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(
            db_config['user'], db_config['password'], db_config['host'], db_config['port'], db_config['name']))
        self.db_session = sessionmaker(bind=self.engine)
        self.session = self.db_session()

    def create_tables(self):
        base.metadata.create_all(self.engine)

    def close_session(self):
        self.session.close()

    def insert_maizi_course(self, course_name, course_url):
        self.session.add(
            MaiZiCourse(
                course_name=course_name,
                course_url=course_url,
                flag=False
            )
        )
        self.session.commit()
        self.session.flush()

    def insert_maizi_lesson(self, c_id, lesson_name, lesson_url):
        self.session.add(
            MaiziLesson(
                c_id=c_id,
                lesson_name=lesson_name,
                lesson_url=lesson_url,
                flag=False,

            )
        )
        self.session.commit()
        self.session.flush()

    def query_maizi_course_id_by_course_name(self, course_name):
        id = self.session.query(MaiZiCourse.id).filter(MaiZiCourse.course_name == course_name).first()
        self.session.flush()
        return id

    def query_maizi_lesson_id_lesson_name_lesson_url_by_c_id(self, c_id):
        data = self.session.query(
            MaiziLesson.id,
            MaiziLesson.lesson_name,
            MaiziLesson.lesson_url,
        ).filter(
            (MaiziLesson.c_id == c_id)
        ).all()
        self.session.flush()
        return data
