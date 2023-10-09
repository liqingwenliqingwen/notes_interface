import unittest

from business.apiRequest import ApiRequests
from business.generateNote import GenerateNote
from business.wipeNote import WipeNote
from common.caseLog import class_case_log, step
from common.checkResult import CheckResult
from common.yamlOperator import YamlOperator


@class_case_log
class TestCaseGetRecycleNoteSmoking(unittest.TestCase):
    apiRequests = ApiRequests()
    wipeNote = WipeNote()
    generateNote = GenerateNote()
    outPutResult = CheckResult()
    envConfig = YamlOperator().env_config()
    getRecycleNotesConfig = YamlOperator.api_data_config('recycleNotes')
    host = envConfig['host']
    userId = envConfig['user_id']
    sid = envConfig['sid']
    setNoteInfoPath = getRecycleNotesConfig['setNoteInfoPath']
    key = envConfig['key'].encode('utf-8')
    iv = envConfig['iv'].encode('utf-8')
    addNoteContentPath = getRecycleNotesConfig['addNoteContentPath']
    deleteNoteSvr = getRecycleNotesConfig['deleteNoteSvr']
    pathCleanRecycle = getRecycleNotesConfig['pathCleanRecycle']
    getRecycleNotes = '/v3/notesvr/user/{}/invalid/startindex/{}/rows/{}/notes'.format('236948373', '0', '50')

    def setUp(self) -> None:
        """清除数据"""
        self.wipeNote.wipeNote(self.userId, self.sid)

    def testCase_01(self):
        """获取回收站便签主体"""
        step('STEP1:造1条测试数据')
        noteIds = self.generateNote.generate_note_test(1, self.userId, self.sid)
        step('STEP2:删除创建的便签')

        body = {
            'noteId': noteIds[0]

        }
        self.apiRequests.note_post(self.host + self.deleteNoteSvr, self.userId, self.sid, body)

        step('STEP3:获取回收站下便签')
        res = self.apiRequests.note_get(self.host + self.getRecycleNotes, self.userId, self.sid)
        self.assertEqual(200, res.status_code)
        expected = {'responseTime': 0, 'webNotes': [
            {'noteId': noteIds[0], 'createTime': int, 'star': 0, 'remindTime': 0,
             'remindType': 0, 'infoVersion': 2, 'infoUpdateTime': int, 'groupId': None,
             'title': 'aiXhXKtVDyR9/L7DJTxhLg==', 'summary': '4ZTUOD5fyvtLawr5pV/D3w==', 'thumbnail': None,
             'contentVersion': 1, 'contentUpdateTime': int}]}
        self.outPutResult.check_out(expected=expected, actual=res.json())
