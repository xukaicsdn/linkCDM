import logging
import warnings
import urllib3
import allure
import requests
from requests import PreparedRequest, Response

from commons import settings
from commons.files import YamlFile


logger = logging.getLogger("requests.session")


class Session(requests.Session):
    """
    三木的封装：
    1. 支持BaseURL
    2. 支持日志记录
    """

    extract = YamlFile(settings.extract_path)  # 持久化保存变量

    def __init__(self, base_url=""):
        urllib3.disable_warnings()
        warnings.simplefilter('ignore', ResourceWarning)
        super().__init__()  # 先按原有的方式完成实例化
        self.base_url = base_url  # 再按新的方式完成  【额外操作】

    @allure.step("请求接口")
    def request(self, method, url, *args, **kwargs):
        if not url.startswith("http"):  # 如果url不是以HTTP开头
            # 就自动添加baseurl
            url = self.base_url + url
        # file
        files = kwargs.pop("files", {})
        if files:
            for k, v in files:
                files[k] = open(v)

            kwargs["files"] = files

        return super().request(method, url, verify=False, *args, **kwargs)  # 按照原有方式执行

    def send(self, request: PreparedRequest, *args, **kwargs) -> Response:
        """
        send方法是对requests.Session类中的send方法进行了重写
        这里的super().request会调用父类requests.Session中的request方法，而父类中的request方法会调用send方法来发送请求。因此，即使在您的代码中没有直接调用send方法，但在执行请求时仍会经过该方法
        """
        logger.info(f"发送请求>>>>>> 接口地址 = {request.method} {request.url}")
        logger.info(f"发送请求>>>>>> 请求头 = {request.headers}")
        logger.info(f"发送请求>>>>>> 请求正文 = {request.body}")

        response = super().send(request, **kwargs)  # 按原有的方式发送请求

        logger.info(f"接收响应      <<<<<< 状态码 = {response.status_code}")
        logger.info(f"接收响应      <<<<<< 响应头 = {response.headers}")
        logger.info(f"接收响应      <<<<<< 响应正文 = {response.content.decode('utf-8')}")

        return response


# if __name__ == '__main__':
#     session = Session(base_url="https://192.168.2.130:9090")
#
#     body = {
#         "method": "POST",
#         "url": "/api/admin.v1.User/Login",
#         "json": {
#             "username": "xpp",
#             "password": "U0c5M2JHbHVhMEF4TkRBeA=="
#         }
#     }
#     aaa = session.request(**body, verify=False)
#
#     print(aaa.json())
#
#     # 或者
#     params = {"username": "poi", "password": "U0c5M2JHbHVhMEF4TkRBeA=="}
#     aaa = session.request(method="post", url="/api/admin.v1.User/Login",
#                           params=params)
#     print(aaa.json())
#
#     session = Session()
#     url = "http://192.168.2.130:9090/api/admin.v1.User/Login"
#     params = {"username": "poi", "password": "U0c5M2JHbHVhMEF4TkRBeA=="}
#     request = requests.Request(method="POST", url=url, params=params)
#     prepped_request = session.prepare_request(request)
#     response = session.send(prepped_request)
#
#     # 打印响应信息
#     print(f"状态码: {response.status_code}")
#     print(f"响应头: {response.headers}")
#     print(f"响应内容: {response.content.decode('utf-8')}")
