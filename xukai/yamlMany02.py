from xukai.yamlMany01 import YamlFile, Loader



if __name__ == '__main__':
    yaml_file = YamlFile(r"E:\Program Files (x86)\JetBrains\PyCharm 2021.1.3\workspace\api_framework\testcases\cdm\login\test_2_创建应用.yaml")
    print(yaml_file)
    print(type(yaml_file))