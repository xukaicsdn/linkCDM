"""
@Filename:   commons/templates
@Author:      三木
@Time:        2023/1/26 15:51
@Describe:    ...
"""
import pdb
import re
import string


def _str(s):
    return f"'{s}'"


class Template(string.Template):
    """
    三木的封装
    1. 支持函数调用
    2. 支持参数使用变量
    """

    func_mapping = {
        "str": _str,
    }  # 定义类变量，存储可用的函数名和对应的函数对象

    # 定义正则表达式，用于匹配 ${func_name(func_args)} 格式的字符串
    call_pattern = re.compile(r"\${(?P<func_name>[^()]+)\((?P<func_args>.*?)\)}")

    def render(self, mapping: dict) -> str:
        """
        重写render方法，支持变量和函数的替换
        :param mapping: 变量和函数的上下文
        :return: 替换后的字符串
        """
        s = self.safe_substitute(mapping)  # 原有方法替换变量
        s = self.safe_substitute_funcs(s, mapping)  # 新方法替换函数结果
        print(s)
        return s

    def safe_substitute_funcs(self, template, mapping) -> str:
        """
        解析字符串中的函数名和参数，并将函数调用结果进行替换
        :param template: 字符串
        :param mapping: 上下文，提供要使用的函数和变量
        :return: 替换后的结果
        """
        mapping = dict(mapping)
        mapping.update(self.func_mapping)

        def convert(mo):
            """
            匹配到的 ${func_name(func_args)} 字符串会通过该方法进行处理
            :param mo: 匹配到的字符串
            :return: 替换后的结果
            """
            func_name = mo.group("func_name")
            func_args = mo.group("func_args")

            # 解析参数中的嵌套函数调用
            while True:
                nested_call = self.call_pattern.search(func_args)
                if nested_call:
                    nested_result = convert(nested_call)
                    func_args = func_args[:nested_call.start()] + nested_result + func_args[nested_call.end():]
                else:
                    break

            func_args = func_args.split(",")
            if func_args == [""]:
                func_args = []

            func = mapping.get(func_name)  # 读取指定函数
            func_args_value = [
                mapping.get(arg.strip(), arg.strip()) for arg in func_args
            ]

            if not callable(func):
                return mo.group()  # 如果是不可调用的假函数，不进行替换
            else:
                return str(func(*func_args_value))  # 否则用函数结果进行替换

        return self.call_pattern.sub(convert, template)


# 相当于jmeter中得函数助手
def load_funcs():
    from commons import funcs

    for func_name in dir(funcs):
        # print("func_name:", func_name)
        # print("funcs:", funcs)

        if func_name.startswith("__"):
            continue

        func = getattr(funcs, func_name)

        if not callable(func):
            continue

        Template.func_mapping[func_name] = func


load_funcs()

if __name__ == '__main__':
    # "我${age}，${name}，${time()}"替换成yaml得字符串格式
    Template("我${age}，${name}，${generate_random_str(1)}").render({"age": 6, "name": "先看"})
    Template("我${age}，${name}，${time()}").render({"age": 6, "name": "先看"})
    Template("我${age}，${name}，${mail()}").render({"age": 6, "name": "先看"})
    Template("${mysql_${version()}_backup()}").render({})
    Template("${generate_random_str(1)}").render({})
    import re

    def fun2(a):
        var = a
        return var


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


    def replace_function_calls(string):
        pattern = r"\${([^{}]+)}"
        match = re.search(pattern, string)
        if match:
            function_call = match.group(1)
            result = eval(function_call)
            new_string = string[:match.start()] + str(result) + string[match.end():]
            return replace_function_calls(new_string)
        else:
            return string


    string = "${generate_random_str(${fun2(5)})}"
    result = replace_function_calls(string)
    print(result)
