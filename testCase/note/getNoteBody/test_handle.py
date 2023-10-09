import unittest

from business.apiRequest import ApiRequests
from business.generateNote import GenerateNote
from business.wipeNote import WipeNote
from common.caseLog import step, class_case_log
from common.checkResult import CheckResult
from common.yamlOperator import YamlOperator


@class_case_log
class TestCaseGetNoteBodyHandle(unittest.TestCase):
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
    userIdB = envConfig['user_idB']

    def setUp(self) -> None:
        """清楚历史数据"""
        self.wipeNote.wipeNote(self.userId, self.sid)

    def testCase_01(self):
        """1条测试数据查询"""
        step('STEP1:造1条测试数据')
        noteIds = self.generateNote.generate_note_test(1, self.userId, self.sid)
        body = {
            'noteIds': noteIds
        }
        res = self.apiRequests.note_post(self.host + self.getNoteBody, self.userId, self.sid, body)
        step('STEP2:获取到的便签内容中的noteId和创建的noteIds相等')
        noteId = [item['noteId'] for item in res.json()['noteBodies']]
        self.assertEqual(noteId, noteIds)

    def testCase_02(self):
        """多条测试数据查询"""
        step('STEP1:造2条测试数据')
        noteIds = self.generateNote.generate_note_test(2, self.userId, self.sid)
        body = {
            'noteIds': noteIds
        }
        res = self.apiRequests.note_post(self.host + self.getNoteBody, self.userId, self.sid, body)
        step('STEP2:获取到的便签内容中的noteId和创建的noteIds相等')
        noteId = [item['noteId'] for item in res.json()['noteBodies']]
        self.assertEqual(noteId, noteIds)

    def testCase_03(self):
        """用户A下查询用户B下的便签内容"""
        step('STEP1:造2条测试数据')
        noteIds = self.generateNote.generate_note_test(1, self.userId, self.sid)
        body = {
            'noteIds': noteIds
        }
        res = self.apiRequests.note_post(self.host + self.getNoteBody, self.userIdB, self.sid, body)
        self.assertEqual(412, res.status_code)
        step('STEP2:校验返回值')
        expected = {'errorCode': -1011, 'errorMsg': 'user change!'}
        self.outPutResult.check_out(expected=expected, actual=res.json())
