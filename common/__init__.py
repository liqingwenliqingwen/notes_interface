import time
import requests
import unittest

from parameterized import parameterized

# 定义测试数据
star_abnormal = [
    [{'star': 1.5}],
    [{'star': "1"}],
    [{'star': '1'}],
    [{'star': ''}],
    [{'star': -1}]
]


# 定义测试函数
def test_03_star_abnormal(self, star):
    host = 'http://note-api.wps.cn'
    path = '/v3/notesvr/set/noteinfo'
    headers = {
        'cookie': 'wps_sid=V02SzZhvW5p4R-F9xWxYg1FnX3fb6XI00a6c5883000e1f8b95',
        'X-user-key': '236948373',
        'Content-Type': 'application/json'
    }
    """
    校验参数star
    """
    # 从self.body中获取数据
    note_id = self.body['noteId']

    # 发送POST请求，并断言响应的状态码为500
    abnormal_result = requests.post(url=self.host + self.path, headers=self.headers, json=star)
    self.assertEqual(500, abnormal_result.status_code, msg='状态码异常')
    # 其他断言或处理逻辑...


# 使用@parameterized.expand装饰器传递测试数据
@parameterized.expand(star_abnormal)
class TestStarAbnormal(unittest.TestCase):
    host = 'http://note-api.wps.cn'
    path = '/v3/notesvr/set/noteinfo'
    headers = {
        'cookie': 'wps_sid=V02SzZhvW5p4R-F9xWxYg1FnX3fb6XI00a6c5883000e1f8b95',
        'X-user-key': '236948373',
        'Content-Type': 'application/json'
    }
    """
    测试校验异常情况
    """

    # 设置测试用例的body数据
    body = {
        'noteId': str(int(time.time() * 1000)) + '_noteId'
    }

    # 运行测试用例
    def test(self):
        test_03_star_abnormal(self, self.body)
