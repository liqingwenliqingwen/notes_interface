import time
import unittest

from parameterized import parameterized

from business.apiRequest import ApiRequests
from business.generateNote import GenerateNote
from business.wipeNote import WipeNote
from common.caseLog import class_case_log, step
from common.checkResult import CheckResult
from common.yamlOperator import YamlOperator


@class_case_log
class TestCaseDeleteNoteSvrInput(unittest.TestCase):
    apiRequests = ApiRequests()
    wipeNote = WipeNote()
    generateNote = GenerateNote()
    outPutResult = CheckResult()
    envConfig = YamlOperator().env_config()
    deleteNoteSvrConfig = YamlOperator.api_data_config('deleteNoteSvr')
    host = envConfig['host']
    userId = envConfig['user_id']
    userIdB = envConfig['user_idB']
    sid = envConfig['sid']
    notPresentSid = envConfig['notPresentSid']
    deleteNoteSvr = deleteNoteSvrConfig['deleteNoteSvr']

    key = envConfig['key'].encode('utf-8')
    iv = envConfig['iv'].encode('utf-8')

    getNotePath = '/v3/notesvr/user/{}/home/startindex/{}/rows/{}/notes'.format(236948373, 0, 10)

    def setUp(self) -> None:
        """清除数据"""
        self.wipeNote.wipeNote(self.userId, self.sid)

    must_key_noteId_None = ([
        (None,),
        ('',)
    ])

    @parameterized.expand(must_key_noteId_None)
    def testCase_01(self, param):
        """校验input_noteId 1，None 2,''"""
        step('STEP1:造1条测试数据')
        noteIds = self.generateNote.generate_note_test(1, self.userId, self.sid)
        step('STEP2:删除测试数据')
        body = {
            'noteId': param
        }
        res = self.apiRequests.note_post(self.host + self.deleteNoteSvr, self.userId, self.sid, body)
        self.assertEqual(500, res.status_code)
        expected = {'errorCode': -7, 'errorMsg': '参数不合法！'}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_02(self):
        """校验input_noteId 删除必填项的key"""
        step('STEP1:造1条测试数据')
        noteIds = self.generateNote.generate_note_test(1, self.userId, self.sid)
        for item in range(len(noteIds)):
            noteId = noteIds[item]
            step('STEP2:删除测试数据')
            body = {
                'noteId': noteId
            }
            body.pop('noteId')
            res = self.apiRequests.note_post(self.host + self.deleteNoteSvr, self.userId, self.sid, body)
            self.assertEqual(500, res.status_code)
            expected = {'errorCode': -7, 'errorMsg': '参数不合法！'}
            self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_03(self):
        """校验input_noteId 删除不存在的noteId"""
        noteId_ = str(int(time.time() * 1000)) + '_id'
        step('STEP1:造1条测试数据')
        noteIds = self.generateNote.generate_note_test(1, self.userId, self.sid)
        for item in range(len(noteIds)):
            noteId = noteIds[item]
            step('STEP2:删除测试数据')
            body = {
                'noteId': noteId_
            }
            res = self.apiRequests.note_post(self.host + self.deleteNoteSvr, self.userId, self.sid, body)
            self.assertEqual(200, res.status_code)
        step('STEP3:校验数据')
        res = self.apiRequests.note_get(self.host + self.getNotePath, self.userId, self.sid)
        self.assertEqual(1, len(res.json()['webNotes']))

    must_key_noteId = ['!!!!@@@@']

    @parameterized.expand(must_key_noteId)
    def testCase_04(self, param):
        """校验input_noteId 包括特殊字符@！！！''"""
        step('STEP1:造1条测试数据')
        noteIds = self.generateNote.generate_note_test(1, self.userId, self.sid)
        step('STEP2:删除测试数据')
        body = {
            'noteId': param
        }
        res = self.apiRequests.note_post(self.host + self.deleteNoteSvr, self.userId, self.sid, body)
        self.assertEqual(200, res.status_code)

    must_key_noteId_chinese = ['你好', '9999999999999999999999999999999999999999999999999999999999999']

    @parameterized.expand(must_key_noteId_chinese)
    def testCase_05(self, param):
        """校验input_noteId 包括特殊字符@！！！''"""
        step('STEP1:造1条测试数据')
        noteIds = self.generateNote.generate_note_test(1, self.userId, self.sid)
        step('STEP2:删除测试数据')
        body = {
            'noteId': param
        }
        res = self.apiRequests.note_post(self.host + self.deleteNoteSvr, self.userId, self.sid, body)
        self.assertEqual(500, res.status_code)
        expected = {'errorCode': -7, 'errorMsg': str}

        self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_06(self):
        """校验删除标签数据-校验身份''"""
        step('STEP1:造1条测试数据')
        noteIds = self.generateNote.generate_note_test(1, self.userId, self.sid)
        step('STEP2:删除测试数据')
        body = {
            'noteId': noteIds
        }
        res = self.apiRequests.note_post(self.host + self.deleteNoteSvr, self.userIdB, self.sid, body)
        self.assertEqual(500, res.status_code)
        expected = {'errorCode': -7, 'errorMsg': str}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_07(self):
        """校验删除标签数据-删除cookie''"""
        step('STEP1:造1条测试数据')
        noteIds = self.generateNote.generate_note_test(1, self.userId, self.sid)
        step('STEP2:删除测试数据')
        body = {
            'noteId': noteIds
        }
        new_header = {
            'Content-Type': 'application/json',
            'X-user-key': str(self.userId),
            'Cookie': f'wps_sid={self.sid}'
        }
        new_header.pop('Cookie')
        res = self.apiRequests.note_post(self.host + self.deleteNoteSvr, self.userId, self.sid, body, new_header)
        self.assertEqual(500, res.status_code)
        expected = {'errorCode': -7, 'errorMsg': str}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_08(self):
        """身份校验，不存在的sid''"""
        step('STEP1:造1条测试数据')
        noteIds = self.generateNote.generate_note_test(1, self.userId, self.sid)
        step('STEP2:删除测试数据')
        body = {
            'noteId': noteIds
        }
        new_header = {
            'Content-Type': 'application/json',
            'X-user-key': str(self.userId),
            'Cookie': f'wps_sid={self.sid}'
        }

        res = self.apiRequests.note_post(self.host + self.deleteNoteSvr, self.userId, self.notPresentSid, body,
                                         new_header)
        self.assertEqual(500, res.status_code)
        expected = {'errorCode': -7, 'errorMsg': str}
        self.outPutResult.check_out(expected=expected, actual=res.json())
