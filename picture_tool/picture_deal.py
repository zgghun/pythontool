# -*- coding:utf-8 -*-
import os, shutil

# 图片格式转换
import configparser
from datetime import datetime

from PIL import Image


def format_convert(source, target, root_path, format='.jpg'):
    img = Image.open(source)  # type: Image.Image
    width, height = img.size

    # 图片像素调整
    factor = 750 / width
    width = width * factor
    height = height * factor
    img = img.resize((int(width), int(height)), Image.ANTIALIAS)

    # 图片通道转换（原来是 RGBA 模式，太大，统一改成 RGB）
    # if ext != ".jpg":
    img = img.convert("RGB")

    # 分割文件路径和文件名
    filedir, filename = os.path.split(source)
    # 获取文件后缀
    ext = os.path.splitext(source)[1]
    filedir = filedir.replace(root_path, target)
    if not os.path.exists(filedir):
        os.makedirs(filedir)
    filename = filename.replace(ext, format)
    new_img = os.path.join(filedir, filename)

    # 保存转换后的图片
    img.save(new_img)

    with open(os.path.join(target, 'log.txt'), 'a') as f:
        out = "{}\n" \
              "    |------ {} kb ---> {} kb\n"
        out = out.format(source.replace(root_path, '')
                         , int(os.path.getsize(source) / 1024)
                         , int(os.path.getsize(new_img) / 1024))
        print(out, file=f)


# 获取指定文件夹下特定后缀的文件绝对路径
def find_picture_path(root_path, suffix=None):
    abs_path = []
    for root, dirs, files in os.walk(root_path):
        for file in files:
            if suffix:
                if os.path.splitext(file)[1] in suffix:
                    abs_path.append(os.path.join(root, file))
            else:
                abs_path.append(os.path.join(root, file))
    return abs_path


def read_config():
    config = configparser.ConfigParser()
    config.read('config.ini', 'utf-8')
    items = config.items('config')
    dict = {}
    for k, v in items:
        dict[k] = v
    return dict


if __name__ == '__main__':
    start_time = datetime.now()
    conf = read_config()

    start_path = conf.get('start_path')
    target_path = conf.get('target_path')
    suffix = ['.jpg', '.png']

    picture_path_list = find_picture_path(start_path, suffix)
    print('共找到：{} 个特定文件'.format(len(picture_path_list)))

    if os.path.exists(target_path):
        shutil.rmtree(target_path)

    for index, path in enumerate(picture_path_list):
        format_convert(path, target=target_path, root_path=start_path)

    ent_time = datetime.now()
    with open(os.path.join(target_path, 'log.txt'), 'a') as f:
        print(ent_time, file=f)
        print(start_time, file=f)
        print("共计耗时     {}".format(ent_time - start_time), file=f)
