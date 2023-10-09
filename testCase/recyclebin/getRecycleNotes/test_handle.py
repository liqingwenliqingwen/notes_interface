import unittest

from business.apiRequest import ApiRequests
from business.generateNote import GenerateNote
from business.wipeNote import WipeNote
from common.caseLog import class_case_log, step, info
from common.checkResult import CheckResult
from common.yamlOperator import YamlOperator


@class_case_log
class TestCaseGetRecycleNoteTestHandle(unittest.TestCase):
    apiRequests = ApiRequests()
    wipeNote = WipeNote()
    generateNote = GenerateNote()
    outPutResult = CheckResult()
    envConfig = YamlOperator().env_config()
    getRecycleNotesConfig = YamlOperator.api_data_config('recycleNotes')
    host = envConfig['host']
    userId = envConfig['user_id']
    sid = envConfig['sid']
    sidB = envConfig['sidB']
    setNoteInfoPath = getRecycleNotesConfig['setNoteInfoPath']
    key = envConfig['key'].encode('utf-8')
    iv = envConfig['iv'].encode('utf-8')
    addNoteContentPath = getRecycleNotesConfig['addNoteContentPath']
    deleteNoteSvr = getRecycleNotesConfig['deleteNoteSvr']
    pathCleanRecycle = getRecycleNotesConfig['pathCleanRecycle']
    getRecycleNotes = '/v3/notesvr/user/{}/invalid/startindex/{}/rows/{}/notes'.format('236948373', '0', 1)

    def setUp(self) -> None:
        """清除数据"""
        self.wipeNote.wipeNote(self.userId, self.sid)

    def testCase_01(self):
        """rows限制，删除2条便签，rows=1,只查一条数据"""
        step('STEP1:造1条测试数据')
        noteIds = self.generateNote.generate_note_test(2, self.userId, self.sid)
        step('STEP2:删除一条创建的便签')
        body = {
            'noteId': noteIds[0]

        }
        self.apiRequests.note_post(self.host + self.deleteNoteSvr, self.userId, self.sid, body)
        step('STEP3:获取回收站下便签')
        res = self.apiRequests.note_get(self.host + self.getRecycleNotes, self.userId, self.sid)
        noteIdsRes = [item['noteId'] for item in res.json()['webNotes']]
        info(f'获取的回收站下的便签{noteIdsRes}')
        if len(noteIdsRes) == 1:
            info('rows只查询到一条数据')

    def testCase_02(self):
        """用户A查看用户B 下的回收站便签数据"""
        step('STEP1:造1条测试数据')
        noteIds = self.generateNote.generate_note_test(1, self.userId, self.sid)
        step('STEP2:删除创建的便签')
        for item in range(len(noteIds)):
            noteId = noteIds[item]
            body = {
                'noteId': noteId

            }
            self.apiRequests.note_post(self.host + self.deleteNoteSvr, self.userId, self.sid, body)

        step('STEP3:获取回收站下便签')
        res = self.apiRequests.note_get(self.host + self.getRecycleNotes, self.userId, self.sidB)
        self.assertEqual(412, res.status_code)
        expected = {'errorCode': -1011, 'errorMsg': 'user change!'}
        self.outPutResult.check_out(expected=expected, actual=res.json())
