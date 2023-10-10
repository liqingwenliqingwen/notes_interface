import time
import unittest

from parameterized import parameterized

from business.apiRequest import ApiRequests
from business.generateNote import GenerateNote
from business.wipeNote import WipeNote
from common.caseLog import step, class_case_log
from common.checkResult import CheckResult
from common.yamlOperator import YamlOperator


@class_case_log
class TestCaseSetNoteGroupInput(unittest.TestCase):
    apiRequests = ApiRequests()
    wipeNote = WipeNote()
    generateNote = GenerateNote()
    outPutResult = CheckResult()
    envConfig = YamlOperator().env_config()
    setNoteGroupConfig = YamlOperator.api_data_config('setNoteGroup')
    host = envConfig['host']
    userId = envConfig['user_id']
    sid = envConfig['sid']
    notPresentSid = envConfig['notPresentSid']
    setNoteGroupPath = setNoteGroupConfig['setNoteGroupPath']
    getNoteGroupPath = setNoteGroupConfig['getNoteGroupPath']

    key = envConfig['key'].encode('utf-8')
    iv = envConfig['iv'].encode('utf-8')

    def setUp(self) -> None:
        """清除数据"""
        self.wipeNote.wipeNote(self.userId, self.sid)

    groupId = [
        (None,),
        ('',)
    ]

    @parameterized.expand(groupId)
    def testCase_01(self, param):
        """新增便签数据冒烟"""
        step('STEP1:新增一个分组便签')
        groupId = str(int(time.time() * 1000)) + '_groupId'
        body = {
            'groupId': param,
            'groupName': '新增分组' + groupId,
            'order': 0
        }
        res = self.apiRequests.note_post(self.host + self.setNoteGroupPath, self.userId, self.sid, body)
        self.assertEqual(500, res.status_code)
        expected = {'errorCode': -7, 'errorMsg': '参数不合法！'}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_02(self):
        """删除groupId key"""
        step('STEP1:新增一个分组便签')
        groupId = str(int(time.time() * 1000)) + '_groupId'
        body = {
            'groupId': groupId,
            'groupName': '新增分组' + groupId,
            'order': 0
        }
        body.pop('groupId')
        res = self.apiRequests.note_post(self.host + self.setNoteGroupPath, self.userId, self.sid, body)
        self.assertEqual(500, res.status_code)
        expected = {'errorCode': -7, 'errorMsg': '参数不合法！'}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    group_contains_chinese = ['999999999999999999999999999999999999999999999999999999999999999999']

    @parameterized.expand(group_contains_chinese)
    def testCase_03(self, param):
        """group超长1，99999999 """
        step('STEP1:新增一个分组便签')
        groupId = str(int(time.time() * 1000)) + '_groupId'
        body = {
            'groupId': param,
            'groupName': '新增分组' + groupId,
            'order': 0
        }

        res = self.apiRequests.note_post(self.host + self.setNoteGroupPath, self.userId, self.sid, body)
        self.assertEqual(500, res.status_code)
        expected = {'errorCode': -7, 'errorMsg': '参数不合法！'}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_04(self):
        """group包括中文"""
        step('STEP1:新增一个分组便签')
        groupId = str(int(time.time() * 1000)) + '_groupId'
        body = {
            'groupId': '你好',
            'groupName': '新增分组' + groupId,
            'order': 0
        }

        res = self.apiRequests.note_post(self.host + self.setNoteGroupPath, self.userId, self.sid, body)
        self.assertEqual(200, res.status_code)
        expected = {'responseTime': int, 'updateTime': int}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    must_key_groupName = [
        (None,),
        ('',)
    ]

    @parameterized.expand(must_key_groupName)
    def testCase_05(self, param):
        """groupName包括1,None 2，‘’"""
        step('STEP1:新增一个分组便签')
        groupId = str(int(time.time() * 1000)) + '_groupId'
        body = {
            'groupId': groupId,
            'groupName': param,
            'order': 0
        }

        res = self.apiRequests.note_post(self.host + self.setNoteGroupPath, self.userId, self.sid, body)
        self.assertEqual(500, res.status_code)
        expected = {'errorCode': -7, 'errorMsg': '参数不合法！'}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_06(self):
        """groupName删除key‘’"""
        step('STEP1:新增一个分组便签')
        groupId = str(int(time.time() * 1000)) + '_groupId'
        body = {
            'groupId': groupId,
            'groupName': '新增分组' + groupId,
            'order': 0
        }
        body.pop('groupName')
        res = self.apiRequests.note_post(self.host + self.setNoteGroupPath, self.userId, self.sid, body)
        self.assertEqual(500, res.status_code)
        expected = {'errorCode': -7, 'errorMsg': '参数不合法！'}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    groupName = ['1@!!!',
                 '99999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999']

    @parameterized.expand(groupName)
    def testCase_07(self, param):
        """groupName删除key‘’"""
        step('STEP1:新增一个分组便签')
        groupId = str(int(time.time() * 1000)) + '_groupId'
        body = {
            'groupId': groupId,
            'groupName': param,
            'order': 0
        }
        res = self.apiRequests.note_post(self.host + self.setNoteGroupPath, self.userId, self.sid, body)
        self.assertEqual(200, res.status_code)

    order = [0, 1.5]

    @parameterized.expand(order)
    def testCase_08(self, param):
        """groupName删除key‘’"""
        step('STEP1:新增一个分组便签')
        groupId = str(int(time.time() * 1000)) + '_groupId'
        body = {
            'groupId': groupId,
            'groupName': '新增分组' + groupId,
            'order': param
        }
        res = self.apiRequests.note_post(self.host + self.setNoteGroupPath, self.userId, self.sid, body)
        self.assertEqual(200, res.status_code)

    order_str = ['1', "1"]

    @parameterized.expand(order_str)
    def testCase_09(self, param):
        """groupName删除key‘’"""
        step('STEP1:新增一个分组便签')
        groupId = str(int(time.time() * 1000)) + '_groupId'
        body = {
            'groupId': groupId,
            'groupName': '新增分组' + groupId,
            'order': param
        }
        res = self.apiRequests.note_post(self.host + self.setNoteGroupPath, self.userId, self.sid, body)
        self.assertEqual(200, res.status_code)

    order = [2147483648, -2147483649]

    @parameterized.expand(order)
    def testCase_10(self, param):
        """order删除key‘’"""
        step('STEP1:新增一个分组便签')
        groupId = str(int(time.time() * 1000)) + '_groupId'
        body = {
            'groupId': groupId,
            'groupName': '新增分组' + groupId,
            'order': param
        }
        body.pop('order')
        res = self.apiRequests.note_post(self.host + self.setNoteGroupPath, self.userId, self.sid, body)
        self.assertEqual(200, res.status_code)

    def testCase_11(self):
        """身份校验-不存在的sid‘’"""
        step('STEP1:新增一个分组便签')
        groupId = str(int(time.time() * 1000)) + '_groupId'
        body = {
            'groupId': groupId,
            'groupName': '新增分组' + groupId,
            'order': 0
        }
        res = self.apiRequests.note_post(self.host + self.setNoteGroupPath, self.userId, self.notPresentSid, body)
        self.assertEqual(401, res.status_code)
        expected = {'errorCode': -2010, 'errorMsg': ''}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_12(self):
        """身份校验-删除cookie‘’"""
        step('STEP1:新增一个分组便签')
        groupId = str(int(time.time() * 1000)) + '_groupId'
        body = {
            'groupId': groupId,
            'groupName': '新增分组' + groupId,
            'order': 0
        }
        new_header = {
            'Content-Type': 'application/json',
            'X-user-key': str(self.userId),
            'Cookie': f'wps_sid={self.sid}'
        }
        new_header.pop('Cookie')
        res = self.apiRequests.note_post(self.host + self.setNoteGroupPath, self.userId, self.sid, body,
                                         new_header)
        self.assertEqual(401, res.status_code)
        expected = {'errorCode': -2009, 'errorMsg': ''}
        self.outPutResult.check_out(expected=expected, actual=res.json())
