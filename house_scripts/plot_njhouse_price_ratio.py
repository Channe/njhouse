import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os
from matplotlib.font_manager import FontProperties

def plot_price_change_ratio(csv_path):
    # 读取CSV文件
    df = pd.read_csv(csv_path, encoding='utf-8-sig')
    
    # 将日期列转换为日期类型
    df['日期'] = pd.to_datetime(df['日期'])
    
    # 按日期排序
    df = df.sort_values('日期')
    
    # 计算降价/涨价比值
    df['价格变动比'] = df['降价房源'] / df['涨价房源']
    
    # 设置中文字体
    font = FontProperties(fname='/System/Library/Fonts/Hiragino Sans GB.ttc')  # Mac系统自带的黑体
    
    # 创建图表和第一个Y轴
    fig, ax1 = plt.subplots(figsize=(12, 6))  # 调整图表大小
    
    # 绘制主数据线（降涨比）
    line1 = ax1.plot(df['日期'], df['价格变动比'], 
             marker='o',
             linestyle='-',
             markerfacecolor='red',
             markersize=6,
             linewidth=1,
             label='降涨比')
    
    # 添加比例10的红色参考线
    ax1.axhline(y=10, 
                color='red',
                linestyle='--',
                alpha=0.8,
                linewidth=1,
                label='警戒线(10)')
    
    # 创建第二个Y轴
    ax2 = ax1.twinx()
    
    # 绘制成交量柱状图
    bars = ax2.bar(df['日期'], df['成交量'],
            alpha=0.3,
            color='gray',
            label='成交量')
    
    # 设置左侧Y轴标签
    ax1.set_ylabel('降涨比', fontproperties=font)
    
    # 设置右侧Y轴标签
    ax2.set_ylabel('成交量', fontproperties=font)
    
    # 合并两个轴的图例
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, prop=font, loc='upper left')
    
    # 设置标题
    ax1.set_title('南京二手房降涨比与成交量', 
                fontproperties=font,
                fontsize=14, 
                pad=15)
    
    # 添加网格线
    ax1.grid(True, linestyle='--', alpha=0.7)
    
    # 添加水印
    ax1.text(0.5, 0.5, '水印',
             fontproperties=font,  # 使用字体
             fontsize=40,
             color='gray',
             alpha=0.2,
             ha='center',
             va='center',
             transform=ax1.transAxes,
             rotation=45)
    
    # 调整x轴显示
    ax1.tick_params(axis='x', rotation=45)
    plt.tight_layout()
    
    # 获取当前日期
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    # 保存图片
    image_path = f"plot_njhouse_bk_daily.png"
    plt.savefig(image_path, bbox_inches='tight')
    plt.close()
    
    print(f"折线图已保存为 {image_path}")
    
    # 打印统计信息
    print("\n降涨比统计信息：")
    print(f"平均降涨比：{df['价格变动比'].mean():.2f}")
    print(f"最大降涨比：{df['价格变动比'].max():.2f}")
    print(f"最小降涨比：{df['价格变动比'].min():.2f}")

if __name__ == "__main__":
    csv_path = "njhouse_stock_daily/njhouse_bk_daily.csv"
    if os.path.exists(csv_path):
        plot_price_change_ratio(csv_path)
    else:
        print("CSV文件不存在，请检查路径。")