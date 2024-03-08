import yaml
from typing import List
import logging
import pdb
from pathlib import Path

import allure
import pytest
from xdist import get_xdist_worker_id

from commons import settings, funcs
from commons.exchange import Exchange
from commons.files import YamlFile, Loader
from commons.models import CaseInfo
from commons.session import Session
import time

logger = logging.getLogger(__name__)
session = Session(settings.base_url)
exchanger = Exchange(path=settings.extract_path)  # 数据交换，完成接口关联

case_path = Path(settings.case_path)
# print("case_path:" + str(case_path), "     type(case_path):" + str(type(case_path)))    # case_path:testcases\debug\mysql      type(case_path):<class 'pathlib.WindowsPath'>


class TestApi:  # 声明可以被pytest识别的测试类
    @classmethod
    def find_yaml_case(cls, path: Path = case_path):
        """
        加载yaml用例
        :return:
        """
        yaml_case_list = path.glob("**/test_*.yaml")
        for yaml_path in yaml_case_list:
            logger.info(f"load file {yaml_path=}")
            file = YamlFile(yaml_path)  # 读取yaml文件
            # print(file, type(file), "kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
            # print(json.dumps(dict(file), sort_keys=False, indent=4, separators=(',', ': ')).encode("utf-8").decode(
            #     "unicode_escape"))

            case_info = CaseInfo(**file)  # 验证yaml用例
            print(case_info)

            case_func = cls.new_case(case_info)  # 转为pytest用例
            logger.info(case_func)
            # setattr函数的作用是给对象设置属性值,这样做的目的是将生成的pytest用例与类关联起来，可以在运行测试时通过类名来调用这些用例函数。
            setattr(cls, f"{yaml_path.name}", case_func)  # 添加到类中

    @classmethod
    def new_case(cls, case_info: CaseInfo):
        """
        实例化用例
        :param case_info:
        :return:
        """

        ddt_data = list(case_info.ddt())
        ddt_title = [data.title for data in ddt_data]

        # 这是pytest原生支持的参数化用法，必须要是Python代码，其底层实现非常复杂
        @pytest.mark.parametrize("case_info", ddt_data, ids=ddt_title)
        def test_func(self, case_info: CaseInfo, request: pytest.FixtureRequest, set_global_data, doctest_namespace):
            """
                在pytest中，默认情况下，使用request作为参数名称可以自动传递pytest.FixtureRequest对象
            """
            # print("用例是否需要fixture", case_info.fixture_code)
            # yaml中的fixture名字已进入pytest
            # case_info  是yaml里的内容，是在原生参数化执行之后，得到的结果
            # case_info 便不能再次使用参数化，因为pytest不允许参数化里参数化
            fixture_value = {}  # fixture返回值

            for fixture_name in case_info.fixture_code:
                fixture_value[fixture_name] = request.getfixturevalue(fixture_name)  # 动态调用fixture
                # exchanger.replace(case_info.fixture_code)

            logger.info(fixture_value)
            logger.info("uuuuuuuuuuuuu")

            # fixture 'init_module' not found  说明pytest试图调用fixture了
            # 不报错，说明调用fixture成功

            exchanger.file.update(fixture_value)
            allure.dynamic.epic(case_info.epic)
            allure.dynamic.feature(case_info.feature)
            allure.dynamic.story(case_info.story)
            allure.dynamic.title(case_info.title)

            logger.info(f"用例开始执行: {case_info.title}".center(80, "="))

            # 0. 变量替换
            case_info.request = exchanger.replace(case_info.request)
            logger.info("1. 正在注入变量...")
            logger.debug(f"{exchanger.file}")

            # 1. 发送请求
            logger.info("2. 正在请求接口...")
            resp = session.request(**case_info.request)
            set_global_data("response", resp.json())

            logger.info("3. 正在提取变量...")
            # 2. 保存变量（接口关联）
            for var_name, extract_info in case_info.extract.items():
                # logger.info(var_name)
                # logger.info("kkkkkkkkkkkkkkkkkkkkkkkkk")
                # logger.info(extract_info)
                exchanger.extract(resp, var_name, *extract_info)

            # 3. 断言
            logger.info("4. 正在断言...")
            case_info.validate = exchanger.replace(
                case_info.validate)  # 只为断言加载变量
            case_info.assert_all()  # 执行断言

            logger.info(f"用例执行结束: {case_info.title}".center(80, "="))

            # 4. 结果检查
            if case_info.post_function:
                logger.warning('\033[95m准备进行结果检查......\033[0m')
                post_function = getattr(funcs, case_info.post_function)

                is_ok = post_function(exchanger)
                # logger.info(f'post_function（{case_info.post_function}）返回值为: {is_ok}')
                logger.info('\033[95m' + f'post_function({case_info.post_function})返回值为: {is_ok}' + '\033[0m')
                if not is_ok:
                    # 结束本线程后续用例
                    self_id = get_xdist_worker_id(request)
                    doctest_namespace['stop_id'] = self_id

                    logger.error('用例执行结果：失败！')
                    assert False  # 本次用例宣布失败

        return test_func


if __name__ == '__main__':
    print(session.base_url)
    print(exchanger.file, 11)
    print(case_path)
    print(TestApi.find_yaml_case(Path(r"E:/Program Files (x86)/JetBrains/PyCharm 2021.1.3/workspace/api_framework/testcases/debug/mysql/")))
