# 每日任务

import subprocess
import os
import sys

# 切换到脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

def update_readme(bk_image_path, stock_image_path):
    """更新 README.md 中的图片链接"""
    # 确保路径没有重复的house_scripts前缀
    # 首先移除可能存在的house_scripts/前缀
    bk_relative_path = bk_image_path
    stock_relative_path = stock_image_path
    
    if bk_relative_path.startswith('house_scripts/'):
        bk_relative_path = bk_relative_path[len('house_scripts/'):]
    
    if stock_relative_path.startswith('house_scripts/'):
        stock_relative_path = stock_relative_path[len('house_scripts/'):]
    
    readme_content = f"""### 南京房产数据

#### 贝壳每日成交量统计、降涨比
![plot_njhouse_bk_daily](./house_scripts/{bk_relative_path})

#### 南京房地产每日挂牌总量、成交量
![plot_njhouse_total_listings](./house_scripts/{stock_relative_path})
"""
    
    # 使用项目根目录的相对路径
    readme_path = os.path.join(os.path.dirname(script_dir), 'README.md')
    
    # 写入更新后的内容
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print('README.md 更新成功')
    
    # 调用发送通知脚本
    try:
        subprocess.run([sys.executable, 'send_notification.py'], check=True)
    except subprocess.CalledProcessError as e:
        print(f'Failed to send notification: {str(e)}')

def run_scripts():
    # 检查必要的环境变量
    required_keys = ['BARK_SECRET_KEY', 'BARK_SECRET_KEY_TINA']
    missing_keys = [key for key in required_keys if not os.getenv(key)]
    
    if missing_keys:
        print(f'警告：未找到以下环境变量: {", ".join(missing_keys)}')
    
    bk_image_path = None
    stock_image_path = None
    
    # 1. 执行数据抓取脚本
    try:
        print('\n开始执行南京房产数据抓取任务...')
        subprocess.run([sys.executable, 'njhouse_stock.py'], check=True)
        print('南京房产数据抓取任务执行成功')
        
        # 2. 数据抓取成功后，执行总房源图表绘制
        try:
            print('\n开始执行总房源图表绘制...')
            result = subprocess.run([sys.executable, 'plot_njhouse_stock.py'], 
                                 capture_output=True, 
                                 text=True,
                                 check=True)
            stock_image_path = result.stdout.strip().split('图表已保存为 ')[-1]
            print('总房源图表绘制成功')
            
            # 3. 执行房价比例图表绘制
            try:
                print('\n开始执行房价比例图表绘制...')
                result = subprocess.run([sys.executable, 'plot_njhouse_price_ratio.py'],
                                     capture_output=True,
                                     text=True,
                                     check=True)
                bk_image_path = result.stdout.strip().split('折线图已保存为 ')[-1]
                print('房价比例图表绘制成功')
                
                # 4. 更新 README.md
                if bk_image_path and stock_image_path:
                    update_readme(bk_image_path, stock_image_path)
                
                print('\n所有任务执行完成！')
            except subprocess.CalledProcessError as e:
                print(f'房价比例图表绘制失败: {str(e)}')
                
        except subprocess.CalledProcessError as e:
            print(f'总房源图表绘制失败: {str(e)}')
            
    except subprocess.CalledProcessError as e:
        print(f'南京房产数据抓取任务执行失败: {str(e)}')

if __name__ == "__main__":
    run_scripts()
