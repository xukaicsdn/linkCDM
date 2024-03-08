import yaml
import os
import json


class Loader(yaml.Loader):
    def __init__(self, stream):
        self._root = os.path.split(stream.name)[0]
        super(Loader, self).__init__(stream)

    def include(self, node):
        filename = os.path.join(self._root, self.construct_scalar(node))
        with open(filename, 'r') as f:
            return yaml.load(f, Loader)


Loader.add_constructor('!include', Loader.include)


class YamlFile(dict):
    def __init__(self, path):
        super(dict, self).__init__()  # 让对象完成原有实例化步骤
        # 接下来完成自定义实例化步骤
        self._path = path  # 保存文件路径
        self.load()

    def load(self):
        with open(self._path, "r", encoding="utf-8") as f:
            data = yaml.load(f, Loader)  # 获取文件内容并作为流对象传入
            # print(data)
            # print(type(data))
        if data:
            self.update(data)


if __name__ == '__main__':
    # with open(r"E:\Program Files (x86)\JetBrains\PyCharm 2021.1.3\workspace\api_framework\test\b.yaml", "r", encoding="utf-8") as f:
    #     result = yaml.load(f, Loader)  # 获取文件内容并作为流对象传入
    #     print(result)
    #     print(type(result))
    yaml_file = YamlFile(r"E:\Program Files (x86)\JetBrains\PyCharm 2021.1.3\workspace\api_framework\xukai\a.yaml")
    print(yaml_file)
    print(type(dict(yaml_file)))
    print(type(json.dumps(dict(yaml_file))), 1111111111111111111111111111111111111111111)
