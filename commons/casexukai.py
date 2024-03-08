import os
from pathlib import Path

from commons.files import YamlFile
import json

case_path = Path(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "testcases", "cdm", "login"))
# print(case_path)

class TestExample:
    @classmethod
    def find_yaml_case(cls, path: Path = case_path):
        """
        加载yaml用例
        """
        yaml_case_list = path.glob("**/test_*.yaml")
        for yaml_path in yaml_case_list:
            print(f"load file {yaml_path=}")
            file = YamlFile(yaml_path)  # 读取yaml文件
            # print(json.dumps(dict(file), sort_keys=False, indent=4, separators=(',', ': ')).encode("utf-8").decode("unicode_escape"))

print(TestExample.find_yaml_case())
