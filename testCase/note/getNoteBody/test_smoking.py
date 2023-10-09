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
class TestCaseGetNoteBodySmoking(unittest.TestCase):
    envConfig = YamlOperator().env_config()
    getNoteBodyConfig = YamlOperator.api_data_config('getNoteBody')
    host = envConfig['host']
    sid = envConfig['sid']
    userId = envConfig['user_id']

    wipeNote = WipeNote()
    generateNote = GenerateNote()
    apiRequests = ApiRequests()
    outPutResult = CheckResult()
    getNoteBody = getNoteBodyConfig['getNoteBody']
    setNoteInfoPath = getNoteBodyConfig['setNoteInfoPath']
    addNoteContentPath = getNoteBodyConfig['addNoteContentPath']
    key = envConfig['key'].encode('utf-8')
    iv = envConfig['iv'].encode('utf-8')

    def setUp(self) -> None:
        """清空数据"""
        self.wipeNote.wipeNote(self.userId, self.sid)

    def testCase_01(self):
        """获取标签内容冒烟测试"""
        step('STEP1:新建便签主体')
        note_id = str(int(time.time() * 1000)) + '_noteId'

        body = {
            'noteId': note_id
        }

        res = self.apiRequests.note_post(self.host + self.setNoteInfoPath, self.userId, self.sid, body)
        step('STEP2:新建便签内容')
        contentVersion = res.json()['infoVersion']
        title = encry('恭喜', self.key, self.iv)
        summary = encry('恭喜发财', self.key, self.iv)
        text_body = encry('zzzzzzzzz', self.key, self.iv)
        body = {
            'noteId': note_id,
            'title': title,
            'summary': summary,
            'body': text_body,
            'localContentVersion': contentVersion,
            'BodyType': 0

        }
        self.apiRequests.note_post(self.host + self.addNoteContentPath, self.userId, self.sid, body)

        step('STEP3:获取便签内容')
        body = {
            'noteIds': [note_id]
        }
        res = self.apiRequests.note_post(self.host + self.getNoteBody, self.userId, self.sid, body)
        step('STEP4:校验code和校验返回值')
        self.assertEqual(200, res.status_code)
        expected = {'responseTime': int, 'noteBodies': [
            {'summary': summary, 'noteId': note_id,
             'infoNoteId': note_id, 'bodyType': 0, 'body': text_body,
             'contentVersion': contentVersion, 'contentUpdateTime': int, 'title': title, 'valid': 1}]}
        self.outPutResult.check_out(expected=expected, actual=res.json())
