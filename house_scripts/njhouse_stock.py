import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime, timedelta
import pytz
import pandas as pd

# 切换到脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

def get_house_data():
    url = "http://njzl.njhouse.com.cn/stock"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 直接查找包含特定文本的span标签
        total = soup.find('span', string=lambda x: '总挂牌房源' in str(x))
        agency = soup.find('span', string=lambda x: '中介挂牌房源' in str(x))
        personal = soup.find('span', string=lambda x: '个人挂牌房源' in str(x))
        yesterday = soup.find('span', string=lambda x: '昨日住宅成交量' in str(x))
        
        data = {
            '总挂牌房源': total.text.split('：')[1].strip() if total else '未找到',
            '中介挂牌房源': agency.text.split('：')[1].strip() if agency else '未找到',
            '个人挂牌房源': personal.text.split('：')[1].strip() if personal else '未找到',
            '昨日住宅成交量': yesterday.text.split('：')[1].strip() if yesterday else '未找到'
        }
        return data
            
    except Exception as e:
        print(f"错误详情: {str(e)}")
        return f"获取数据时发生错误: {str(e)}"

def save_data_to_csv(data):
    try:
        # 获取北京时间
        beijing_tz = pytz.timezone('Asia/Shanghai')
        current_time = datetime.now(beijing_tz)
        # 获取前一天的日期
        yesterday = current_time - timedelta(days=1)
        date_str = yesterday.strftime('%Y-%m-%d')
        
        # 获取周几（使用中文表示）
        weekday_map = {
            0: '周一',
            1: '周二',
            2: '周三',
            3: '周四',
            4: '周五',
            5: '周六',
            6: '周日'
        }
        weekday = weekday_map[yesterday.weekday()]
        
        # 创建目录
        save_dir = 'njhouse_stock_daily'
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        
        # CSV文件路径
        csv_path = os.path.join(save_dir, 'njhouse_stock_daily.csv')
        
        # 准备新数据
        data['日期'] = date_str
        data['周几'] = weekday
        df_new = pd.DataFrame([data])
        
        # 如果文件存在，读取现有数据并将新数据放在最上面
        if os.path.exists(csv_path):
            df_existing = pd.read_csv(csv_path, encoding='utf-8-sig')
            df_combined = pd.concat([df_new, df_existing], ignore_index=True)
            df_combined.to_csv(csv_path, index=False, encoding='utf-8-sig')
        else:
            # 如果文件不存在，直接创建新文件
            df_new.to_csv(csv_path, index=False, encoding='utf-8-sig')
            
        return csv_path
    except Exception as e:
        print(f"保存数据时发生错误: {str(e)}")
        return None

def clean_duplicate_data(csv_path):
    # 检查并删除重复日期的数据
    df = pd.read_csv(csv_path, encoding='utf-8-sig')
    # 使用drop_duplicates方法删除重复的日期数据，保留最新的数据
    df.drop_duplicates(subset=['日期'], keep='last', inplace=True)
    # 将处理后的数据写回CSV文件
    df.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print("数据已清洗，重复日期的数据已删除。")

if __name__ == "__main__":
    result = get_house_data()
    if isinstance(result, dict):
        # 打印数据
        for key, value in result.items():
            print(f"{key}: {value}")
        
        # 保存数据并获取CSV文件路径
        csv_path = save_data_to_csv(result)
        if csv_path:
            print(f"\n数据已成功保存到 {csv_path}")
        else:
            print("\n数据保存失败")

        # 清洗数据
        clean_duplicate_data(csv_path)
    else:
        print(result)
