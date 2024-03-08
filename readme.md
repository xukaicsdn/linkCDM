# api_framework

## 简介

本框架只需要纯yaml文件，即可进行接口自动化测试，

既降低了接口自动化框架的使用难度，又打下了迁移自动化测试平台的基础

## 技术特点

本框架使用pytest+yaml+requests+allure 搭建，

实现了：

- yaml文件自动读取
- yaml文件动态保存
- yaml内容动态替换
- 数据驱动测试
- 接口关联（支持关联的数据有：状态码、响应头、响应正文、cookies、url等）
- 参数化测试
- 热加载函数（类型转换、加密解密、数据库查询等）
- 日志记录
- HTML测试报告
- post_function在断言之后

## 环境搭建

1. 安装Python 3.10

2. 安装JDK及allure

3. 下载本框架源码

4. 安装依赖

    ```
    pip install -r requirements.txt
    ```
5. 启动框架

    ```
    python main.py
    ```

## 框架用法

### 1. 创建测试项目

在`testcases` 目录下新建测试项目，例如

```
bbs
```

### 2. 创建测试文件

在测试项目中创建测试文件，文件名有以下要求

1. 文件名以`test_`开头
2. 文件名中列出本用例的执行序号
3. 文件后缀为`.yaml`

例如

```
test_1.yaml
test_2_home.yaml
```

### 3. 编写用例内容

yaml用例文件包含以下**必填字典**

| 字段名      | 用途   |
|----------|------|
| title    | 用例名称 |
| request  | 请求参数 |
| extract  | 变量提取 |
| validate | 接口断言 |

以及以下**选填字段**

| 字段名         | 用途    |
|-------------|-------|
| parametrize | 参数化测试 |
| epic        | 项目名称  |
| feature     | 模块名称  |
| story       | 功能名称  |

用例示例

```yaml
feature: 流程用例
title: 登录

request:
  method: POST
  url: /login/access_token
  json:
    email: bf@qq.com  
    password: bf123456 
    

extract:
  code: [ status_code, (.*), 0 ]
  access_token: [json, $.access_token, 0]

validate:
  equals: 
    状态码断言:
      - 200  
      - ${code}
```

### 4. 执行用例

```bash
python run.py
```

### 5. 查询测试结果

- 日志文件：位于logs目录下
- HTML测试报告：位于report目录下


### 6. 高级用法：用例和框架分离
1. 在任意位置新建目录，；例如`C:\Users\admin\Desktop\123`
2. 讲以下文件移动到新目录中
   - pytest.ini 
   - testcases目录（或者单个yaml用例文件）
3. 在新目录中执行本框架的main.py，例如
   ```
   python D:\api_framework\main.py
   ```
4. 框架将执行`C:\Users\admin\Desktop\123`下的用例文件，而为框架所在目录


## 联系方式

框架系本人原创开发，若需商用、定制或二次开发，欢迎联系：

> 微信：python_sanmu
