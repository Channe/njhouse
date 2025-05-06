import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os
import matplotlib as mpl
import platform

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

def plot_total_listings(csv_path):
    # 设置字体
    set_font()
    
    # 读取CSV文件
    df = pd.read_csv(csv_path, encoding='utf-8-sig')
    
    try:
        policy_df = pd.read_csv('house_scripts/njhouse_stock_daily/njhouse_policy.csv', encoding='utf-8-sig')
        has_policy_data = True
    except FileNotFoundError:
        print("政策数据文件不存在，将不显示政策信息")
        has_policy_data = False
    
    # 确保CSV数据类型正确
    # 确保日期列是datetime格式
    df['日期'] = pd.to_datetime(df['日期'])
    
    # 确保总挂牌房源列是数值型
    df['总挂牌房源'] = pd.to_numeric(df['总挂牌房源'], errors='coerce')
    
    # 处理昨日住宅成交量为空的情况
    df['昨日住宅成交量'] = pd.to_numeric(df['昨日住宅成交量'], errors='coerce').fillna(0)
    
    # 按日期排序
    df = df.sort_values('日期')
    
    # 创建图表和主Y轴
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    # 标记周末背景
    weekend_mask = df['日期'].dt.dayofweek.isin([5, 6])  # 5是周六，6是周日
    weekend_dates = df[weekend_mask]['日期']
    for date in weekend_dates:
        ax1.axvspan(date - pd.Timedelta(hours=12), 
                   date + pd.Timedelta(hours=12),
                   alpha=0.1,
                   color='gray',
                   label='周末' if date == weekend_dates.iloc[0] else "")
    
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
    
    # 标注政策点
    if has_policy_data:
        # 确保政策日期是datetime格式
        policy_df['日期'] = pd.to_datetime(policy_df['日期'])
        
        for idx, row in policy_df.iterrows():
            policy_date = row['日期']
            
            # 查找匹配的数据点
            matching_data = df[df['日期'] == policy_date]
            
            if not matching_data.empty:
                # 获取政策日期对应的总挂牌房源数据
                y_value = matching_data['总挂牌房源'].iloc[0]
                
                # 使用日期和数值绘制标记点
                ax1.scatter(policy_date, y_value,
                          marker='*',
                          s=200,  # 相当于markersize=15的效果
                          color='red',
                          zorder=5)
                
                # 添加政策说明文本
                ax1.annotate(f"{row['政策']}\n{row['具体内容']}",
                            xy=(policy_date, y_value),
                            xytext=(10, 10),
                            textcoords='offset points',
                            fontsize=8,
                            bbox=dict(boxstyle='round,pad=0.5',
                                    fc='yellow',
                                    alpha=0.5),
                            arrowprops=dict(arrowstyle='->'))
    
    # 设置标题
    plt.title('南京房市数据统计', fontsize=14, pad=15)
    
    # 合并所有图例
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + [bars], labels1 + ['昨日住宅成交量'], loc='upper left')
    
    # 设置x轴日期格式
    plt.gcf().autofmt_xdate()
    
    # 添加水印
    ax1.text(0.5, 0.5, 'github.com/Channe/njhouse',
             fontsize=40,
             color='gray',
             alpha=0.2,
             ha='center',
             va='center',
             transform=ax1.transAxes,
             rotation=45)
    
    # 调整布局
    plt.tight_layout()
    
    # 获取当前日期时间戳
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # 确保目标目录存在
    os.makedirs('house_scripts/plot_pngs', exist_ok=True)
    
    # 保存图片
    image_path = f"house_scripts/plot_pngs/plot_njhouse_total_listings_{timestamp}.png"
    plt.savefig(image_path, bbox_inches='tight', dpi=300)
    plt.close()
    
    print(f"图表已保存为 {image_path}")
    
    # 返回生成的文件名，供 daily_jobs.py 使用
    return image_path

if __name__ == "__main__":
    csv_path = 'house_scripts/njhouse_stock_daily/njhouse_stock_daily.csv'
    if os.path.exists(csv_path):
        plot_total_listings(csv_path)
    else:
        print(f"CSV文件不存在，请检查路径: {csv_path}") 