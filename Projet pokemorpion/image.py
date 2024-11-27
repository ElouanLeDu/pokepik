import os
from PIL import Image
import pandas as pds

def load_image_by_name(folder_path, image_name):
    """
    从指定文件夹中调取对应名字的图片。

    :param folder_path: 图片所在文件夹的路径
    :param image_name: 需要调取的图片名字（包括扩展名）
    :return: PIL.Image 对象，如果未找到则返回 None
    """
    # 获取文件夹中所有文件的列表
    image_name = f"{image_name}.png"
    files = os.listdir(folder_path)
    # 检查目标图片是否在文件列表中
    if image_name in files:
        image_path = os.path.join(folder_path, image_name)
        # 使用PIL加载图片
        try:
            img = Image.open(image_path)
            return img
        except Exception as e:
            print(f"无法加载图片 {image_name}，错误：{e}")
            return None
    else:
        print(f"未找到图片 {image_name} 在文件夹 {folder_path} 中。")
        return None


# 示例用法
folder = "pokemon_images"  # 替换为你的文件夹路径n
names = pds.read_csv("pokemon.csv")
lst=names["Name"]
for i in lst:# 替换为目标图片名称
    image = load_image_by_name(folder, i)


