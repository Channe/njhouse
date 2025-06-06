import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os
import matplotlib as mpl
import platform

# 切换到脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# 根据操作系统设置合适的中文字体
def set_font():
    system = platform.system()
    if system == 'Darwin':  # macOS
        mpl.rcParams['font.sans-serif'] = ['PingFang SC', 'Heiti SC', 'Microsoft YaHei', 'Arial Unicode MS']
    elif system == 'Linux':  # GitHub Actions (Ubuntu)
        mpl.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'Noto Sans CJK JP', 'DejaVu Sans']
    else:  # Windows
        mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
    
    mpl.rcParams['axes.unicode_minus'] = False
    mpl.rcParams['font.family'] = 'sans-serif'

def plot_price_change_ratio(csv_path):
    # 设置字体
    set_font()
    
    # 读取房价数据
    df = pd.read_csv(csv_path, encoding='utf-8-sig')
    
    # 读取政策数据
    try:
        policy_df = pd.read_csv('njhouse_stock_daily/njhouse_policy.csv', encoding='utf-8-sig')
        policy_df['日期'] = pd.to_datetime(policy_df['日期'])
        has_policy_data = True
    except FileNotFoundError:
        print("政策数据文件不存在，将不显示政策信息")
        has_policy_data = False
    
    # 将日期列转换为日期类型
    df['日期'] = pd.to_datetime(df['日期'])
    
    # 按日期排序
    df = df.sort_values('日期')
    
    # 计算降价/涨价比值
    df['降价房源'] = pd.to_numeric(df['降价房源'], errors='coerce')
    df['涨价房源'] = pd.to_numeric(df['涨价房源'], errors='coerce').replace(0, float('nan'))
    df['价格变动比'] = df['降价房源'] / df['涨价房源']
    
    # 替换无穷大值为NaN，并填充NaN值为0，使用推荐的写法避免警告
    df['价格变动比'] = df['价格变动比'].replace([float('inf'), -float('inf')], float('nan'))
    df['价格变动比'] = df['价格变动比'].fillna(0)
    
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
    
    # 转换成交量为数值并处理缺失值
    df['成交量'] = pd.to_numeric(df['成交量'], errors='coerce').fillna(0)
    
    # 绘制成交量柱状图
    bars = ax2.bar(df['日期'], df['成交量'],
            alpha=0.3,
            color='gray',
            label='成交量')
    
    # 设置左侧Y轴标签
    ax1.set_ylabel('降涨比')
    
    # 设置右侧Y轴标签
    ax2.set_ylabel('成交量')
    
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
    
    ax1.legend(unique_lines, unique_labels, loc='upper left')
    
    # 设置标题
    ax1.set_title('南京二手房降涨比与成交量', 
                fontsize=14, 
                pad=15)
    
    # 添加网格线
    ax1.grid(True, linestyle='--', alpha=0.7)
    
    # 添加水印
    ax1.text(0.5, 0.5, 'github.com/Channe/njhouse',
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
    if has_policy_data:
        for idx, row in policy_df.iterrows():
            # 找到政策日期对应的降涨比值
            matching_data = df[df['日期'] == row['日期']]
            if not matching_data.empty:
                y_value = matching_data['价格变动比'].iloc[0]
                
                # 添加政策点标记
                ax1.scatter(row['日期'], y_value, 
                        marker='*',
                        s=200,  # 相当于markersize=15
                        color='red',
                        zorder=5)
                
                # 添加政策说明文本
                ax1.annotate(row['政策'],
                            xy=(row['日期'], y_value),
                            xytext=(10, 10),
                            textcoords='offset points',
                            fontsize=8,
                            bbox=dict(boxstyle='round,pad=0.5',
                                    fc='yellow',
                                    alpha=0.5),
                            arrowprops=dict(arrowstyle='->'))
    
    # 获取当前日期时间戳
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # 确保目标目录存在
    os.makedirs('plot_pngs', exist_ok=True)
    
    # 保存图片
    image_path = f"plot_pngs/plot_njhouse_bk_daily_{timestamp}.png"
    plt.savefig(image_path, bbox_inches='tight')
    plt.close()
    
    print(f"折线图已保存为 {image_path}")
    
    # 返回生成的文件名，供 daily_jobs.py 使用
    return image_path

if __name__ == "__main__":
    csv_path = "njhouse_stock_daily/njhouse_bk_daily.csv"
    if os.path.exists(csv_path):
        plot_price_change_ratio(csv_path)
    else:
        print(f"CSV文件不存在，请检查路径: {csv_path}")