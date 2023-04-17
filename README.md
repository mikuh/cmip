# cmip
一个高效的信息处理库。

## 安装
```shell
pip install -U cmip
```

## 用法

### 1. 动态渲染异步爬虫
example: 
```python
from cmip.web import web_scraping
import asyncio
urls = [
        "https://baidu.com",
        "https://qq.com",
        # ...More URL
    ]
asyncio.run(web_scraping(urls, output_path="output", max_concurrent_tasks=10, save_image=True, min_img_size=200))
```
参数含义：

| urls | 网页链接（包含协议头） |
| --- | --- |
| output_path | 输出路径 |
| max_concurrent_tasks | 最大同时执行任务数，根据自身机器资源和网络情况调整 |
| save_image | 是否保存图片 |
| min_img_size | 当图片小于这个值时不爬取 |