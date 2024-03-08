import base64
import hashlib
import logging
import urllib.parse
from commons.databases import PostgresHandler

import rsa

from commons import settings


def url_unquote(s: str) -> str:
    return urllib.parse.unquote(s)


def time():
    import time

    return time.time()



def sleep(x):
    import time

    time.sleep(float(x))

    return x


def sql(sql: str, *args):
    from commons.databases import db
    sql = sql % args
    logging.debug(f"{sql=}")
    res = db.execute_sql(sql)

    return res[0]


def md5(content):
    content = str(content).encode("utf-8")
    md5_value = hashlib.md5(content).hexdigest()
    return md5_value


def base64_encode(content):
    content = str(content).encode("utf-8")  # 转二进制
    base64_value = base64.b64encode(content).decode(encoding="utf-8")  # 转字符串
    return base64_value


def base64_decode(content):
    base64_value = base64.b64decode(content).decode(encoding="utf-8")  # 转字符串
    return base64_value


def rsa_encode(content):
    content = str(content).encode("utf-8")  # 转二进制

    with open(settings.rsa_public) as f:
        pubkey = rsa.PublicKey.load_pkcs1(f.read().encode())  # 加载密钥

    ras_value = rsa.encrypt(content, pubkey)  # 得到二进制数据
    base64_value = base64.b64encode(ras_value).decode(encoding="utf-8")  # 转字符串
    return base64_value


def rsa_decode(content):
    content = base64.b64decode(content)

    with open(settings.rsa_private) as f:
        priv_key = rsa.PrivateKey.load_pkcs1(f.read().encode())  # 加载密钥

    ras_value = rsa.decrypt(content, priv_key)  # 得到二进制数据

    return ras_value.decode()  # 转字符串


def add(content, num):
    return int(content) + int(num)


def generate_random_str(randomlength: int):
    """
        生成一个指定长度的随机字符串
    """
    import random
    random_str = ''
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz'
    length = len(base_str) - 1
    for i in range(int(randomlength)):
        random_str += base_str[random.randint(0, length)]
    return random_str


def phone():
    """
    return: str
    """
    from faker import Faker
    fk = Faker(locale="zh_CN")
    phone = fk.phone_number()
    return phone


def mail():
    """
    return: str
    """
    from faker import Faker
    fk = Faker(locale="zh_CN")
    phone = fk.phone_number()
    return f"{phone}@163.com"


def fun2(a):
    var = a
    return var


def base64_b64encode(password):
    """
        base64两次加密
    """
    import base64
    password = password
    encoded_password_1 = base64.b64encode(password.encode("utf-8")).decode("utf-8")
    encoded_password_2 = base64.b64encode(encoded_password_1.encode("utf-8")).decode("utf-8")
    return str(encoded_password_2)


def base64_b64decode(encoded_password="U0c5M2JHbHVhMEF4TkRBeA=="):
    """
        base64两次解密
    """
    import base64
    encoded_password = encoded_password
    decoded_password_1 = base64.b64decode(encoded_password).decode("utf-8")
    decoded_password_2 = base64.b64decode(decoded_password_1).decode("utf-8")
    return decoded_password_2


def check_http_ok(exchanger):  # 函数必须接收参数
    """
    函数返回True 表示检查通过，继续执行期用例
    函数返回False 表示检查失败，不再执行本线程其他用例
    """
    # 从变量中取值。如果需要什么变量，在yaml的extract进行定义
    code = exchanger.file['code']

    # 对变量进行任意的判断

    if code == '200':
        return True  # 检查成功，本用例通过，其他用例继续执行
    else:
        return False  # 检查失败，本用例不通过，其他用例放弃执行


# 在这个文件中定义函数，完成检查
def check_create_ok(exchanger):  # 参数是固定的
    import time
    # if 1 == 1:  # todo 补充判断逻辑  ，先模拟判断成功
    create_strategy_event_id = exchanger.file['create_strategy_event_id']
    postgres_handler = PostgresHandler("192.168.2.130", "postgres", "postgres", "123")

    state = 1
    while state == 1:  # todo 补充判断逻辑  ，先模拟判断成功，if 1 == 2模拟失败是否能跳过
        sql = f"""
            SELECT state
            FROM public."event"
            WHERE id={create_strategy_event_id};
        """
        logging.warning(f"{sql=}")
        query_result = postgres_handler.execute_query(sql)

        for row in query_result:
            # 使用字段名访问值
            state = row.state  # 替换为你的实际字段名
            logging.warning(f"{state=}")
            time.sleep(20)
        if state == 2:
            return True
    return False


# ---------------------------------------------------------------------------------------------
# 全局数据字典，作为数据源
data_dict = {
    "linux7_mysql8_0_cdm": [
        {"ip": "192.168.2.44", "port": 3306, "username": "root", "password": base64_b64encode("Howlink@1401")},
        {"ip": "192.168.2.12", "port": 3306, "username": "root", "password": "Howlink@1401"}
    ],
    "linux7_mysql5_0_cdm": [
        {"ip": "192.168.2.14", "port": 3306, "username": "root", "password": base64_b64encode("Howlink@1401")},
        {"ip": "192.168.2.12", "port": 3306, "username": "root", "password": "Howlink@1401"}
    ]
}


def get_param_value(group_name, index, param_name):
    if group_name in data_dict:
        group_variables = data_dict[group_name]
        if int(index) < len(group_variables):
            return group_variables[int(index)].get(param_name)
    return None


if __name__ == '__main__':
    # 示例用法，无需传递数据字典
    port_value = get_param_value("linux7_mysql8_0_cdm", 0, "password")
    port_value1 = get_param_value("linux7_mysql5_0_cdm", 0, "ip")
    port_value2 = get_param_value("linux7_mysql8_0_cdm", 0, "port")
    print(port_value, port_value1, port_value2)  # 输出 3306
    # ---------------------------------------------------------------------------------------------

    print(base64_b64encode("Howlink@1024"))
    print(base64_b64encode("Howlink@1401"))
    print(base64_b64decode("U0c5M2JHbHVhMEF4TkRBeA=="))
