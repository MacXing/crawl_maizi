# -*- coding: utf-8 -*- 
# @Time : 2019/3/28 10:48 
# @Author : Allen 
# @Site :  配置文件
import os

# 本机迅雷地址
xunlei_path = r"E:\迅雷\Program\Thunder.exe"

# 迅雷默认保存地址
xunlei_default_save_path = r"F:\迅雷下载"

# 保存视频目录
save_video_dir = r"F:\迅雷下载"

# vide_url.txt 路径
video_url_path = os.path.dirname(os.path.abspath(__file__)) + r'\resource\video_course_url.txt'

# 数据库配置
db_config = {
    'host': '192.168.160.36',
    'user': 'root',
    'password': 'gzxiaoi',
    'name': 'crawler',
    'port': '3306',
}
