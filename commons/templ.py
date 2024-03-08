import re
import string


class TemplateWithFunctionCall(string.Template):
    func_mapping = {}  # 存储可用的函数名和对应的函数对象

    def __init__(self, template):
        super().__init__(template)
        self.pattern = re.compile(r"\${(?P<func_name>[^()]+)\((?P<func_args>.*?)\)}")

    def substitute(self, mapping):
        # 将函数映射添加到mapping中
        mapping.update(self.func_mapping)
        return super().substitute(mapping)

    def _convert_func_call(self, match, mapping):
        func_name = match.group("func_name")
        func_args = match.group("func_args")

        # 递归解析嵌套的函数调用
        while True:
            nested_call = self.pattern.search(func_args)
            if nested_call:
                nested_result = self._convert_func_call(nested_call, mapping)
                func_args = func_args[:nested_call.start()] + nested_result + func_args[nested_call.end():]
            else:
                break

        func_args = func_args.split(",")
        if func_args == [""]:
            func_args = []

        func = mapping.get(func_name)
        if not callable(func):
            return match.group()  # 非可调用函数直接返回原字符串
        else:
            func_args_value = [
                mapping.get(arg.strip(), arg.strip()) for arg in func_args
            ]
            return str(func(*func_args_value))  # 替换为函数调用的结果

    def safe_substitute(self, mapping):
        result = super().safe_substitute(mapping)
        return self.pattern.sub(lambda match: self._convert_func_call(match, mapping), result)


# 示例函数
def add(a, b):
    return a + b


def multiply(a, b):
    return a * b


# 创建TemplateWithFunctionCall对象
template = TemplateWithFunctionCall("${add(${multiply(2, 3)}, 4)}")
# 设置函数映射
template.func_mapping = {
    "add": add,
    "multiply": multiply
}
# 替换函数调用并输出结果
result = template.safe_substitute({})
print(result)
