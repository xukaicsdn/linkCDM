"""
@Filename:   commons/files
@Author:      三木
@Time:        2023/1/13 13:12
@Describe:    ...
"""


import yaml
import os


class Loader(yaml.Loader):
    def __init__(self, stream):
        self._root = os.path.split(stream.name)[0]
        super(Loader, self).__init__(stream)

    def include(self, node):
        filename = os.path.join(self._root, self.construct_scalar(node))
        with open(filename, 'r', encoding="utf-8") as f:
            return yaml.load(f, Loader)


Loader.add_constructor('!include', Loader.include)


class YamlFile(dict):
    def __init__(self, path):
        super(dict, self).__init__()  # 让对象完成原有实例化步骤，实例化一个空得字典{}
        # 接下来完成自定义实例化步骤
        self._path = path  # 保存yaml文件路径
        self.load()

    def load(self):
        with open(self._path, "r", encoding="utf-8") as f:
            data = yaml.load(f, Loader=Loader)  # 获取文件内容并作为流对象传入
            print(data)
            # print(type(data))
        if data:
            self.update(data)

    def save(self):
        with open(self._path, "w", encoding="utf-8") as f:
            yaml.dump(dict(self), f)


if __name__ == '__main__':
    yaml_file = YamlFile(r'E:\Program Files (x86)\JetBrains\PyCharm 2021.1.3\workspace\api_framework\testcases\debug\mysql\linux7_mysql5_5_cdm\test_2_创建应用.yaml')
