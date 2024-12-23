### TODO list
1. [x] 启用github，csv 数据变更，自动更新图片
   1. [x] bug: csv 数据变更未触发 github action
   2. [x] bug: 图片名称没变，导致 readme 更新很慢
2. [ ] 自动抓取贝壳数据，并保存为csv文件，当前为 App 手动截图获取数据
3. [x] 每日早上8点自动运行 daily_jobs.py 脚本，执行数据抓取、数据处理、图表绘制
4. [ ] 部署到服务器，每日自动运行
5. [x] 每次运行成功后，调用 API 发送 Bark 消息到指定手机

### 当前运行步骤：
1. 贝壳 App 每日截图一次，截图文件放到目录 `nj_bk_daily_pictures/`
1. 截图数据填写到 njhouse_bk_daily.csv
1. 运行脚本 daily_jobs.py: `python daily_jobs.py`
