import yaml
import os.path


class Loader(yaml.Loader):
    def __init__(self, stream):
        self._root = os.path.split(stream.name)[0]
        # print(os.path.split(stream.name),11111111111111)
        super(Loader, self).__init__(stream)

    def include(self, node):
        filename = os.path.join(self._root, self.construct_scalar(node))
        with open(filename, 'r') as f:
            return yaml.load(f, Loader)


Loader.add_constructor('!include', Loader.include)


class YamlFile(dict, yaml.Loader):
    def __init__(self, path, stream):
        super(dict, self).__init__()  # 让对象完成原有实例化步骤
        # 接下来完成自定义实例化步骤
        self._path = path  # 保存文件路径
        self._root = os.path.split(stream.name)[0]
        yaml.Loader.__init__(self, stream)
        self.load()

    def load(self):
        with open(self._path, "r", encoding="utf-8") as f:
            data = yaml.load(f,)
            print(data), print(type(data))
        if data:
            self.update(data)  # 保存文件内容,修改是在内存中修改的，并没有修改yaml文件，需要保存文件才行



if __name__ == '__main__':
    with open('./a.yaml', 'r', encoding='UTF-8') as f:
        result = yaml.load(f, Loader)
        print(result)


