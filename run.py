from scrapyd_api import ScrapydAPI

# 1. 在命令行执行scrapyd开启scrapyd服务
# scrapyd

# 2. 获取scrapydAPI接口
scrapyd = ScrapydAPI('http://localhost:6800')

# 3. 新增一个project（包含version、egg）
with open('dist/1_0.egg', 'rb') as egg:
    scrapyd.add_version('SearchEngine', '1.0', egg)

# 4. 启动一个spider
conf = {
    'allowed_domains': ['www.epochtimes.com'],
    'start_urls': ['https://www.epochtimes.com'],
}
custom_settings = {
    'CLOSESPIDER_TIMEOUT': 180,
    'CONCURRENT_ITEMS': 100,
    'CONCURRENT_REQUESTS': 16,
    'CONCURRENT_REQUESTS_PER_IP': 16,
    'COOKIES_ENABLED': False,
    'DEPTH_LIMIT': 2,
    'DOWNLOAD_TIMEOUT': 10,
}
import json
jobid = scrapyd.schedule('SearchEngine', 'demo', settings=custom_settings, conf=json.dumps(conf))
