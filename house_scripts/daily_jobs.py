# 每日任务

import subprocess

def run_scripts():
    # 1. 执行数据抓取脚本
    try:
        print('\n开始执行南京房产数据抓取任务...')
        subprocess.run(['python', 'njhouse_stock.py'], check=True)
        print('南京房产数据抓取任务执行成功')
        
        # 2. 数据抓取成功后，执行总房源图表绘制
        try:
            print('\n开始执行总房源图表绘制...')
            subprocess.run(['python', 'plot_njhouse_stock.py'], check=True)
            print('总房源图表绘制成功')
            print('\n所有任务执行完成！')
        except subprocess.CalledProcessError as e:
            print(f'总房源图表绘制失败: {str(e)}')
            
    except subprocess.CalledProcessError as e:
        print(f'南京房产数据抓取任务执行失败: {str(e)}')

if __name__ == "__main__":
    run_scripts()
