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
class TestCaseDeleteNoteGroupInput(unittest.TestCase):
    apiRequests = ApiRequests()
    wipeNote = WipeNote()
    generateNote = GenerateNote()
    outPutResult = CheckResult()
    envConfig = YamlOperator().env_config()
    deleteNoteGroupConfig = YamlOperator.api_data_config('deleteNoteGroup')
    host = envConfig['host']
    userId = envConfig['user_id']
    sid = envConfig['sid']
    sidB = envConfig['sidB']
    notPresentSid = envConfig['notPresentSid']
    setNoteGroupPath = deleteNoteGroupConfig['addNoteGroupPath']
    getNoteGroupPath = deleteNoteGroupConfig['getNoteGroupPath']
    delNoteGroup = deleteNoteGroupConfig['delNoteGroup']

    key = envConfig['key'].encode('utf-8')
    iv = envConfig['iv'].encode('utf-8')

    def setUp(self) -> None:
        """清除数据"""
        self.wipeNote.wipeNote(self.userId, self.sid)

    must_key_Null = [
        (None,),
        ('',)
    ]

    @parameterized.expand(must_key_Null)
    def testCase_01(self, param):
        """删除分组便签-input 1,groupId ，输入None ,2输入空字符串"""
        step('STEP1:新增一个分组便签')
        groupId = str(int(time.time() * 1000)) + '_groupId'
        body = {
            'groupId': groupId,
            'groupName': '新增分组' + groupId,
            'order': 0
        }
        self.apiRequests.note_post(self.host + self.setNoteGroupPath, self.userId, self.sid, body)
        step('STEP2:删除分组便签')
        body = {
            'groupId': param
        }
        res = self.apiRequests.note_post(self.host + self.delNoteGroup, self.userId, self.sid, body)
        self.assertEqual(500, res.status_code)
        expected = {'errorCode': -7, 'errorMsg': '参数不合法！'}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_02(self):
        """删除分组便签-input 删除groupId的key"""
        step('STEP1:新增一个分组便签')
        groupId = str(int(time.time() * 1000)) + '_groupId'
        body = {
            'groupId': groupId,
            'groupName': '新增分组' + groupId,
            'order': 0
        }
        self.apiRequests.note_post(self.host + self.setNoteGroupPath, self.userId, self.sid, body)
        step('STEP2:删除分组便签')
        body = {
            'groupId': groupId
        }
        body.pop('groupId')
        res = self.apiRequests.note_post(self.host + self.delNoteGroup, self.userId, self.sid, body)
        self.assertEqual(500, res.status_code)
        expected = {'errorCode': -7, 'errorMsg': '参数不合法！'}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_03(self):
        """删除分组便签-input groupId,输入一个不存在的groupId"""
        step('STEP1:新增一个分组便签')
        groupId = str(int(time.time() * 1000)) + '_groupId'
        body = {
            'groupId': groupId,
            'groupName': '新增分组' + groupId,
            'order': 0
        }
        self.apiRequests.note_post(self.host + self.setNoteGroupPath, self.userId, self.sid, body)
        step('STEP2:删除分组便签')
        body = {
            'groupId': 'qwqwqwq'
        }
        res = self.apiRequests.note_post(self.host + self.delNoteGroup, self.userId, self.sid, body)
        self.assertEqual(200, res.status_code)
        expected = {'responseTime': int}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    must_key_contains_chinese = ['你好',
                                 '999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999']

    @parameterized.expand(must_key_contains_chinese)
    def testCase_04(self, param):
        """删除分组便签-input groupId1，输入汉字 2，输入超长字符"""
        step('STEP1:新增一个分组便签')
        groupId = str(int(time.time() * 1000)) + '_groupId'
        body = {
            'groupId': groupId,
            'groupName': '新增分组' + groupId,
            'order': 0
        }
        self.apiRequests.note_post(self.host + self.setNoteGroupPath, self.userId, self.sid, body)
        step('STEP2:删除分组便签')
        body = {
            'groupId': param
        }
        res = self.apiRequests.note_post(self.host + self.delNoteGroup, self.userId, self.sid, body)
        self.assertEqual(500, res.status_code)
        expected = {'errorCode': -7, 'errorMsg': str}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    must_key_contains_str = ['@!%$&__', '12345' or '1=1']

    @parameterized.expand(must_key_contains_str)
    def testCase_05(self, param):
        """删除分组便签-input groupId 1，包含特殊字符 2，包括or 1=1"""
        step('STEP1:新增一个分组便签')
        groupId = str(int(time.time() * 1000)) + '_groupId'
        body = {
            'groupId': groupId,
            'groupName': '新增分组' + groupId,
            'order': 0
        }
        self.apiRequests.note_post(self.host + self.setNoteGroupPath, self.userId, self.sid, body)
        step('STEP2:删除分组便签')
        body = {
            'groupId': param
        }
        res = self.apiRequests.note_post(self.host + self.delNoteGroup, self.userId, self.sid, body)
        self.assertEqual(200, res.status_code)
        expected = {'responseTime': int}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_06(self):
        """身份校验，输入一个不存在的sid"""
        step('STEP1:新增一个分组便签')
        groupId = str(int(time.time() * 1000)) + '_groupId'
        body = {
            'groupId': groupId,
            'groupName': '新增分组' + groupId,
            'order': 0
        }
        self.apiRequests.note_post(self.host + self.setNoteGroupPath, self.userId, self.sid, body)
        step('STEP2:删除分组便签')
        body = {
            'groupId': groupId
        }
        res = self.apiRequests.note_post(self.host + self.delNoteGroup, self.userId, self.notPresentSid, body)
        self.assertEqual(401, res.status_code)
        expected = {'errorCode': -2010, 'errorMsg': ''}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_07(self):
        """删除wps_sid的key"""
        step('STEP1:新增一个分组便签')
        groupId = str(int(time.time() * 1000)) + '_groupId'
        body = {
            'groupId': groupId,
            'groupName': '新增分组' + groupId,
            'order': 0
        }
        self.apiRequests.note_post(self.host + self.setNoteGroupPath, self.userId, self.sid, body)
        step('STEP2:删除分组便签')
        body = {
            'groupId': groupId
        }
        new_header = {
            'Content-type': 'application/json',
            'X-user-key': str(self.userId),
            'Cookie': f'wps_sid={self.sid}'
        }
        new_header.pop('Cookie')
        res = self.apiRequests.note_post(self.host + self.delNoteGroup, self.userId, self.sid, body, new_header)
        self.assertEqual(401, res.status_code)
        expected = {'errorCode': -2009, 'errorMsg': ''}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_08(self):
        """用户A登录用户B"""
        step('STEP1:新增一个分组便签')
        groupId = str(int(time.time() * 1000)) + '_groupId'
        body = {
            'groupId': groupId,
            'groupName': '新增分组' + groupId,
            'order': 0
        }
        self.apiRequests.note_post(self.host + self.setNoteGroupPath, self.userId, self.sid, body)
        step('STEP2:删除分组便签')
        body = {
            'groupId': groupId
        }

        res = self.apiRequests.note_post(self.host + self.delNoteGroup, self.userId, self.sidB, body)
        self.assertEqual(412, res.status_code)
        expected = {'errorCode': -1011, 'errorMsg': 'user change!'}
        self.outPutResult.check_out(expected=expected, actual=res.json())
