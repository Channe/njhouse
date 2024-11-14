import os
import pytesseract
from PIL import Image
import pandas as pd
from datetime import datetime

def extract_data_from_image(image_path):
    try:
        # 使用pytesseract从图片中提取文字
        text = pytesseract.image_to_string(Image.open(image_path), lang='chi_sim')
        
        # 提取日期、成交量、涨价和降价数据
        date = None
        volume = None
        price_increase = None
        price_decrease = None
        
        for line in text.split('\n'):
            if '日期' in line:
                date = line.split('：')[1].strip()
            elif '成交量' in line:
                volume = line.split('：')[1].strip()
            elif '涨价' in line:
                price_increase = line.split('：')[1].strip()
            elif '降价' in line:
                price_decrease = line.split('：')[1].strip()
        
        return {
            '日期': date,
            '成交量': volume,
            '涨价': price_increase,
            '降价': price_decrease
        }
    except Exception as e:
        print(f"从图片中提取数据时发生错误: {str(e)}")
        return None

def save_data_to_csv(data, csv_path):
    try:
        df_new = pd.DataFrame([data])
        
        # 如果文件存在，读取现有数据并将新数据放在最上面
        if os.path.exists(csv_path):
            df_existing = pd.read_csv(csv_path, encoding='utf-8-sig')
            df_combined = pd.concat([df_new, df_existing], ignore_index=True)
            df_combined.to_csv(csv_path, index=False, encoding='utf-8-sig')
        else:
            # 如果文件不存在，直接创建新文件
            df_new.to_csv(csv_path, index=False, encoding='utf-8-sig')
            
        return True
    except Exception as e:
        print(f"保存数据时发生错误: {str(e)}")
        return False

def process_images_in_directory(directory_path, csv_path):
    for filename in os.listdir(directory_path):
        if filename.endswith('.png') or filename.endswith('.jpg'):
            image_path = os.path.join(directory_path, filename)
            data = extract_data_from_image(image_path)
            if data:
                save_data_to_csv(data, csv_path)

if __name__ == "__main__":
    image_directory = 'nj_bk_daily_pictures'
    csv_path = 'nj_bk_daily.csv'
    process_images_in_directory(image_directory, csv_path)
    print("所有图片数据已处理并保存到 nj_bk_daily.csv")
