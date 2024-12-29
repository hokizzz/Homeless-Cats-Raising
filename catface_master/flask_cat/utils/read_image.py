# -*- coding: utf-8 -*-
# Time : 2024/12/24 23:07
# Author : lirunsheng
# User : l'r's
# Software: PyCharm
# File : read_image.py
import os
import pandas as pd
import base64
from datetime import datetime


def image_to_base64(image_path):
    """
    将图像文件转换为 Base64 编码。

    :param image_path: 图像文件的路径
    :return: 图像的 Base64 编码字符串
    """
    with open(image_path, "rb") as img_file:
        img_data = img_file.read()
        return base64.b64encode(img_data).decode('utf-8')


def get_image_info(directory, extensions=None):
    """
    读取指定文件夹中的图像信息，解析文件名，并构造 Pandas DataFrame。

    :param directory: 文件夹路径
    :param extensions: 可选，指定图像文件的扩展名列表，默认为支持常见图像格式
    :return: 包含图像信息的 Pandas DataFrame 和 `name=other` 的计数
    """
    filenames = os.listdir(directory)

    # 默认支持的图像格式
    if extensions is None:
        extensions = ['.jpg', '.jpeg', '.png', '.bmp']

    image_info = []
    other_count = 0  # 用于统计 `name=other` 的数量

    for filename in filenames:
        # 过滤文件扩展名
        if any(filename.lower().endswith(ext) for ext in extensions):
            file_path = os.path.join(directory, filename)

            # 按文件名解析时间和名称（格式：time_name.jpg）
            try:
                time_str, name, weight = filename.split('_')
                time_str = time_str.strip()
                name = name.split('.')[0].strip()  # 去掉扩展名
                timestamp = datetime.strptime(time_str, '%Y%m%d%H%M%S')  # 按时间格式解析
            except ValueError:
                print(f"文件名 {filename} 格式错误，跳过")
                continue

            # 统计 `name=other`
            if name.lower() == "other":
                other_count += 1

            # 获取图像的 Base64 数据
            img_base64 = image_to_base64(file_path)

            # 添加信息到列表
            image_info.append({
                'id': len(image_info) + 1,  # 从1开始
                'name': name,
                'time': timestamp,
                'data': img_base64,
                'weight':weight
            })

    # 转换为 Pandas DataFrame
    df = pd.DataFrame(image_info)

    # 按时间排序
    if not df.empty:
        df = df.sort_values(by='time')

    return df, other_count


def dataframe_to_dict_list(df):
    """
    将 Pandas DataFrame 转换为字典列表。

    :param df: Pandas DataFrame
    :return: 字典列表
    """
    return df.to_dict(orient='records')


# # 示例用法
# directory = r'K:\working\YOLOv5-Lite-master\face_cat\catface-master\recognition_result'  # 替换为你的文件夹路径
#
# # 获取图像信息和统计 `name=other` 的数量
# df_images, other_count = get_image_info(directory)
#
# # 将 Pandas DataFrame 转换为字典列表
# image_dict_list = dataframe_to_dict_list(df_images)
#
# # 输出结果
# print(f"Name='other' 的图像数量: {other_count}")
# print("图像信息（按时间排序）：")
# for image in image_dict_list:
#     print(image)

