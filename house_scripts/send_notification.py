import os
import requests

def send_notification():
    # 获取环境变量中的密钥
    keys = []
    if os.getenv('BARK_SECRET_KEY'):
        keys.append(os.getenv('BARK_SECRET_KEY'))
    if os.getenv('BARK_SECRET_KEY_TINA'):
        keys.append(os.getenv('BARK_SECRET_KEY_TINA'))
    
    if not keys:
        print("Error: No BARK keys found in environment variables")
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