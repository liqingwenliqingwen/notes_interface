import time
import unittest

import requests

from common.checkResult import CheckResult


class GetNoteGroupTest(unittest.TestCase):
    """
    获取分组
    1，新建便签分组
    2，获取便签分组
    """
    out_put_result = CheckResult()
    add_note_group_path = '/v3/notesvr/set/notegroup'
    host = 'http://note-api.wps.cn'
    get_note_group_path = '/v3/notesvr/get/notegroup'
    headers = {
        'cookie': 'wps_sid=V02SzZhvW5p4R-F9xWxYg1FnX3fb6XI00a6c5883000e1f8b95',
        'X-user-key': '236948373',
        'Content-Type': 'application/json'
    }
    key = 'H9n&S@oGohGpV6d7'.encode('utf-8')
    iv = '5150956153345366'.encode('utf-8')

    def test_01_get_note_group_major(self):
        # 1，新建分组
        group_id = str(int(time.time() * 1000)) + '_group_id'
        body = {
            'groupId': group_id,
            'groupName': '新建分组X',
            'order': 1,
        }
        """1，调用新建分组方法"""
        requests.post(url=self.host + self.add_note_group_path, headers=self.headers, json=body)

        body = {}

        """"2,调用获取分组方法"""
        get_note_group_res = requests.post(url=self.host + self.get_note_group_path, headers=self.headers, json=body)
        print(get_note_group_res.json())
        groupId = [item['groupId'] for item in get_note_group_res.json()['noteGroups']]
        print("所有的分组有{}".format(groupId))


