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


### 2. 计算网页结构相似度
example:
```python
from cmip.web import html, simhash_array, hamming_distance_array
import requests

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}

html_text_baidu = requests.get("https://baidu.com", headers=headers).text
html_text_example_com = requests.get("https://example.com", headers=headers).text
html_text_example_org = requests.get("https://example.org", headers=headers).text
dom_tree_baidu = html.dom_tree(html_text_baidu)
dom_tree_example_com = html.dom_tree(html_text_example_com)
dom_tree_example_org = html.dom_tree(html_text_example_org)
simhash_baidu = simhash_array(dom_tree_baidu)
simhash_example_com = simhash_array(dom_tree_example_com)
simhash_example_org = simhash_array(dom_tree_example_org)

print("Similarity:", hamming_distance_array([simhash_example_com], [simhash_baidu, simhash_example_org]))
```
一般而言，当网页距离在4以内时，网页结构较为相似。