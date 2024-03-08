"""
@Filename:   commons/exchange.py
@Author:      三木
@Time:        2023/1/29 20:59
@Describe:    替换变量
"""
import copy
import json.decoder
import logging
import re

import allure
import jsonpath
import lxml.html
import yaml

from commons.files import YamlFile
from commons.templates import Template
import jinja2


logger = logging.getLogger(__name__)


class Exchange:
    def __init__(self, path):
        self.file = YamlFile(path)

    @allure.step("提取变量")
    def extract(self, resp, var_name, attr, expr: str, index: int):
        resp = copy.deepcopy(resp)
        try:
            resp.json = resp.json()
        except json.decoder.JSONDecodeError:
            resp.json = {"msg": " is not json data"}

        data = getattr(resp, attr)  #

        flag = expr[0]

        match flag:
            case '/':  # xpath
                html = lxml.html.fromstring(resp.text)
                res = html.xpath(expr)
            case '$':  # jsonpath
                data = dict(data)
                res = jsonpath.jsonpath(data, expr)
            case _:  # re
                res = re.findall(expr, str(data))

        print(f"{res=}")
        if res:  # 如果有数据
            value = res[index]
        else:  # 如果没有数据
            value = "not data"

        logger.debug(f"{var_name} = {value}")

        self.file[var_name] = value  # 保存变量
        self.file.save()  # 持久化存储到文件

    @allure.step("替换变量")
    def replace(self, data: dict):
        # 1. 将case_info 转成字符串
        case_info_str = yaml.dump(data)

        # 2. 替换字符串
        case_info_str = Template(case_info_str).render(self.file)

        # 3. 将字符串 转成case_info,case_info为字典类型
        new_case_info = yaml.safe_load(case_info_str)
        return new_case_info
