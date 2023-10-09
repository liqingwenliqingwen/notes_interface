import time
import unittest

from business.apiRequest import ApiRequests
from business.generateNote import GenerateNote
from business.wipeNote import WipeNote
from common.AES_tool import encry
from common.caseLog import class_case_log, step
from common.checkResult import CheckResult
from common.yamlOperator import YamlOperator


@class_case_log
class TestCaseSetNoteContentSmoking(unittest.TestCase):
    apiRequests = ApiRequests()
    wipeNote = WipeNote()
    generateNote = GenerateNote()
    outPutResult = CheckResult()
    envConfig = YamlOperator().env_config()
    getNotesRemindConfig = YamlOperator.api_data_config('getNotesRemind')
    host = envConfig['host']
    userId = envConfig['user_id']
    sid = envConfig['sid']
    setNoteInfoPath = getNotesRemindConfig['setNoteInfoPath']
    key = envConfig['key'].encode('utf-8')
    iv = envConfig['iv'].encode('utf-8')
    addNoteContentPath = getNotesRemindConfig['addNoteContentPath']
    getNotesRemind = getNotesRemindConfig['getNotesRemind']

    def setUp(self) -> None:
        """清空数据"""
        self.wipeNote.wipeNote(self.userId, self.sid)

    def testCase_01(self):
        """查看日历下便签冒烟测试"""
        noteId = str(int(time.time() * 1000)) + 'note_id'
        step('STEP1:新建日历下便签')
        body = {
            'noteId': noteId,
            'remindTime': 1704072587,
            'remindType': 2

        }
        res = self.apiRequests.note_post(self.host + self.setNoteInfoPath, self.userId, self.sid, body)
        contentVersion = res.json()['infoVersion']
        step('STEP2:新建便签内容')
        title = encry('恭喜', self.key, self.iv)
        summary = encry('恭喜发财', self.key, self.iv)
        text_body = encry('中秋节快乐', self.key, self.iv)
        body = {
            'noteId': noteId,
            'title': title,
            'summary': summary,
            'body': text_body,
            'localContentVersion': contentVersion,
            'BodyType': 0

        }

        res = self.apiRequests.note_post(self.host + self.addNoteContentPath, self.userId, self.sid, body)
        step('STEP3:查看日历下便签')
        remindStartTime = 1701394187
        remindEndTime = 1706750987
        body = {
            'remindStartTime': remindStartTime,
            'remindEndTime': remindEndTime,
            'startIndex': 0,
            'rows': 10

        }
        res = self.apiRequests.note_post(self.host + self.getNotesRemind, self.userId, self.sid, body)
        # for item in res.json()['webNotes']:
        #     self.assertIn(noteId, item['noteId'])
        step('STEP4:断言查询到的便签都在查询范围内')
        for item in res.json()['webNotes']:
            assert remindStartTime <= item['remindTime'] <= remindEndTime
