import pytest
# from yamlMany01 import YamlFile
from commons.files import YamlFile
import yaml
from typing import *


# @pytest.fixture(scope="function")
# def login():
#     print("====总conftest文件 登录功能，返回账号，token===")
#     name = ["testyy", "testjj"]
#     token = "npoi213bn4"
#     yield name, token
#     print("====总conftest文件 退出登录！！！====")

# 优化
def run_fixtures(fixture_yaml_file: str) -> None:
    """
        执行前置和后置，yield之前是前置，yield之后是后置（巧妙用了yield原理）
    """
    fixture_def: List[str] = YamlFile(fixture_yaml_file)["fixture_code"]
    for fixture in fixture_def:
        if "fixture" in yaml.dump(fixture):
            exec(fixture, globals())


run_fixtures("config.yaml")
# YamlFile("config.yaml").run_fixtures()  # 为什么不行呢，作用域问题？？？？？
# fixture_def: List[str] = YamlFile("config.yaml")["fixture_code"]
# for fixture in fixture_def:
#     if "fixture" in yaml.dump(fixture):
#         print("==========执行============")
#         exec(fixture)

# if "fixture" in yaml.dump(fixture_def):
#     print("==========执行============")
#     exec(fixture_def[0])


# @pytest.fixture(autouse=True)
# def get_info(login):
#     name, token = login
#     print(login)
#     print(f"==总conftest文件 每个用例都默认自动调用的fixture：打印用户token： {token} ==")


def test_get_info(login, login01, aa=7):
    print(login, type(login))
    print(login01, type(login01))
    name, token = login
    name01, token01 = login01
    print("***项目最基础用例：获取用户个人信息***")
    print(f"用户名:{name[0]}, token:{token}")
    print(f"用户名:{name01[0]}, token:{token01},{aa}")


def my_range(n):
    i = 0
    while i < n:
        yield i
        i += 1


# 使用生成器对象迭代
for num in my_range(5):
    print(num)


class TestExample:

    @pytest.fixture
    def setup(self):
        num1 = 10
        num2 = 5
        return num1, num2

    def test_addition(self, setup):
        num1, num2 = setup
        assert num1 + num2 == 15

    def test_subtraction(self, setup):
        num1, num2 = setup
        assert num1 - num2 == 5


class TestLogin:
    @pytest.mark.parametrize("username, password, token",
                             [("user1", "password1", "token1"), ("user2", "password2", "token2")])
    def test_login(self, username, password, token):
        # 使用username和password登录，提取token并保存到yaml文件中
        print("===============================", username, password, token, "===============================")


class TestAPI:
    @pytest.mark.parametrize("token", ["token1", "token2"])
    def test_api(self, token):
        # 使用提取的token进行接口请求
        print("===============================", token, "===============================")


if __name__ == '__main__':
    pytest.main(['-v', '-s', __file__])
    # pytest.main(['-s', __file__, '--workers=1', '--tests-per-worker=4'])
