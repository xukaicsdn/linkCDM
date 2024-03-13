"""
@Filename:   commons/models
@Author:      三木
@Time:        2023/1/13 13:09
@Describe:    声明yaml用例格式
"""
import json
import logging
from dataclasses import asdict, dataclass
from typing import Optional

import allure
import yaml
# from certifi.__main__ import args

from commons.templates import Template

logger = logging.getLogger(__name__)
from commons import settings


@dataclass
class CaseInfo:
    title: str
    request: dict
    extract: dict
    # validate: dict
    validate: Optional[dict] = None  # validate参数是非必要的，可以选择不传入，即在yaml可写也可不写断言了
    fixture_code: list = ""
    parametrize: list = ""
    epic: str = settings.allure_epic
    feature: str = settings.allure_feature
    story: str = settings.allure_story

    is_run: str = ""  # 非必传，等于1代表跳过此用例
    post_function: str = ""

    def __post_init__(self):
        """实例化之后自动运行"""
        self.parametrize_data = []  # 保存字典形式的参数化数据

        if self.parametrize:
            args_name = self.parametrize[0]
            args_values = self.parametrize[1:]

            for args_value in args_values:
                assert len(args_name) == len(args_value), "参数化数据未对齐"

                d = dict(zip(args_name, args_value))  # 列表转字典
                self.parametrize_data.append(d)

    def ddt(self):
        if not self.parametrize:  # 单用例测试
            yield self
            return

        self.parametrize = []
        for data in self.parametrize_data:  # 参数化测试
            case_info_str = self.to_yaml()
            case_info_str = Template(case_info_str).render(data)  # 参数化注入用例
            yield CaseInfo.by_yaml(case_info_str)

    def to_json(self):
        json_str = json.dumps(asdict(self))

        return json_str

    @classmethod
    def by_json(cls, json_str):

        obj = cls(**json.loads(json_str))
        return obj

    def to_yaml(self):
        yaml_str = yaml.dump(
            asdict(self),
            allow_unicode=True,
            sort_keys=False,
        )

        return yaml_str

    @classmethod
    def by_yaml(cls, yaml_str):
        obj = cls(**yaml.safe_load(yaml_str))
        return obj

    @allure.step("断言")
    def assert_all(self):
        """
        执行所有断言
        :return:
        """
        if not self.validate:
            return
        for assert_type, assert_data in self.validate.items():
            for msg, data in assert_data.items():
                a, b = data[0], data[1]
                match assert_type:
                    case "equals":
                        logger.info(f"assert {a} == {b}, {msg}")
                        assert a == b, msg
                    case "not_equals":
                        logger.info(f"assert {a} != {b}, {msg}")
                        assert a != b, msg
                    case "contains":
                        logger.info(f"assert {a} in {b}, {msg}")
                        assert a in b, msg
                    case "not_contains":
                        logger.info(f"assert {a} not in {b}, {msg}")
                        assert a not in b, msg
