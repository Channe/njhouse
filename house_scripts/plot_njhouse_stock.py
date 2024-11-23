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
    
    # 创建图表和主Y轴
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    # 绘制总挂牌房源（折线图，主Y轴）
    color1 = 'tab:blue'
    ax1.grid(True, alpha=0.3)
    ax1.set_xlabel('日期')
    ax1.set_ylabel('总挂牌房源', color=color1)
    line1 = ax1.plot(df['日期'], df['总挂牌房源'], color=color1, marker='o', linestyle='-', label='总挂牌房源')
    ax1.tick_params(axis='y', labelcolor=color1)
    
    # 创建第二个Y轴，绘制成交量（柱状图）
    ax2 = ax1.twinx()
    color2 = 'tab:red'
    ax2.set_ylabel('昨日住宅成交量', color=color2)
    bars = ax2.bar(df['日期'], df['昨日住宅成交量'], alpha=0.3, color=color2, label='昨日住宅成交量')
    ax2.tick_params(axis='y', labelcolor=color2)
    
    # 设置标题
    plt.title('南京房市数据统计', fontsize=14, pad=15)
    
    # 添加图例
    # 合并折线图和柱状图的图例
    ax1.legend(line1 + [bars], ['总挂牌房源', '昨日住宅成交量'], loc='upper left')
    
    # 设置x轴日期格式
    plt.gcf().autofmt_xdate()  # 自动调整日期标签角度
    
    # 添加水印
    ax1.text(0.5, 0.5, '水印',
             fontsize=40,
             color='gray',
             alpha=0.2,
             ha='center',
             va='center',
             transform=ax1.transAxes,
             rotation=45)
    
    # 调整布局
    plt.tight_layout()
    
    # 保存图片
    image_path = "plot_njhouse_total_listings.png"
    plt.savefig(image_path, bbox_inches='tight', dpi=300)
    plt.close()
    
    print(f"图表已保存为 {image_path}")

if __name__ == "__main__":
    csv_path = 'njhouse_stock_daily/njhouse_stock_daily.csv'
    if os.path.exists(csv_path):
        plot_total_listings(csv_path)
    else:
        print("CSV文件不存在，请检查路径。") 