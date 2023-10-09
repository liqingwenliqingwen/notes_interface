import time
import unittest

import requests

from common.AES_tool import encry
from common.checkResult import CheckResult


class GetNoteInGroupTest(unittest.TestCase):
    """
    查看分组下便签
    1，新增分组
    2，新增便签主体
    3，新增便签内容
    4，查看分组下便签
    """
    add_note_group_path = '/v3/notesvr/set/notegroup'
    out_put_result = CheckResult()
    host = 'http://note-api.wps.cn'
    note_content_path = '/v3/notesvr/set/notecontent'
    note_info = '/v3/notesvr/set/noteinfo'
    get_note_in_group = '/v3/notesvr/web/getnotes/group'
    headers = {
        'cookie': 'wps_sid=V02SzZhvW5p4R-F9xWxYg1FnX3fb6XI00a6c5883000e1f8b95',
        'X-user-key': '236948373',
        'Content-Type': 'application/json'
    }

    key = 'H9n&S@oGohGpV6d7'.encode('utf-8')
    iv = '5150956153345366'.encode('utf-8')

    def test_01_get_note_in_group_major(self):
        """1，新增分组"""
        group_id = str(int(time.time() * 1000)) + '_group_id'
        body = {
            'groupId': group_id,
            'groupName': '新建分组1',
            'order': 1,
        }
        print("新增的分组id(请求body中的)为{}".format(body['groupId']))
        res = requests.post(url=self.host + self.add_note_group_path, headers=self.headers, json=body)
        # print(res.json())

        """2,在分组下新增便签主体"""

        note_id = str(int(time.time() * 1000)) + '_noteId'
        body = {
            'noteId': note_id,
            'star': 0,
            'groupId': group_id

        }
        print('新建便签主体请求的分组为{}，新建分组下(body)的便签id为{}'.format(body['groupId'], body['noteId']))
        res = requests.post(url=self.host + self.note_info, headers=self.headers, json=body)

        """3,新建便签内容"""
        contentVersion = res.json()['infoVersion']

        title = encry('恭喜', self.key, self.iv)
        summary = encry('恭喜发财', self.key, self.iv)
        text_body = encry('zzzzzzzzz', self.key, self.iv)
        body = {
            'noteId': note_id,
            'title': title,
            'summary': summary,
            'body': text_body,
            'localContentVersion': contentVersion,
            'BodyType': 0

        }

        update_note_result = requests.post(url=self.host + self.note_content_path, headers=self.headers, json=body)
        print(update_note_result.json())

        """4，查看分组下便签"""
        body = {
            'groupId': group_id

        }
        print('查看分组下的便签分组名字为{}'.format(body['groupId']))
        note_in_Group = requests.post(url=self.host + self.get_note_in_group, headers=self.headers, json=body)
        print(note_in_Group.json())
