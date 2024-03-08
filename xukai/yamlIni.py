import configparser
import yaml
import re

# 创建 ConfigParser 对象
config = configparser.ConfigParser()

# 读取 .ini 文件
config.read('config.ini')

# 将 .ini 文件的值转换为字典
ini_data = {}
for section in config.sections():
    ini_data[section] = dict(config.items(section))

# 读取 YAML 文件
with open('config.yaml', 'r', encoding='utf-8') as f:
    yaml_data = f.read()

# 替换 YAML 中的 ${} 引用
def replace_fn(match):
    key = match.group(1)
    section, option = key.split('_')
    return ini_data[section][option]

yaml_data = re.sub(r'\$\{(.+?)\}', replace_fn, yaml_data)

# 解析 YAML
config_data = yaml.load(yaml_data, Loader=yaml.FullLoader)

# 输出结果
print(config_data)
