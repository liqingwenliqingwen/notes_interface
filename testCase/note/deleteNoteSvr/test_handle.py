import unittest

from business.apiRequest import ApiRequests
from business.generateNote import GenerateNote
from business.wipeNote import WipeNote
from common.caseLog import class_case_log, step
from common.checkResult import CheckResult
from common.yamlOperator import YamlOperator


@class_case_log
class TestCaseDeleteNoteSvrHandle(unittest.TestCase):
    apiRequests = ApiRequests()
    wipeNote = WipeNote()
    generateNote = GenerateNote()
    outPutResult = CheckResult()
    envConfig = YamlOperator().env_config()
    deleteNoteSvrConfig = YamlOperator.api_data_config('deleteNoteSvr')
    host = envConfig['host']
    userId = envConfig['user_id']
    userIdB = envConfig['user_idB']
    sidB = envConfig['sidB']
    sid = envConfig['sid']
    deleteNoteSvr = deleteNoteSvrConfig['deleteNoteSvr']

    key = envConfig['key'].encode('utf-8')
    iv = envConfig['iv'].encode('utf-8')

    getNotePath = '/v3/notesvr/user/{}/home/startindex/{}/rows/{}/notes'.format(236948373, 0, 10)

    def setUp(self) -> None:
        """清除数据"""
        self.wipeNote.wipeNote(self.userId, self.sid)

    def testCase_01(self):
        """用户A删除用户B下的便签"""
        step('STEP1:用户A 下造1条测试数据')
        noteIds = self.generateNote.generate_note_test(1, self.userId, self.sid)
        for item in range(len(noteIds)):
            noteId = noteIds[item]
            step('STEP2:用户B删除数据')
            body = {
                'noteId': noteId
            }
            res = self.apiRequests.note_post(self.host + self.deleteNoteSvr, self.userIdB, self.sidB, body)
            self.assertEqual(200, res.status_code)
        step('STEP3:获取用户A下的便签数据')
        res = self.apiRequests.note_get(self.host + self.getNotePath, self.userId, self.sid)
        noteIdsRes = [item['noteId'] for item in res.json()['webNotes']]
        step('STEP4:用户A下新建的便签数据，用户B删除后，获取用户A下的便签数据和新建的一致')
        self.assertEqual(noteIds, noteIdsRes)

    def testCase_02(self):
        """用户A下有2条用户数据，只删除一条"""
        step('STEP1:用户A 下造2条测试数据')
        noteIds = self.generateNote.generate_note_test(2, self.userId, self.sid)
        body = {
            'noteId': noteIds[0]
        }
        step('STEP2:删除一条用户数据')
        res = self.apiRequests.note_post(self.host + self.deleteNoteSvr, self.userId, self.sid, body)
        self.assertEqual(200, res.status_code)
        step('STEP3:获取用户A下的便签数据')
        res = self.apiRequests.note_get(self.host + self.getNotePath, self.userId, self.sid)
        noteIdsRes = [item['noteId'] for item in res.json()['webNotes']]
        step('STEP4:用户A下新建的便签数据，用户B删除后，获取用户A下的便签数据和新建的一致')
        self.assertEqual([noteIds[1]], noteIdsRes)
