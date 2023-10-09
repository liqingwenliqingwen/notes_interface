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
    setNoteContentConfig = YamlOperator.api_data_config('setNoteContent')
    host = envConfig['host']
    userId = envConfig['user_id']
    sid = envConfig['sid']
    setNoteInfoPath = setNoteContentConfig['setNoteInfoPath']
    key = envConfig['key'].encode('utf-8')
    iv = envConfig['iv'].encode('utf-8')
    addNoteContentPath = setNoteContentConfig['addNoteContentPath']
    getNoteBody = setNoteContentConfig['getNoteBody']

    def setUp(self) -> None:
        """清空数据"""
        self.wipeNote.wipeNote(self.userId, self.sid)

    def testCase_01(self):
        """设置便签内容"""
        step('STEP1:设置便签主体')
        noteId = str(int(time.time() * 1000)) + '_noteId'
        body = {
            'noteId': noteId
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
        step('STEP3:获取便签内容')

        body = {
            'noteIds': [noteId]
        }
        res = self.apiRequests.note_post(self.host + self.getNoteBody, self.userId, self.sid, body)
        step('STEP4:校验返回值和code')
        self.assertEqual(200, res.status_code)
        expected = {'responseTime': int, 'noteBodies': [
            {'summary': summary, 'noteId': noteId,
             'infoNoteId': noteId, 'bodyType': 0, 'body': text_body,
             'contentVersion': contentVersion, 'contentUpdateTime': int, 'title': title, 'valid': 1}]}
        self.outPutResult.check_out(expected=expected, actual=res.json())
