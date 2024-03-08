from pathlib import Path

import datetime
import os
import shutil

import pytest

from commons.cases import TestApi


# TestApi.find_yaml_case()  # 搜集yaml

class TestLinuxMysql5_5CDM(TestApi):  # 每个类1个线程
    ...


class TestLinuxMysql8_0_34CDM(TestApi):  # 每个类1个线程
    ...


class TestOracleCDMSingleMachine(TestApi):  # 两个类2个线程
    ...


# TestMysqlCDM.find_yaml_case(Path(r'testcases/ddt/aaa'))  # 加载本线程要执行的用例
# TestOracleCDMSingleMachine.find_yaml_case(Path(r'testcases/ddt/bbb'))


TestLinuxMysql5_5CDM.find_yaml_case(Path(r'testcases/debug/mysql/mysql_cdm/linux7_mysql8.0.24_cdm'))  # 加载本线程要执行的用例
# TestLinuxMysql8_0_34CDM.find_yaml_case(Path(r'testcases/debug/mysql/mysql_cdm/linux_mysql8.0.34_cdm'))
# TestOracleCDMSingleMachine.find_yaml_case(Path(r'testcases/debug/oracle/oracleCDM单节点'))

if __name__ == "__main__":
    pytest.main(  # 执行用例
        [
            __file__,
            f"--rootdir={os.getcwd()}",
            f"-c={os.getcwd()}/pytest.ini",
        ]
    )

    os.system("allure generate temp -o report --clean")  # 生成报告
    # 保存日志
    # now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    # shutil.move("logs/pytest.log", f"logs/{now}.log")
    Path("logs/pytest.log").unlink(True)
