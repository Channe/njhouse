import pytesseract
from PIL import Image
import pandas as pd
from datetime import datetime
import re
import os
import argparse
import cv2

def parse_arguments():
    """
    解析命令行参数
    """
    parser = argparse.ArgumentParser(description='从图片中提取房产数据并保存到CSV')
    parser.add_argument('--image_path', '-i', 
                      type=str, 
                      required=True,  # 设置为必需参数
                      help='图片文件的路径')
    parser.add_argument('--output', '-o',
                      type=str,
                      default='./njhouse_stock_daily/njhouse_bk_daily_ocr.csv',  # 设置默认输出文件
                      help='输出CSV文件的路径 (默认: njhouse_bk_daily_ocr.csv)')
    return parser.parse_args()

def extract_data_from_image(image_path):
    """
    从图片中提取数据
    """
    # 打开并预处理图片
    img = Image.open(image_path)
    
    # 设置tesseract路径（如果需要的话）
    pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'
    
    # 使用中文识别
    custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789-,.'
    text = pytesseract.image_to_string(img, lang='chi_sim', config=custom_config)
    
    # 初始化数据字典
    data = {
        '日期': datetime.now().strftime('%Y-%m-%d'),
        '成交均价': None,
        '成交量': None,
        '新增挂牌': None,
        '涨价房源': None,
        '降价房源': None,
        '看房人数': None,
        '看房量': None,
        '成交周期': None
    }
    
    # 使用正则表达式提取数字
    # 这里需要根据实际图片内容调整正则表达式
    lines = text.split('\n')
    for line in lines:
        # 成交均价 (通常是带小数点的数字)
        if '均价' in line or '成交均价' in line:
            price = re.search(r'(\d+\.?\d*)', line)
            if price:
                data['成交均价'] = float(price.group(1))
        
        # 成交量
        if '成交量' in line:
            volume = re.search(r'(\d+)', line)
            if volume:
                data['成交量'] = int(volume.group(1))
                
        # 新增挂牌
        if '新增挂牌' in line:
            new_listings = re.search(r'(\d+)', line)
            if new_listings:
                data['新增挂牌'] = int(new_listings.group(1))
                
        # 其他数据项的提取...
        # 根据实际图片格式补充其他数据的提取逻辑
    
    return data

def save_to_csv(data, csv_path):
    """
    保存数据到CSV文件
    """
    # 如果文件存在，读取现有数据
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
    else:
        # 创建新的DataFrame
        df = pd.DataFrame(columns=['日期', '成交均价', '成交量', '新增挂牌', 
                                 '涨价房源', '降价房源', '看房人数', '看房量', '成交周期'])
    
    # 添加新数据
    new_row = pd.DataFrame([data])
    df = pd.concat([df, new_row], ignore_index=True)
    
    # 保存到CSV
    df.to_csv(csv_path, index=False)
    print(f"数据已保存到: {csv_path}")

def preprocess_image(image):
    # 转换为灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 二值化处理
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # 可选：降噪
    denoised = cv2.fastNlMeansDenoising(binary)
    
    return denoised

def main():
    # 解析命令行参数
    args = parse_arguments()
    
    try:
        # 检查图片文件是否存在
        if not os.path.exists(args.image_path):
            raise FileNotFoundError(f"找不到图片文件: {args.image_path}")
            
        # 提取数据
        print(f"正在处理图片: {args.image_path}")
        data = extract_data_from_image(args.image_path)
        
        # 保存数据
        save_to_csv(data, args.output)
        
        print("处理完成！")
        
    except Exception as e:
        print(f"发生错误: {str(e)}")
        exit(1)  # 发生错误时退出程序

if __name__ == "__main__":
    main()