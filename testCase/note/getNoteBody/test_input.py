import unittest

from parameterized import parameterized

from business.apiRequest import ApiRequests
from business.generateNote import GenerateNote
from business.wipeNote import WipeNote
from common.caseLog import step, class_case_log
from common.checkResult import CheckResult
from common.yamlOperator import YamlOperator


@class_case_log
class TestCaseGetNoteBodyInput(unittest.TestCase):
    wipeNote = WipeNote()
    apiRequests = ApiRequests()
    outPutResult = CheckResult()
    generateNote = GenerateNote()
    envConfig = YamlOperator().env_config()
    getNoteBodyConfig = YamlOperator().api_data_config('getNoteBody')
    host = envConfig['host']
    sid = envConfig['sid']
    userId = envConfig['user_id']
    getNoteBody = getNoteBodyConfig['getNoteBody']
    notPresentSid = envConfig['notPresentSid']

    def setUp(self) -> None:
        """清除测试数据"""
        self.wipeNote.wipeNote(self.userId, self.sid)

    noteId_must_key_None = ([

        ('',)
    ])

    @parameterized.expand(noteId_must_key_None)
    def testCase_01(self, param):
        """must_key_noteIds1，None2,''"""
        step('STEP1:造1条测试数据')
        res = self.generateNote.generate_note_test(1, self.userId, self.sid)
        step('STEP2:获取便签内容')
        body = {
            'noteIds': param
        }
        res = self.apiRequests.note_post(self.host + self.getNoteBody, self.userId, self.sid, body)
        self.assertEqual(500, res.status_code)
        expected = {'errorCode': -7, 'errorMsg': ''}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    noteId_must_key_null = ([
        (None,)

    ])

    @parameterized.expand(noteId_must_key_null)
    def testCase_02(self, param):
        """must_key_noteIds1，None2,''"""
        step('STEP1:造1条测试数据')
        res = self.generateNote.generate_note_test(1, self.userId, self.sid)
        step('STEP2:获取便签内容')
        body = {
            'noteIds': param
        }
        res = self.apiRequests.note_post(self.host + self.getNoteBody, self.userId, self.sid, body)
        self.assertEqual(500, res.status_code)
        expected = {'errorCode': -7, 'errorMsg': '参数不合法！'}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_03(self):
        """must_key_noteIds1，None2,''"""
        step('STEP1:造1条测试数据')
        noteIds = self.generateNote.generate_note_test(1, self.userId, self.sid)
        step('STEP2:获取便签内容')
        body = {
            'noteIds': noteIds
        }
        body.pop('noteIds')
        res = self.apiRequests.note_post(self.host + self.getNoteBody, self.userId, self.sid, body)
        self.assertEqual(500, res.status_code)
        expected = {'errorCode': -7, 'errorMsg': '参数不合法！'}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    noteIds_contains_chinese = [['!!!@@@'], ['你好']]

    @parameterized.expand(noteIds_contains_chinese)
    def testCase_04(self, param):
        """must_key_noteIds1，特殊字符'2,包含中文'"""
        step('STEP1:造1条测试数据')
        noteIds = self.generateNote.generate_note_test(1, self.userId, self.sid)
        step('STEP2:获取便签内容')
        body = {
            'noteIds': param
        }
        res = self.apiRequests.note_post(self.host + self.getNoteBody, self.userId, self.sid, body)
        self.assertEqual(500, res.status_code)
        expected = {'errorCode': -7, 'errorMsg': ''}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_05(self):
        """must_key_noteIds1不存在的noteId'"""
        step('STEP1:造1条测试数据')
        noteIds = self.generateNote.generate_note_test(1, self.userId, self.sid)
        step('STEP2:获取便签内容')
        body = {
            'noteIds': ['123']
        }
        res = self.apiRequests.note_post(self.host + self.getNoteBody, self.userId, self.sid, body)
        self.assertEqual(200, res.status_code)
        expected = {'responseTime': int, 'noteBodies': []}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_06(self):
        """must_key_noteIds1不存在的noteId'"""
        step('STEP1:造1条测试数据')
        noteIds = self.generateNote.generate_note_test(1, self.userId, self.sid)
        step('STEP2:获取便签内容')
        body = {
            'noteIds': ['123 ' or '1=1']
        }
        res = self.apiRequests.note_post(self.host + self.getNoteBody, self.userId, self.sid, body)
        self.assertEqual(200, res.status_code)
        expected = {'responseTime': int, 'noteBodies': []}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_07(self):
        """身份校验-删除cookie'"""
        step('STEP1:造1条测试数据')
        noteIds = self.generateNote.generate_note_test(1, self.userId, self.sid)
        step('STEP2:获取便签内容')
        body = {
            'noteIds': noteIds
        }
        new_header = {
            'Content-Type': 'application/json',
            'X-user-key': str(self.userId),
            'Cookie': f'wps_sid={self.sid}'
        }
        new_header.pop('Cookie')
        res = self.apiRequests.note_post(self.host + self.getNoteBody, self.userId, self.sid, body, new_header)
        self.assertEqual(401, res.status_code)
        expected = {'errorCode': -2009, 'errorMsg': ''}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_08(self):
        """身份校验-不存在的sid'"""
        step('STEP1:造1条测试数据')
        noteIds = self.generateNote.generate_note_test(1, self.userId, self.sid)
        step('STEP2:获取便签内容')
        body = {
            'noteIds': noteIds
        }
        new_header = {
            'Content-Type': 'application/json',
            'X-user-key': str(self.userId),
            'Cookie': f'wps_sid={self.notPresentSid}'
        }
        res = self.apiRequests.note_post(self.host + self.getNoteBody, self.userId, self.notPresentSid, body,
                                         new_header)
        self.assertEqual(401, res.status_code)
        expected = {'errorCode': -2010, 'errorMsg': ''}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_09(self):
        """身份校验-不存在的sid'"""
        step('STEP1:造1条测试数据')
        noteIds = self.generateNote.generate_note_test(1, self.userId, self.sid)
        step('STEP2:获取便签内容')
        body = {
            'noteIds': noteIds
        }
        new_header = {
            'Content-Type': 'application/json',
            'X-user-key': str(self.userId),
            'Cookie': f'wps_sid={self.sid}'
        }
        new_header.pop('Cookie')
        res = self.apiRequests.note_post(self.host + self.getNoteBody, self.userId, self.sid, body,
                                         new_header)
        self.assertEqual(401, res.status_code)
        expected = {'errorCode': -2009, 'errorMsg': ''}
        self.outPutResult.check_out(expected=expected, actual=res.json())
