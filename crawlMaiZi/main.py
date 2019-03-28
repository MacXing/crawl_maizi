# -*- coding: utf-8 -*- 
# @Time : 2019/3/28 10:51 
# @Author : Allen 
# @Site :  主程序
from crawlMaiZi.db.models_service import ModelService
from crawlMaiZi.download import parse_josn
from crawlMaiZi.download import download_video_by_course_name


def insert_table(data, models):
    for d in data:
        course_url = d['url']
        course_name = d['course_name']
        lesson_name = d['lesson_name']
        lesson_url = d['video_url']
        c_id = models.query_maizi_course_id_by_course_name(course_name)
        if c_id:
            models.insert_maizi_lesson(c_id[0], lesson_name, lesson_url)
        else:
            models.insert_maizi_course(course_name, course_url)
            c_id = models.query_maizi_course_id_by_course_name(course_name)
            models.insert_maizi_lesson(c_id[0], lesson_name, lesson_url)
    models.close_session()


def main():
    models = ModelService()
    # models.create_tables()  # 有则不用创建
    # data = parse_josn()  # json_数据
    # insert_table(data, models)  # 插入数据库
    download_video_by_course_name(models, '选修课-c++概述')  # 通过课程名称下载视频
    models.close_session()


if __name__ == '__main__':
    main()
