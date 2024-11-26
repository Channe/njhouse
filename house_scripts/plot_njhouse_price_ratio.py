import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os
from matplotlib.font_manager import FontProperties

def plot_price_change_ratio(csv_path):
    # 读取房价数据
    df = pd.read_csv(csv_path, encoding='utf-8-sig')
    
    # 读取政策数据
    policy_df = pd.read_csv('./njhouse_stock_daily/njhouse_policy.csv', encoding='utf-8-sig')
    policy_df['日期'] = pd.to_datetime(policy_df['日期'])
    
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
    
    # 在创建图表之后，绘制主数据线之前添加周末背景
    # 获取周末的日期
    weekend_mask = df['日期'].dt.dayofweek.isin([5, 6])  # 5是周六，6是周日
    weekend_dates = df[weekend_mask]['日期']
    
    # 为每个周末日期添加垂直的背景色带
    for date in weekend_dates:
        ax1.axvspan(date - pd.Timedelta(hours=12),  # 向左偏移12小时
                   date + pd.Timedelta(hours=12),  # 向右偏移12小时
                   alpha=0.2,
                   color='lightgray',
                   label='周末' if date == weekend_dates.iloc[0] else "")  # 只在图例中显示一次
    
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
    
    # 移除重复的周末图例（如果有的话）
    unique_labels = []
    unique_lines = []
    seen_labels = set()
    for line, label in zip(lines1 + lines2, labels1 + labels2):
        if label not in seen_labels:
            seen_labels.add(label)
            unique_labels.append(label)
            unique_lines.append(line)
    
    ax1.legend(unique_lines, unique_labels, prop=font, loc='upper left')
    
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
    
    # 在图表上标注政策点
    for idx, row in policy_df.iterrows():
        # 找到政策日期对应的降涨比值
        if row['日期'] in df['日期'].values:
            y_value = df[df['日期'] == row['日期']]['价格变动比'].values[0]
            
            # 添加政策点标记
            ax1.plot(row['日期'], y_value, 
                    marker='*',
                    markersize=15,
                    color='red',
                    zorder=5)
            
            # 添加政策说明文本
            ax1.annotate(row['政策'],
                        xy=(row['日期'], y_value),
                        xytext=(10, 10),
                        textcoords='offset points',
                        fontproperties=font,
                        fontsize=8,
                        bbox=dict(boxstyle='round,pad=0.5',
                                fc='yellow',
                                alpha=0.5),
                        arrowprops=dict(arrowstyle='->'))
    
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