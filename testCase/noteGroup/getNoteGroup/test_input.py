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
class TestCaseGetNoteGroupInput(unittest.TestCase):
    apiRequests = ApiRequests()
    wipeNote = WipeNote()
    generateNote = GenerateNote()
    outPutResult = CheckResult()
    envConfig = YamlOperator().env_config()
    getNoteGroupConfig = YamlOperator.api_data_config('getNoteGroup')
    host = envConfig['host']
    userId = envConfig['user_id']
    sid = envConfig['sid']
    sidB = envConfig['sidB']
    notPresentSid = envConfig['notPresentSid']
    setNoteGroupPath = getNoteGroupConfig['setNoteGroupPath']
    getNoteGroupPath = getNoteGroupConfig['getNoteGroupPath']

    key = envConfig['key'].encode('utf-8')
    iv = envConfig['iv'].encode('utf-8')

    def setUp(self) -> None:
        """清除数据"""
        self.wipeNote.wipeNote(self.userId, self.sid)

    optional_excludeInvalid = [
        (None,),
        ('',)
    ]

    @parameterized.expand(optional_excludeInvalid)
    def testCase_01(self, param):
        """查询便签数据"""
        step('STEP1:新增一个分组便签')
        groupId = str(int(time.time() * 1000)) + '_groupId'
        body = {
            'groupId': groupId,
            'groupName': '新增分组' + groupId,
            'order': 0
        }
        self.apiRequests.note_post(self.host + self.setNoteGroupPath, self.userId, self.sid, body)
        step('STEP2:获取分组便签')
        body = {
            'excludeInvalid': param
        }
        res = self.apiRequests.note_post(self.host + self.getNoteGroupPath, self.userId, self.sid, body)
        self.assertEqual(200, res.status_code)

    optional_excludeInvalid_enum = [
        (True,),
        (False,)
    ]

    @parameterized.expand(optional_excludeInvalid_enum)
    def testCase_02(self, param):
        """查询便签数据"""
        step('STEP1:新增一个分组便签')
        groupId = str(int(time.time() * 1000)) + '_groupId'
        body = {
            'groupId': groupId,
            'groupName': '新增分组' + groupId,
            'order': 0
        }
        self.apiRequests.note_post(self.host + self.setNoteGroupPath, self.userId, self.sid, body)
        step('STEP2:获取分组便签')
        body = {
            'excludeInvalid': param
        }
        res = self.apiRequests.note_post(self.host + self.getNoteGroupPath, self.userId, self.sid, body)
        self.assertEqual(200, res.status_code)

    def testCase_03(self):
        """用户A查询用户B下的便签"""
        step('STEP1:新增一个分组便签')
        groupId = str(int(time.time() * 1000)) + '_groupId'
        body = {
            'groupId': groupId,
            'groupName': '新增分组' + groupId,
            'order': 0
        }
        self.apiRequests.note_post(self.host + self.setNoteGroupPath, self.userId, self.sid, body)
        step('STEP2:获取分组便签')
        body = {
            'excludeInvalid': True
        }
        res = self.apiRequests.note_post(self.host + self.getNoteGroupPath, self.userId, self.sidB, body)
        self.assertEqual(412, res.status_code)
        expected = {'errorCode': -1011, 'errorMsg': 'user change!'}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_04(self):
        """用户A查询用户B下的便签"""
        step('STEP1:新增一个分组便签')
        groupId = str(int(time.time() * 1000)) + '_groupId'
        body = {
            'groupId': groupId,
            'groupName': '新增分组' + groupId,
            'order': 0
        }
        self.apiRequests.note_post(self.host + self.setNoteGroupPath, self.userId, self.sid, body)
        step('STEP2:获取分组便签')
        body = {
            'excludeInvalid': True
        }
        res = self.apiRequests.note_post(self.host + self.getNoteGroupPath, self.userId, self.notPresentSid, body)
        self.assertEqual(401, res.status_code)
        expected = {'errorCode': -2010, 'errorMsg': ''}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_05(self):
        """用户A查询用户B下的便签"""
        step('STEP1:新增一个分组便签')
        groupId = str(int(time.time() * 1000)) + '_groupId'
        body = {
            'groupId': groupId,
            'groupName': '新增分组' + groupId,
            'order': 0
        }
        self.apiRequests.note_post(self.host + self.setNoteGroupPath, self.userId, self.sid, body)
        step('STEP2:获取分组便签')
        body = {
            'excludeInvalid': True
        }
        new_header = {
            'Content-type': 'application/json',
            'X-user-key': str(self.userId),
            'Cookie': f'wps_sid={self.sid}'
        }
        new_header.pop('Cookie')
        res = self.apiRequests.note_post(self.host + self.getNoteGroupPath, self.userId, self.sid, body, new_header)
        self.assertEqual(401, res.status_code)
        expected = {'errorCode': -2009, 'errorMsg': ''}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_06(self):
        """使用不存在的sid"""
        step('STEP1:新增一个分组便签')
        groupId = str(int(time.time() * 1000)) + '_groupId'
        body = {
            'groupId': groupId,
            'groupName': '新增分组' + groupId,
            'order': 0
        }
        self.apiRequests.note_post(self.host + self.setNoteGroupPath, self.userId, self.sid, body)
        step('STEP2:获取分组便签')
        body = {
            'excludeInvalid': True
        }
        res = self.apiRequests.note_post(self.host + self.getNoteGroupPath, self.userId, self.notPresentSid, body
                                         )
        self.assertEqual(401, res.status_code)
        expected = {'errorCode': -2010, 'errorMsg': ''}
        self.outPutResult.check_out(expected=expected, actual=res.json())
