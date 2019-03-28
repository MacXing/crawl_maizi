# coding: utf-8
import json
import time

import requests
from crawlMaiZi.url_processor import get_beautiful_object
import os
import shutil


def parse_josn():
    data_lists = []
    with open("video_course_url.txt", "r", encoding='utf-8') as file:
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


def check_start(save_path, filename):
    '''
    检测文件是否开始下载
    '''
    cache_file = filename + ".xltd"
    cache_file2 = filename+'.mp4'
    return os.path.exists(os.path.join(save_path, cache_file)) or os.path.exists(os.path.join(save_path, cache_file2))


def check_end(save_path, fiename):
    '''
    检测文件是否下载完成
    '''
    return os.path.exists(os.path.join(save_path, fiename))


def get_filename(url):
    return os.path.split(url)[1]


def xunlei_downloader(url):
    '''
    下载资源:迅雷下载
    返回文件路径表示下载完成 否则失败
    '''
    default_save_path = 'F:\迅雷下载'  # 迅雷有一个默认下载地址，所有迅雷下载的东西都在这个目录下
    os.system(r'"E:\迅雷\Program\Thunder.exe" {url}'.format(url=url))
    # 一定要休眠一段时间,执行命令后要等一会儿迅雷才会新建任务,
    # 然后还要寻找资源,这都需要时间,大概多久,自己去测试,根据网络、资源不同,寻找资源的速度也不同
    # 如果没启动迅雷,迅雷还会启动一会儿
    time.sleep(2)
    filename = get_filename(url)
    print("正在下载 {}".format(filename))
    # 检测任务是否已开始
    # 有时候会因为资源不存在,或者迅雷该死的版权问题会下载失败
    if check_start(default_save_path, filename):
        while True:
            # 每分钟检测一次是否下载完成
            time.sleep(5)
            if check_end(default_save_path, filename):
                return os.path.join(default_save_path, filename)

    else:
        return False


def move_and_rename_video(save_path, file_path,video_name):
    create_path(save_path)
    shutil.move(file_path, save_path)
    source_file_name = os.path.split(file_path)[-1]
    os.rename(os.path.join(save_path,source_file_name),os.path.join(save_path,video_name))
    print("下载完成：{}".format(video_name))


def download_video_for_xunlei():
    data = parse_josn()
    for d in data:
        # print(d)
        save_path = os.path.join('F:\迅雷下载', d['course_name'])
        video_url = d['video_url']
        file_path = xunlei_downloader(video_url)
        if file_path:
            video_name = d['lesson_name']+'.mp4'
            move_and_rename_video(save_path, file_path,video_name)


if __name__ == "__main__":
    download_video_for_xunlei()
