import os
import requests
import pandas as pd

def send_notification():
    # 从 CSV 文件读取密钥
    try:
        df = pd.read_csv('BARK_SECRET_KEY.csv')
        keys = df.iloc[:, 0].tolist()  # 读取第一列的所有值
        
        if not keys or len(keys) < 2:
            print("Error: Not enough keys found in BARK_SECRET_KEY.csv")
            return
        
    except Exception as e:
        print(f"Error reading BARK_SECRET_KEY.csv: {e}")
        return
    
    # 使用 requests.Session
    session = requests.Session()
    
    # 发送请求到所有密钥
    for key in keys:
        # 构建请求的 URL
        url = f"https://api.day.app/{key}/南京房产每日数据?url=https://github.com/Channe/njhouse"
        
        # 发送请求
        try:
            response = session.get(url)
            if response.status_code == 200:
                print(f"Notification sent successfully for key: {key[:5]}...")
            else:
                print(f"Failed to send notification for key: {key[:5]}... Status code: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error sending notification for key: {key[:5]}... Error: {e}")
    
    session.close()

if __name__ == "__main__":
    send_notification()