import time
import unittest

from parameterized import parameterized

from business.apiRequest import ApiRequests
from business.generateNote import GenerateNote
from business.wipeNote import WipeNote
from common.AES_tool import encry, decry
from common.caseLog import step, class_case_log
from common.checkResult import CheckResult
from common.yamlOperator import YamlOperator


@class_case_log
class SetNoteContentHandle(unittest.TestCase):
    envConfig = YamlOperator().env_config()
    setNoteContentConfig = YamlOperator().api_data_config('setNoteContent')
    outPutResult = CheckResult()
    apiRequests = ApiRequests()
    wipeNote = WipeNote()
    generateNote = GenerateNote()

    host = envConfig['host']
    sid = envConfig['sid']
    sidB = envConfig['sidB']
    userId = envConfig['user_id']
    userIdB = envConfig['user_idB']
    setNoteInfoPath = setNoteContentConfig['setNoteInfoPath']
    addNoteContentPath = setNoteContentConfig['addNoteContentPath']
    getNoteBody = setNoteContentConfig['getNoteBody']

    key = envConfig['key'].encode('utf-8')
    iv = envConfig['iv'].encode('utf-8')

    def setUp(self) -> None:
        """清除数据"""
        self.wipeNote.wipeNote(self.userId, self.sid)

    body_text_enum = [0, 1]

    @parameterized.expand(body_text_enum)
    def testCase_01_set_note_handle_bodyType_enum(self, param):
        """遍历body_text的枚举值"""
        step('STEP1:设置便签主体')

        noteId = str(int(time.time() * 1000)) + '_noteId'
        body = {
            'noteId': noteId
        }
        res = self.apiRequests.note_post(self.host + self.setNoteInfoPath, self.userId, self.sid, body)
        contentVersion = res.json()['infoVersion']
        step('STEP2:新建便签内容')
        title = encry('你好中国', self.key, self.iv)
        summary = encry('中国你好', self.key, self.iv)
        body_text = encry('哈哈哈哈哈', self.key, self.iv)
        body = {
            'noteId': noteId,
            'title': title,
            'summary': summary,
            'body': body_text,
            'localContentVersion': contentVersion,
            'BodyType': param
        }
        res = self.apiRequests.note_post(self.host + self.addNoteContentPath, self.userId, self.sid, body)
        self.assertEqual(200, res.status_code)

    def testCase_02_set_note_content_handle(self):
        """新增一个不存在的便签内容"""
        step('STEP1:设置便签主体')

        noteId = str(int(time.time() * 1000)) + '_noteId'
        body = {
            'noteId': noteId
        }
        res = self.apiRequests.note_post(self.host + self.setNoteInfoPath, self.userId, self.sid, body)
        contentVersion = res.json()['infoVersion']
        step('STEP2:新建便签内容')
        title = encry('你好中国', self.key, self.iv)
        summary = encry('中国你好', self.key, self.iv)
        body_text = encry('哈哈哈哈哈', self.key, self.iv)
        body = {
            'noteId': noteId,
            'title': title,
            'summary': summary,
            'body': body_text,
            'localContentVersion': contentVersion,
            'BodyType': 0
        }
        res = self.apiRequests.note_post(self.host + self.addNoteContentPath, self.userId, self.sid, body)
        self.assertEqual(200, res.status_code)
        step('STEP3:获取便签内容')
        body = {
            'noteIds': [noteId]
        }
        res = self.apiRequests.note_post(self.host + self.getNoteBody, self.userId, self.sid, body)
        titleRes = [item['title'] for item in res.json()['noteBodies']]
        summaryRes = [item['summary'] for item in res.json()['noteBodies']]
        text_bodyRes = [item['body'] for item in res.json()['noteBodies']]

        step('step4:获取每一个title,校验title')
        for item in range(len(titleRes)):
            title = titleRes[item]
        titleDecry = decry(title, self.key, self.iv)
        self.assertEqual(titleDecry.replace('\x04', ''), '你好中国')

        step('step5:获取每一个summary,校验summary')
        for item in range(len(summaryRes)):
            summary = summaryRes[item]
        summaryDecry = decry(summary, self.key, self.iv)
        self.assertEqual(summaryDecry.replace('\x04', ''), '中国你好')

        step('STEP6:获取每一个text_bodyRes,校验text_bodyRes')
        for item in range(len(text_bodyRes)):
            text_body = text_bodyRes[item]
        text_bodyDecry = decry(body_text, self.key, self.iv)
        self.assertEqual(text_bodyDecry.strip('\x01'), '哈哈哈哈哈')

    def testCase_03_update_note_content_handle(self):
        """更新便签内容"""
        step('STEP1:设置便签主体')

        noteId = str(int(time.time() * 1000)) + '_noteId'
        body = {
            'noteId': noteId
        }
        res = self.apiRequests.note_post(self.host + self.setNoteInfoPath, self.userId, self.sid, body)
        contentVersion = res.json()['infoVersion']
        step('STEP2:新建便签内容')
        title = encry('你好中国', self.key, self.iv)
        summary = encry('中国你好', self.key, self.iv)
        body_text = encry('哈哈哈哈哈', self.key, self.iv)
        body = {
            'noteId': noteId,
            'title': title,
            'summary': summary,
            'body': body_text,
            'localContentVersion': contentVersion,
            'BodyType': 0
        }
        res = self.apiRequests.note_post(self.host + self.addNoteContentPath, self.userId, self.sid, body)

        step('STEP3：更新便签内容')
        title_update = encry('国庆节中秋节快乐', self.key, self.iv)
        body = {
            'noteId': noteId,
            'title': title_update,
            'summary': summary,
            'body': body_text,
            'localContentVersion': contentVersion,
            'BodyType': 0
        }
        res_update = self.apiRequests.note_post(self.host + self.addNoteContentPath, self.userId, self.sid, body)
        step('STEP4:获取便签内容')
        body = {
            'noteIds': [noteId]
        }
        res = self.apiRequests.note_post(self.host + self.getNoteBody, self.userId, self.sid, body)
        titleRes = [item['title'] for item in res.json()['noteBodies']]
        summaryRes = [item['summary'] for item in res.json()['noteBodies']]
        text_bodyRes = [item['body'] for item in res.json()['noteBodies']]

        step('step5:获取每一个title,校验title')
        for item in range(len(titleRes)):
            title = titleRes[item]
        titleDecry = decry(title, self.key, self.iv)
        self.assertEqual(titleDecry.replace('\x08', ''), '国庆节中秋节快乐')

        step('step5:获取每一个summary,校验summary')
        for item in range(len(summaryRes)):
            summary = summaryRes[item]
        summaryDecry = decry(summary, self.key, self.iv)
        self.assertEqual(summaryDecry.replace('\x04', ''), '中国你好')

        step('STEP6:获取每一个text_bodyRes,校验text_bodyRes')
        for item in range(len(text_bodyRes)):
            text_body = text_bodyRes[item]
        text_bodyDecry = decry(body_text, self.key, self.iv)
        self.assertEqual(text_bodyDecry.strip('\x01'), '哈哈哈哈哈')

    def testCase_04_set_note_content_handle(self):
        """用户B去更新用户A 下的便签内容"""
        step('STEP1:设置便签主体')

        noteId = str(int(time.time() * 1000)) + '_noteId'
        body = {
            'noteId': noteId
        }
        res = self.apiRequests.note_post(self.host + self.setNoteInfoPath, self.userId, self.sid, body)
        contentVersion = res.json()['infoVersion']
        step('STEP2:新建便签内容')
        title = encry('你好中国', self.key, self.iv)
        summary = encry('中国你好', self.key, self.iv)
        body_text = encry('哈哈哈哈哈', self.key, self.iv)
        body = {
            'noteId': noteId,
            'title': title,
            'summary': summary,
            'body': body_text,
            'localContentVersion': contentVersion,
            'BodyType': 0
        }
        res = self.apiRequests.note_post(self.host + self.addNoteContentPath, self.userId, self.sidB, body)
        self.assertEqual(412, res.status_code)
        expected = {'errorCode': -1011, 'errorMsg': 'user change!'}
        self.outPutResult.check_out(expected=expected, actual=res.json())
