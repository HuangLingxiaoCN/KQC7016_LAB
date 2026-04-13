# Python 网页爬虫代码深度分析报告



## 一、报告概述

本报告针对一段**Python 静态网页爬虫代码**进行全面解析，明确代码功能、执行逻辑、核心技术点及应用价值。该代码实现了从指定招聘网站（Fake Jobs）**批量抓取招聘信息、筛选Python相关岗位**的完整功能，是入门级网页数据采集的标准实践案例。

### 代码核心目标

1. 爬取目标网站的全部招聘岗位信息（职位名称、公司、工作地点）；

2. 对原始数据进行格式化处理，去除冗余空白字符；

3. 精准筛选出包含Python关键词的相关岗位并单独输出。

---

## 二、开发环境与依赖库

### 1. 核心依赖库

|库名称|作用|
|---|---|
|`requests`|发送HTTP网络请求，获取目标网页的原始HTML源码|
|`BeautifulSoup4`|解析HTML/XML文档，实现网页元素的精准查找与数据提取|
### 2. 环境安装命令

```Bash

pip install requests beautifulsoup4
```

---

## 三、代码整体执行流程

代码采用**模块化设计**，执行流程分为6个核心步骤，逻辑清晰、层层递进：

1. 导入依赖库 → 2. 请求网页获取源码 → 3. 解析HTML生成结构化对象 → 4. 定位数据容器 → 5. 提取全量岗位信息 → 6. 筛选Python相关岗位并输出

---

## 四、代码分段详细解析

### （一）模块导入

```Python

import requests
from bs4 import BeautifulSoup
```

- 功能：引入爬虫必备的两个第三方库，为后续网络请求和网页解析提供工具支持。

### （二）网页请求与数据获取

```Python

URL = "https://realpython.github.io/fake-jobs/"
page = requests.get(URL)
```

- 定义目标招聘网站的URL地址；

- 使用`requests.get()`发送GET请求，获取服务器返回的网页响应对象。

### （三）HTML网页解析

```Python

soup = BeautifulSoup(page.content, "html.parser")
```

- 将网页原始内容（`page.content`）传入`BeautifulSoup`；

- 使用Python内置的`html.parser`解析器，将杂乱的HTML源码转换为可操作的结构化对象`soup`。

### （四）定位数据总容器

```Python

results = soup.find(id="ResultsContainer")
```

- 核心方法：`find()` → 查找**第一个**匹配条件的元素；

- 精准定位网页中`id="ResultsContainer"`的标签，该标签是所有招聘岗位的总容器，缩小数据查找范围。

### （五）提取全量招聘岗位信息

```Python

job_elements = results.find_all("div", class_="card-content")
for job_element in job_elements:
    # 定位岗位核心信息标签
    title_element = job_element.find("h2", class_="title")
    company_element = job_element.find("h3", class_="company")
    location_element = job_element.find("p", class_="location")
    # 三级数据输出：原始标签 → 纯文本 → 格式化纯文本
    print(title_element)
    print(title_element.text)
    print(title_element.text.strip())
```

1. `find_all()`：查找容器内所有`class="card-content"`的`div`标签，每个标签对应一个岗位卡片；

2. 循环遍历所有岗位，分别提取**职位名称、公司、工作地点**；

3. 数据输出对比：

    - 直接打印元素：输出完整HTML标签；

    - `.text`：提取标签内纯文本（含多余空格/换行）；

    - `.text.strip()`：去除文本首尾空白字符，输出干净规整的数据（工业级标准用法）。

### （六）筛选Python相关岗位

```Python

# 模糊匹配包含Python的岗位标题
python_jobs = results.find_all("h2", string=lambda text: "python" in text.lower())
# 向上查找父标签，获取完整岗位卡片
python_job_elements = [h2_element.parent.parent.parent for h2_element in python_jobs]
# 循环输出筛选后的岗位信息
for job_element in python_job_elements:
    title = job_element.find("h2", class_="title").text.strip()
    company = job_element.find("h3", class_="company").text.strip()
    location = job_element.find("p", class_="location").text.strip()
    print(title, company, location)
```

1. 模糊筛选：使用`lambda`匿名函数，不区分大小写匹配包含`python`的岗位标题；

2. 层级定位：通过`.parent`向上遍历3层父标签，从标题元素还原完整的岗位卡片；

3. 数据输出：打印筛选后干净的Python岗位信息。

---

## 五、核心技术点总结

|技术语法|功能说明|应用场景|
|---|---|---|
|`requests.get()`|发送网络请求，获取网页源码|所有静态网页数据采集|
|`BeautifulSoup()`|HTML文档解析|结构化处理网页数据|
|`find()/find_all()`|查找网页元素|精准定位目标数据|
|`.text`|提取标签内纯文本|获取网页文字内容|
|`.strip()`|去除空白字符|数据清洗、格式化|
|`.parent`|向上查找父级元素|层级式定位网页数据|
|`lambda`|匿名函数筛选|模糊匹配、条件过滤|
---

## 六、代码运行效果

1. 输出网站**全部招聘岗位**的原始标签、纯文本、格式化文本；

2. 统计并输出**Python相关岗位的数量**；

3. 单独打印所有Python岗位的**职位名称、公司、工作地点**，数据整洁无冗余。

