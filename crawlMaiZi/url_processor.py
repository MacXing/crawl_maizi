# -*- coding: utf-8 -*- 
# @Time : 2019/3/8 14:06 
# @Author : Allen 
# @Site :  解析麦子学院www.m.maiziedu.com
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
import pprint
import json


def get_all_course():
    '''
    http://m.maiziedu.com/course/all-all/0-1/
    .........
    http://m.maiziedu.com/course/all-all/0-73/
    :return:
    '''
    url = 'http://m.maiziedu.com/course/{}/'
    return [url.format(i) for i in range(1, 1063)]


def requests_url(url):
    headers = {
        "User - Agent": "Mozilla / 5.0(Windows NT 6.1;Win64;x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 71.0.35 78.98 Safari / 537.36"
    }
    return requests.get(url=url, headers=headers)


def get_beautiful_object(html):
    return BeautifulSoup(html, 'html.parser')


def parser_teacher_id(url):
    try:
        r = requests_url(url)
        bs = get_beautiful_object(r.content)
        teacher_url = 'http://m.maiziedu.com' + bs.find('div', 'summary').a['href']
        print("Finish url:{}".format(url))
        write_txt(teacher_url)
    except:
        print("Error url:{}".format(url))


def multiprocess_teacher_url():
    teacher_urls = []
    urls = get_all_course()
    p = Pool(10)
    for url in urls:
        teacher_urls.append(p.apply_async(parser_teacher_id, args=[url, ]))
    p.close()
    p.join()


def write_txt(url):
    with open('teacher_urls.txt', 'a', encoding='utf-8') as file:
        file.write(url + '\n')


def read_txt():
    data = []
    with open('teacher_urls.txt', 'r', encoding='utf-8') as file:
        for line in file.readlines():
            data.append(line.strip())
    return list(set(data))


def multiprocess_course_url():
    p = Pool(10)
    for url in read_txt():
        p.apply_async(parser_teacher_home, args=[url, ])
    p.close()
    p.join()


def parser_teacher_home(url):
    bs = get_beautiful_object(requests_url(url).content)
    for li in bs.find('article', 'course_list').ul.find_all('li'):
        url = 'http://m.maiziedu.com' + li.a['href']
        course_name = li.a.find('strong').text
        parser_lesson_url(url, course_name)


def parser_lesson_url(url, course_name):
    bs = get_beautiful_object(requests_url(url).content)
    for li in bs.find('article', 'course-chapter').find('ol').find_all('li'):
        url = 'http://m.maiziedu.com' + li.a['href']
        lesson_name = li.a.text
        write_lesson_json(url, course_name, lesson_name)


def write_lesson_json(url, course_name, lesson_name):
    meta = {}
    meta['url'] = url
    meta['course_name'] = course_name
    meta['lesson_name'] = lesson_name
    with open('course_information.txt', 'a', encoding='utf-8') as file:
        file.write(json.dumps(meta, ensure_ascii=False) + '\n')
    print("Success crawl {} 课的 {} 节".format(course_name, lesson_name))


if __name__ == '__main__':
    multiprocess_teacher_url()  # 多进程爬取老师主页
    multiprocess_course_url()  # 多进程获取课程url
