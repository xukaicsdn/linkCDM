import datetime

from pathlib import Path

import logging
import pytest
import os

from xdist import get_xdist_worker_id
from commons.databases import PostgresHandler


def pytest_configure(config):
    _id = os.environ.get("PYTEST_XDIST_WORKER")
    now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    if _id is not None:
        path = Path(config.getini("log_file"))

        file = open(str(path.with_name(f"{now}_{_id}_{path.name}")), "w", encoding="utf-8")

        logging.basicConfig(
            stream=file,
            level=getattr(logging, config.getini("log_file_level").upper()),
            format=config.getini("log_file_format"),
        )


@pytest.fixture(autouse=True)
def check_woker_id(request, doctest_namespace):
    self_id = get_xdist_worker_id(request)
    if doctest_namespace.get('stop_id') == self_id:
        pytest.skip('停止线程')


# -----------------------------------------------------------------------------------------------------
# 定义一个全局变量，用于存储内容
global_data = {}


@pytest.fixture(scope='function')
def set_global_data(get_global_data):
    """
        设置全局变量，用于关联参数
        参考：https://blog.csdn.net/xjian32123/article/details/122134248
        :return:
    """
    print("这是测试方法set_global_data的前置")

    def _set_global_data(key, value):
        global_data[key] = value

    yield _set_global_data
    print("这是set_global_data测试方法的后置")
    # print(global_data, "----------------------------------------------------")
    res = get_global_data("response")
    print(res)


@pytest.fixture(scope='function')
def get_global_data():
    """
        从全局变量global_data中取值
        参考：https://blog.csdn.net/xjian32123/article/details/122134248
        :return:
    """

    def _get_global_data(key):
        return global_data.get(key)

    yield _get_global_data
# -----------------------------------------------------------------------------------------------------


@pytest.fixture(scope='session')
def init_session():
    print("这是测试会话的前置")
    yield
    print("这是测试会话的后置")


@pytest.fixture(scope='module')
def init_module():
    print("这是测试模块的前置")
    yield
    print("这是测试模块的后置")


@pytest.fixture(scope='class')
def init_class():
    print("这是测试类的前置")
    a = 777
    yield a  # 如果fixture返回值要传递给用例
    print("这是测试类的后置")


@pytest.fixture(scope='function')
def init_function(sql=f"""
        SELECT id, ip_addr, app_kinds, os, os_version, "version", iqn
        FROM public.lblet
        WHERE ip_addr='192.168.2.44';
        """):
    print("这是测试方法的前置")
    postgres_handler = PostgresHandler("192.168.2.130", "postgres", "postgres", "123")
    logging.warning(f"{sql=}")
    query_result = postgres_handler.execute_query(sql)
    id, ip_addr, os, os_version, version, iqn = None, None, None, None, None, None
    for row in query_result:
        # 使用字段名访问值
        id = row.id  # 替换为你的实际字段名
        logging.warning(f"{id=}")
        ip_addr = row.ip_addr
        logging.warning(f"{ip_addr=}")
        os = row.os
        logging.warning(f"{os=}")
        os_version = row.os_version
        logging.warning(f"{os_version=}")
        version = row.version
        logging.warning(f"{version=}")
        iqn = row.iqn
        logging.warning(f"{iqn=}")
    a = 888
    yield id, ip_addr, os, os_version, version, iqn  # 如果fixture返回值要传递给用例
    print("这是测试方法的后置")
    logging.warning(f"{id}, {ip_addr}, {os}, {os_version}, {version}, {iqn}")


@pytest.fixture(scope='function')
def ffffff(request):
    # 这个函数的作用在于不用执行后置
    print("-------------ffffff在测试用例执行之前的操作---------------------")

    def setup():
        # 在测试用例执行之后的操作
        print("-------------ffffff在测试用例执行之后的操作---------------------")
        a = 666666666666
        print(f"--------------{a}-------------------------")
        return a

    request.addfinalizer(setup)  # 注册后置操作


@pytest.fixture(scope='function')
def gggg(request):
    print("-------------ffffff在测试用例执行之前的操作---------------------")
    def teardown():
        print("-------------ffffff在测试用例执行之后的操作---------------------")
        a = 666666666666
        print(f"--------------{a}-------------------------")
        yield a

    request.addfinalizer(teardown)  # 注册后置操作
    yield from teardown()


def test_a(init_function):
    print(999, init_function)


def test_b(gggg):
    print("执行测试用例")
    print(gggg)


if __name__ == '__main__':
    pytest.main(['-v', '-s',  __file__])