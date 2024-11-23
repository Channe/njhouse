### TODO list
1. 自动抓取贝壳数据，并保存为csv文件，当前为 App 手动截图获取数据
2. 每日自动运行 daily_jobs.py 脚本，执行数据抓取、数据处理、图表绘制
3. 部署到服务器，每日自动运行

### 当前运行步骤：
1. 贝壳 App 每日截图一次，截图文件放到目录 `nj_bk_daily_pictures/`
1. 截图数据填写到 njhouse_bk_daily.csv
1. 运行脚本 daily_jobs.py: `python daily_jobs.py`
