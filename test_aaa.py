#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @project : API_Service
# @File    : test_1.py
# @Date    : 2021/6/15 3:07 下午
# @Author  : 李文良


# demo：
import pytest

def test_01():
    print('测试用例1操作')

def test_02():
    print('测试用例2操作')

def test_03():
    print('测试用例3操作')

def test_04():
    print('测试用例4操作')


def test_05():
    print('测试用例5操作')


def test_06():
    print('测试用例6操作')


def test_07():
    print('测试用例7操作')


def test_08():
    print('测试用例8操作')

if __name__ == "__main__":
    pytest.main(["-s", "test_aaa.py", '--tests-per-worker=4'])

