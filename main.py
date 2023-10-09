# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.





# This is a sample Python script.
import os
import unittest
from datetime import datetime

from BeautifulReport import BeautifulReport

DIR = os.path.dirname(os.path.abspath(__file__))
ENVIRON = 'Online'


def run(test_suite):
    # 定义输出的文件位置和名字
    filename = "report.html"
    result = BeautifulReport(test_suite)
    result.report(filename='report\\' + filename, description='测试报告', report_dir='./')


if __name__ == '__main__':
    pattern = 'all'  # all：执行所有用例，smoking冒烟用例
    if pattern == 'all':
        suite = unittest.TestLoader().discover('./testCase', 'test_*.py')
    else:
        suite = unittest.TestLoader().discover('./testCase', 'test_smoking*.py')

    run(suite)
