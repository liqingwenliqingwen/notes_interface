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
class TestCaseGetNotesRemindHandle(unittest.TestCase):
    apiRequests = ApiRequests()
    wipeNote = WipeNote()
    generateNote = GenerateNote()
    outPutResult = CheckResult()
    envConfig = YamlOperator().env_config()
    getNotesRemindConfig = YamlOperator.api_data_config('getNotesRemind')
    host = envConfig['host']
    userId = envConfig['user_id']
    sid = envConfig['sid']
    sidB = envConfig['sidB']
    setNoteInfoPath = getNotesRemindConfig['setNoteInfoPath']
    key = envConfig['key'].encode('utf-8')
    iv = envConfig['iv'].encode('utf-8')
    addNoteContentPath = getNotesRemindConfig['addNoteContentPath']
    getNotesRemind = getNotesRemindConfig['getNotesRemind']

    def setUp(self) -> None:
        """清空数据"""
        self.wipeNote.wipeNote(self.userId, self.sid)

    def testCase_01(self):
        """-用户A查看用户B下的日历下便签"""
        noteId = str(int(time.time() * 1000)) + '_note_id'
        step('STEP1:新建日历下便签')
        body = {
            'noteId': noteId,
            'remindTime': 1704072587

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
        res = self.apiRequests.note_post(self.host + self.getNotesRemind, self.userId, self.sidB, body)
        self.assertEqual(412, res.status_code)
        expected = {'errorCode': -1011, 'errorMsg': 'user change!'}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_02(self):
        """查看日历便签的开始时间，比时间时间大"""
        noteId = str(int(time.time() * 1000)) + '_note_id'
        step('STEP1:新建日历下便签')
        body = {
            'noteId': noteId,
            'remindTime': 1704072587

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
        remindEndTime = 1701394187
        remindStartTime = 1706750987
        body = {
            'remindStartTime': remindStartTime,
            'remindEndTime': remindEndTime,
            'startIndex': 0,
            'rows': 10

        }
        res = self.apiRequests.note_post(self.host + self.getNotesRemind, self.userId, self.sid, body)
        self.assertEqual(412, res.status_code)
        expected = {'errorCode': -7, 'errorMsg': 'remindTime Requested!'}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_03(self):
        """新建便签不在查询范围内"""
        noteId = str(int(time.time() * 1000)) + '_note_id'
        step('STEP1:新建日历下便签')
        body = {
            'noteId': noteId,
            'remindTime': 1704072587

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
        remindEndTime = 760066187
        remindStartTime = 728530187
        body = {
            'remindStartTime': remindStartTime,
            'remindEndTime': remindEndTime,
            'startIndex': 0,
            'rows': 10

        }
        res = self.apiRequests.note_post(self.host + self.getNotesRemind, self.userId, self.sid, body)
        self.assertEqual(200, res.status_code)
        expected = {'responseTime': 0, 'webNotes': []}
        self.outPutResult.check_out(expected=expected, actual=res.json())
