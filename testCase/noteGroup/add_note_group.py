import time
import unittest

import requests

from common.checkResult import CheckResult


class AddNoteGroupTest(unittest.TestCase):
    """
    添加分组主流程
    """
    out_put_result = CheckResult()
    host = 'http://note-api.wps.cn'
    add_note_group_path = '/v3/notesvr/set/notegroup'
    headers = {
        'cookie': 'wps_sid=V02SzZhvW5p4R-F9xWxYg1FnX3fb6XI00a6c5883000e1f8b95',
        'Content-Type': 'application/json',
        'X-user-key': '236948373'
    }
    key = 'H9n&S@oGohGpV6d7'.encode('utf-8')
    iv = '5150956153345366'.encode('utf-8')

    def test_01_add_note_group_major(self):
        group_id = str(int(time.time() * 1000)) + '_group_id'
        body = {
            'groupId': group_id,
            'groupName': '新建分组1',
            'order': 1,
        }
        res = requests.post(url=self.host + self.add_note_group_path, headers=self.headers, json=body)
        self.assertEqual(200, res.status_code)
        expected = {
            'responseTime': int,
            'updateTime': int
        }
        self.out_put_result.check_out(expected=expected, actual=res.json())
