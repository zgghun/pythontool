# -*- coding:utf-8 -*-
import os, shutil

# 图片格式转换
import configparser

from PIL import Image


def format_convert(source, target, root_path, format='.jpg'):
    img = Image.open(source)  # type: Image.Image
    width, height = img.size

    # 图片像素调整
    factor = 750 / width
    width = width * factor
    height = height * factor
    img = img.resize((int(width), int(height)), Image.ANTIALIAS)

    # 图片通道转换
    # if ext != ".jpg":
    img = img.convert("RGB")

    filedir, filename = os.path.split(source)
    path, ext = os.path.splitext(source)

    filedir = filedir.replace(root_path, target)
    if not os.path.exists(filedir):
        os.mkdir(filedir)
    filename = filename.replace(ext, format)
    new_img = os.path.join(filedir, filename)

    img.save(new_img)


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
    config.read('config.ini')
    items = config.items('config')
    dict = {}
    for k, v in items:
        dict[k] = v
    return dict

if __name__ == '__main__':
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

