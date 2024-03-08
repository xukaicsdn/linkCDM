"""
@Filename:   commons/settings
@Author:      三木
@Time:        2023/1/13 15:35
@Describe:    ...
"""
from pathlib import Path
import os
import time
from iniconfig import IniConfig

project_path = os.path.split(os.path.realpath(__file__))[0].split('tools')[0]
name = "beifan"
age = 18
case_path = r"testcases/debug/mysql"  # yaml用例存放目录
extract_path = r"data/extract.yaml"  # 数据关联保存路径


db_host = "192.168.2.44"
db_port = 3306
db_user = "root"
db_password = "Howlink@1401"
db_database = "mysql"


allure_epic = "项目名称：CDM"
allure_feature = "默认feature"
allure_story = "默认story"
allure_description = f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}"

base_url = ""  # 接口项目base_url
timeout = 10

rsa_public = "data/public.pem"
rsa_private = "data/private.pem"


def load_ini(path, section="api_test"):
    path = Path(path)
    data = {}
    if path.exists():
        ini = IniConfig(str(path))
        if section in ini:
            data = dict(ini[section].items())

    for k, v in data.items():
        globals()[k] = v


load_ini("pytest.ini")
Path(extract_path).parent.mkdir(exist_ok=True)
open(extract_path, "a").close()
