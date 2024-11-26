import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from PIL import Image
from io import BytesIO

# 读取 Excel 文件，提取宝可梦名称
input_file = 'pokemon.csv'  # 替换为您的文件路径
output_folder = 'pokemon_images'  # 存储图片的文件夹
os.makedirs(output_folder, exist_ok=True)

# 读取 Excel 数据
df = pd.read_csv(input_file)

# 确保有 'Name' 列
if 'Name' not in df.columns:
    raise ValueError("The Excel file must contain a 'Name' column.")

# 获取所有宝可梦的名称
pokemon_names = df['Name'].tolist()


# 定义函数抓取图片
def fetch_pokemon_image(name):
    base_url = f"https://bulbapedia.bulbagarden.net/wiki/{name}"
    try:
        # 发送请求
        response = requests.get(base_url)
        if response.status_code != 200:
            print(f"Failed to fetch page for {name}")
            return None

        # 解析 HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        # 查找图片标签（通常是第一个包含 Pokémon 图片的标签）
        image_tag = soup.find('a', class_='image')
        if image_tag and image_tag.img:
            # 提取图片 URL
            img_url = 'https:' + image_tag.img['src']
            return img_url
        else:
            print(f"Image not found for {name}")
            return None
    except Exception as e:
        print(f"Error fetching image for {name}: {e}")
        return None


# 定义函数下载图片
def download_image(img_url, name):
    try:
        response = requests.get(img_url)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            img_path = os.path.join(output_folder, f"{name}.png")
            img.save(img_path)
            print(f"Downloaded: {name}")
            return img_path
        else:
            print(f"Failed to download image for {name}")
            return None
    except Exception as e:
        print(f"Error downloading image for {name}: {e}")
        return None


# 主逻辑：抓取并下载图片
df['Image URL'] = df['Name'].apply(fetch_pokemon_image)
df['Local Path'] = df.apply(
    lambda row: download_image(row['Image URL'], row['Name']) if row['Image URL'] else None, axis=1
)

# 保存结果到 Excel 文件
output_excel = '/mnt/data/pokemon_with_downloaded_images.xlsx'
df.to_excel(output_excel, index=False)

print(f"Process completed. Results saved to {output_excel}")
