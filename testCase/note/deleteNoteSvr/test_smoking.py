import unittest

from business.apiRequest import ApiRequests
from business.generateNote import GenerateNote
from business.wipeNote import WipeNote
from common.caseLog import class_case_log, step
from common.checkResult import CheckResult
from common.yamlOperator import YamlOperator


@class_case_log
class TestCaseDeleteNoteSvrSmoking(unittest.TestCase):
    apiRequests = ApiRequests()
    wipeNote = WipeNote()
    generateNote = GenerateNote()
    outPutResult = CheckResult()
    envConfig = YamlOperator().env_config()
    deleteNoteSvrConfig = YamlOperator.api_data_config('deleteNoteSvr')
    host = envConfig['host']
    userId = envConfig['user_id']
    sid = envConfig['sid']
    deleteNoteSvr = deleteNoteSvrConfig['deleteNoteSvr']

    key = envConfig['key'].encode('utf-8')
    iv = envConfig['iv'].encode('utf-8')

    getNotePath = '/v3/notesvr/user/{}/home/startindex/{}/rows/{}/notes'.format(236948373, 0, 10)

    def setUp(self) -> None:
        """清除数据"""
        self.wipeNote.wipeNote(self.userId, self.sid)

    def testCase_01(self):
        """删除noteId冒烟测试"""
        step('STEP1:造1条测试数据')
        noteIds = self.generateNote.generate_note_test(1, self.userId, self.sid)
        for item in range(len(noteIds)):
            noteId = noteIds[item]
            step('STEP2:删除新建的noteId')
            body = {
                'noteId': noteId
            }
            res = self.apiRequests.note_post(self.host + self.deleteNoteSvr, self.userId, self.sid, body)
            self.assertEqual(200, res.status_code)

        step('STEP3:获取便签首页便签数据为0')
        res = self.apiRequests.note_get(self.host + self.getNotePath, self.userId, self.sid)
        self.assertEqual(0, len(res.json()['webNotes']))

