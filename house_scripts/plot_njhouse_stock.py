import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

# 设置中文字体显示
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # 设置中文字体为黑体
plt.rcParams['axes.unicode_minus'] = False     # 解决负号显示问题

def plot_total_listings(csv_path):
    # 读取CSV文件
    df = pd.read_csv(csv_path, encoding='utf-8-sig')
    
    # 确保日期列是datetime格式
    df['日期'] = pd.to_datetime(df['日期'])
    
    # 按日期排序
    df = df.sort_values('日期')
    
    # 创建折线图
    plt.figure(figsize=(10, 6))
    plt.plot(df['日期'], df['总挂牌房源'], marker='o', linestyle='-')
    plt.title('南京总挂牌房源数', fontsize=14, pad=15)
    plt.xlabel('日期')
    plt.ylabel('总挂牌房源')
    plt.grid(True)
    
    # 添加水印
    plt.text(0.5, 0.5, '水印',
             fontsize=40,
             color='gray',
             alpha=0.2,
             ha='center',
             va='center',
             transform=plt.gca().transAxes,
             rotation=45)
    
    # 调整x轴显示
    plt.xticks(rotation=45)  # 旋转标签45度
    plt.tight_layout()       # 自动调整布局，防止标签被切割
    
    # 获取当前日期
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    # 保存图片
    image_path = f"plot_njhouse_total_listings.png"
    plt.savefig(image_path, bbox_inches='tight')
    plt.close()
    
    print(f"折线图已保存为 {image_path}")

if __name__ == "__main__":
    csv_path = 'njhouse_stock_daily/njhouse_stock_daily.csv'
    if os.path.exists(csv_path):
        plot_total_listings(csv_path)
    else:
        print("CSV文件不存在，请检查路径。") 