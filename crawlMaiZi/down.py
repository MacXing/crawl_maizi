# coding: utf-8
import json
import requests
from multiprocessing import Pool
from crawlMaiZi.url_processor import get_beautiful_object
import os


def parse_josn():
    data_lists = []
    with open("course_information.txt", "r", encoding='utf-8') as file:
        for line in file.readlines():
            try:
                mzjson = json.loads(line)
                data_lists.append(mzjson)
            except:
                pass
    return data_lists


def create_path(path):
    if os.path.exists(path):
        pass
    else:
        os.makedirs(path)
    return path


def multiprocess_save_video_url(data):
    headers = {
        "User-Agent": "Mozilla / 5.0(Windows NT 6.1;Win64;x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 71.0.35 78.98 Safari / 537.36",
        "Accept-Encoding": "identity;q=1, *;q=0",
        "Referer": data['url'],
    }
    try:
        r = requests.get(data["url"], headers=headers)
        video_url = get_beautiful_object(r.content).find('source')['src']
        data['video_url'] = video_url
        write_json_file('video_course_url.txt', data)
        print("Success insert {} 课下的 {} video视频".format(data['course_name'], data['lesson_name']))
    except:
        pass


def write_json_file(file_name, data_json):
    with open(file_name, 'a', encoding='utf-8') as file:
        file.write(json.dumps(data_json, ensure_ascii=False) + '\n')


def downLoad(data):
    headers = {
        "User-Agent": "Mozilla / 5.0(Windows NT 6.1;Win64;x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 71.0.35 78.98 Safari / 537.36",
        "Accept-Encoding": "identity;q=1, *;q=0",
        "Referer": data['url'],
    }
    r = requests.get(data["url"], headers=headers)
    base_path = create_path("E://MaiZi//" + data["course_name"] + "//")
    video = base_path + data["lesson_name"] + ".mp4"
    video_url = get_beautiful_object(r.content).find('source')['src']
    v_r = requests.get(video_url, headers=headers, stream=True)
    try:
        with open(video, "wb") as code:
            code.write(v_r.content)
        print(video + " is down load success!")
    except Exception as e:
        print("the down video:%(LessName)s load is failer\n url is :%(LessHref)s \n videourl:%(LessVideo)s " % data)
        print(e)


if __name__ == "__main__":
    pool = Pool(10)
    datas = parse_josn()
    pool.map(multiprocess_save_video_url, datas)
    pool.close()
    pool.join()
