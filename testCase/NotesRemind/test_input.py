import time
import unittest

from parameterized import parameterized

from business.apiRequest import ApiRequests
from business.generateNote import GenerateNote
from business.wipeNote import WipeNote
from common.AES_tool import encry
from common.caseLog import class_case_log, step
from common.checkResult import CheckResult
from common.yamlOperator import YamlOperator


@class_case_log
class TestCaseGetNotesRemindInput(unittest.TestCase):
    apiRequests = ApiRequests()
    wipeNote = WipeNote()
    generateNote = GenerateNote()
    outPutResult = CheckResult()
    envConfig = YamlOperator().env_config()
    getNotesRemindConfig = YamlOperator.api_data_config('getNotesRemind')
    host = envConfig['host']
    userId = envConfig['user_id']
    sid = envConfig['sid']
    notPresentSid = envConfig['notPresentSid']
    setNoteInfoPath = getNotesRemindConfig['setNoteInfoPath']
    key = envConfig['key'].encode('utf-8')
    iv = envConfig['iv'].encode('utf-8')
    addNoteContentPath = getNotesRemindConfig['addNoteContentPath']
    getNotesRemind = getNotesRemindConfig['getNotesRemind']

    def setUp(self) -> None:
        """清空数据"""
        self.wipeNote.wipeNote(self.userId, self.sid)

    remindStartTime = [
        (None,),
        ('',)
    ]

    @parameterized.expand(remindStartTime)
    def testCase_01(self, param):
        """查看日历下便签remindTime为空"""
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
            'remindStartTime': param,
            'remindEndTime': remindEndTime,
            'startIndex': 0,
            'rows': 10

        }
        res = self.apiRequests.note_post(self.host + self.getNotesRemind, self.userId, self.sid, body)
        self.assertEqual(412, res.status_code)
        expected = {'errorCode': -7, 'errorMsg': 'remindTime Requested!'}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    must_key = ['remindStartTime', 'remindEndTime']

    @parameterized.expand(must_key)
    def testCase_02(self, param):
        """查看日历下便签删除四个必填字段的key"""
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
        body.pop(param)
        res = self.apiRequests.note_post(self.host + self.getNotesRemind, self.userId, self.sid, body)
        self.assertEqual(412, res.status_code)
        expected = {'errorCode': -7, 'errorMsg': 'remindTime Requested!'}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    must_key_remindStartTime = [
        (0,)
    ]

    @parameterized.expand(must_key_remindStartTime)
    def testCase_03(self, param):
        """查看日历下便签删除四个必填字段的key"""
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
            'remindStartTime': param,
            'remindEndTime': remindEndTime,
            'startIndex': 0,
            'rows': 10

        }

        res = self.apiRequests.note_post(self.host + self.getNotesRemind, self.userId, self.sid, body)
        self.assertEqual(412, res.status_code)
        expected = {'errorCode': -7, 'errorMsg': 'remindTime Requested!'}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    must_key_remindStartTime = [
        (-1704072587,)
    ]

    @parameterized.expand(must_key_remindStartTime)
    def testCase_04(self, param):
        """查看日历下便签删除四个必填字段的key"""
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
            'remindStartTime': param,
            'remindEndTime': remindEndTime,
            'startIndex': 0,
            'rows': 10

        }

        res = self.apiRequests.note_post(self.host + self.getNotesRemind, self.userId, self.sid, body)
        self.assertEqual(200, res.status_code)
        expected = {'responseTime': 0, 'webNotes': list}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    must_key_remindStartTime = [(1.5,), ('5',)]

    @parameterized.expand(must_key_remindStartTime)
    def testCase_05(self, param):
        """查看日历下便签删除四个必填字段的key"""
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
            'remindStartTime': param,
            'remindEndTime': remindEndTime,
            'startIndex': 0,
            'rows': 10

        }

        res = self.apiRequests.note_post(self.host + self.getNotesRemind, self.userId, self.sid, body)
        self.assertEqual(200, res.status_code)
        expected = {'responseTime': 0, 'webNotes': list}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    remindEndTime = [
        (None,),
        ('',)
    ]

    @parameterized.expand(remindEndTime)
    def testCase_06(self, param):
        """查看日历下便签remindTime为空"""
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
            'remindEndTime': param,
            'startIndex': 0,
            'rows': 10

        }
        res = self.apiRequests.note_post(self.host + self.getNotesRemind, self.userId, self.sid, body)
        self.assertEqual(412, res.status_code)
        expected = {'errorCode': -7, 'errorMsg': 'remindTime Requested!'}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    must_key_remindEndTime = [(0,), (-1704072587,)]

    @parameterized.expand(must_key_remindStartTime)
    def testCase_07(self, param):
        """查看日历下便签删除四个必填字段的key"""
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
            'remindEndTime': param,
            'startIndex': 0,
            'rows': 10

        }

        res = self.apiRequests.note_post(self.host + self.getNotesRemind, self.userId, self.sid, body)
        self.assertEqual(412, res.status_code)
        expected = {'errorCode': -7, 'errorMsg': 'remindTime Requested!'}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    must_key_remindEndTime_ = [(1.5,), ('5',)]

    @parameterized.expand(must_key_remindEndTime_)
    def testCase_08(self, param):
        """查看日历下便签删除四个必填字段的key"""
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
            'remindEndTime': param,
            'startIndex': 0,
            'rows': 10

        }

        res = self.apiRequests.note_post(self.host + self.getNotesRemind, self.userId, self.sid, body)
        self.assertEqual(412, res.status_code)
        expected = {'errorCode': -7, 'errorMsg': 'remindTime Requested!'}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    must_key_startIndex = [
        (None,),
        ('',)
    ]

    @parameterized.expand(must_key_startIndex)
    def testCase_09(self, param):
        """查看日历下便签删除四个必填字段的key"""
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
            'startIndex': param,
            'rows': 10

        }

        res = self.apiRequests.note_post(self.host + self.getNotesRemind, self.userId, self.sid, body)
        self.assertEqual(200, res.status_code)
        expected = {'responseTime': 0, 'webNotes': list}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_10(self):
        """查看日历下便签删除四个必填字段的key"""
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
        body.pop('startIndex')

        res = self.apiRequests.note_post(self.host + self.getNotesRemind, self.userId, self.sid, body)
        self.assertEqual(200, res.status_code)
        expected = {'responseTime': 0, 'webNotes': list}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    startIndex = [(-1,), (1.5,)]

    @parameterized.expand(startIndex)
    def testCase_11(self, param):
        """查看日历下便签删除四个必填字段的key"""
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
            'startIndex': param,
            'rows': 10

        }

        res = self.apiRequests.note_post(self.host + self.getNotesRemind, self.userId, self.sid, body)
        self.assertEqual(200, res.status_code)
        expected = {'responseTime': 0, 'webNotes': list}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    startIndex = [
        (-2147483648,)
    ]

    @parameterized.expand(startIndex)
    def testCase_12(self, param):
        """查看日历下便签删除四个必填字段的key"""
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
            'startIndex': param,
            'rows': 10

        }

        res = self.apiRequests.note_post(self.host + self.getNotesRemind, self.userId, self.sid, body)
        self.assertEqual(200, res.status_code)
        expected = {'responseTime': 0, 'webNotes': list}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    startIndex = [
        (2147483648,)
    ]

    @parameterized.expand(startIndex)
    def testCase_13(self, param):
        """查看日历下便签删除四个必填字段的key"""
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
            'startIndex': param,
            'rows': 10

        }

        res = self.apiRequests.note_post(self.host + self.getNotesRemind, self.userId, self.sid, body)
        self.assertEqual(500, res.status_code)
        expected = {'errorCode': -7, 'errorMsg': ''}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    startIndex = ['1', "1"]

    @parameterized.expand(startIndex)
    def testCase_14(self, param):
        """查看日历下便签删除四个必填字段的key"""
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
            'startIndex': param,
            'rows': 10

        }

        res = self.apiRequests.note_post(self.host + self.getNotesRemind, self.userId, self.sid, body)
        self.assertEqual(200, res.status_code)
        expected = {'responseTime': 0, 'webNotes': list}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    must_key_rows = [
        (None,),
        ('',)
    ]

    @parameterized.expand(must_key_rows)
    def testCase_15(self, param):
        """查看日历下便签删除四个必填字段的key"""
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
            'rows': param

        }

        res = self.apiRequests.note_post(self.host + self.getNotesRemind, self.userId, self.sid, body)
        self.assertEqual(200, res.status_code)
        expected = {'responseTime': 0, 'webNotes': list}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_16(self):
        """查看日历下便签删除四个必填字段的key"""
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
        body.pop('rows')

        res = self.apiRequests.note_post(self.host + self.getNotesRemind, self.userId, self.sid, body)
        self.assertEqual(200, res.status_code)
        expected = {'responseTime': 0, 'webNotes': list}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    rows = [(-1,), (1.5,)]

    @parameterized.expand(rows)
    def testCase_17(self, param):
        """查看日历下便签删除四个必填字段的key"""
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
            'rows': param

        }

        res = self.apiRequests.note_post(self.host + self.getNotesRemind, self.userId, self.sid, body)
        self.assertEqual(200, res.status_code)
        expected = {'responseTime': 0, 'webNotes': list}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    row = [
        (-2147483648,)
    ]

    @parameterized.expand(row)
    def testCase_18(self, param):
        """查看日历下便签删除四个必填字段的key"""
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
            'rows': param

        }

        res = self.apiRequests.note_post(self.host + self.getNotesRemind, self.userId, self.sid, body)
        self.assertEqual(200, res.status_code)
        expected = {'responseTime': 0, 'webNotes': list}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    row = [
        (2147483648,)
    ]

    @parameterized.expand(row)
    def testCase_19(self, param):
        """查看日历下便签删除四个必填字段的key"""
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
            'rows': param

        }

        res = self.apiRequests.note_post(self.host + self.getNotesRemind, self.userId, self.sid, body)
        self.assertEqual(500, res.status_code)
        expected = {'errorCode': -7, 'errorMsg': ''}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    row = ['1', "1"]

    @parameterized.expand(row)
    def testCase_20(self, param):
        """查看日历下便签删除四个必填字段的key"""
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
            'rows': param

        }

        res = self.apiRequests.note_post(self.host + self.getNotesRemind, self.userId, self.sid, body)
        self.assertEqual(200, res.status_code)
        expected = {'responseTime': 0, 'webNotes': list}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_21(self):
        """查看日历下便签删除四个必填字段的key"""
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

        res = self.apiRequests.note_post(self.host + self.getNotesRemind, self.userId, self.notPresentSid, body)
        self.assertEqual(401, res.status_code)
        expected = {'errorCode': -2010, 'errorMsg': ''}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_22(self):
        """查看日历下便签删除四个必填字段的key"""
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
        new_header = {
            'Content-type': 'application/json',
            'X-user-key': str(self.userId),
            'Cookie': f'wps_sid={self.sid}'

        }
        new_header.pop('Cookie')

        res = self.apiRequests.note_post(self.host + self.getNotesRemind, self.userId, self.sid, body, new_header)
        self.assertEqual(401, res.status_code)
        expected = {'errorCode': -2009, 'errorMsg': ''}
        self.outPutResult.check_out(expected=expected, actual=res.json())
