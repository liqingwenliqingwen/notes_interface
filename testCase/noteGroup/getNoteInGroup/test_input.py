import time
import unittest

from parameterized import parameterized

from business.apiRequest import ApiRequests
from business.generateNote import GenerateNote
from business.wipeNote import WipeNote
from business.wipeNoteGroup import WipeNoteGroup
from common.AES_tool import encry
from common.caseLog import step, class_case_log
from common.checkResult import CheckResult
from common.yamlOperator import YamlOperator


@class_case_log
class TestCaseGetNoteInGroupInput(unittest.TestCase):
    apiRequests = ApiRequests()
    wipeNote = WipeNote()
    wipeNoteGroup = WipeNoteGroup()
    generateNote = GenerateNote()
    outPutResult = CheckResult()
    envConfig = YamlOperator().env_config()
    getNoteInGroupConfig = YamlOperator.api_data_config('getNoteInGroup')
    host = envConfig['host']
    userId = envConfig['user_id']
    userIdB = envConfig['user_idB']
    notPresentSid = envConfig['notPresentSid']
    sidB = envConfig['sidB']
    sid = envConfig['sid']
    setNoteGroupPath = getNoteInGroupConfig['addNoteGroupPath']

    setNoteInfoPath = getNoteInGroupConfig['setNoteInfoPath']
    addNoteContentPath = getNoteInGroupConfig['addNoteContentPath']
    getNoteInGroupPath = getNoteInGroupConfig['getNoteInGroupPath']

    key = envConfig['key'].encode('utf-8')
    iv = envConfig['iv'].encode('utf-8')

    def setUp(self) -> None:
        """清除数据"""
        # self.wipeNoteGroup.testCase_01_wipeNoteGroup(self.userId, self.sid)
        self.wipeNote.wipeNote(self.userId, self.sid)

    must_key = [
        (None,),
        ('',)
    ]

    @parameterized.expand(must_key)
    def testCase_01(self, param):
        """查询分组下便签input _groupId 1,None 2,''"""
        step('STEP1:新增一个分组便签')
        noteId = str(int(time.time() * 1000)) + '_noteId'
        groupId = str(int(time.time() * 1000)) + '_groupId'
        body = {
            'groupId': groupId,
            'groupName': '新增分组' + groupId,
            'order': 0
        }
        self.apiRequests.note_post(self.host + self.setNoteGroupPath, self.userId, self.sid, body)
        step('STEP2:新建一个便签主体')
        body = {
            'noteId': noteId,
            'groupId': groupId
        }
        res = self.apiRequests.note_post(self.host + self.setNoteInfoPath, self.userId, self.sid, body)
        contentVersion = res.json()['infoVersion']
        step('STEP3:新建便签内容')
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

        self.apiRequests.note_post(self.host + self.addNoteContentPath, self.userId, self.sid, body)
        step('STEP4:查看分组下便签')
        body = {
            'groupId': param
        }
        res = self.apiRequests.note_post(self.host + self.getNoteInGroupPath, self.userId, self.sid, body)
        self.assertEqual(500, res.status_code)
        expected = {'errorCode': -7, 'errorMsg': '参数不合法！'}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_02(self):
        """查询分组下便签input _groupId 1,None 2,''"""
        step('STEP1:新增一个分组便签')
        noteId = str(int(time.time() * 1000)) + '_noteId'
        groupId = str(int(time.time() * 1000)) + '_groupId'
        body = {
            'groupId': groupId,
            'groupName': '新增分组' + groupId,
            'order': 0
        }
        self.apiRequests.note_post(self.host + self.setNoteGroupPath, self.userId, self.sid, body)
        step('STEP2:新建一个便签主体')
        body = {
            'noteId': noteId,
            'groupId': groupId
        }
        res = self.apiRequests.note_post(self.host + self.setNoteInfoPath, self.userId, self.sid, body)
        contentVersion = res.json()['infoVersion']
        step('STEP3:新建便签内容')
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

        self.apiRequests.note_post(self.host + self.addNoteContentPath, self.userId, self.sid, body)
        step('STEP4:查看分组下便签')
        body = {
            'groupId': groupId
        }
        body.pop('groupId')
        res = self.apiRequests.note_post(self.host + self.getNoteInGroupPath, self.userId, self.sid, body)
        self.assertEqual(500, res.status_code)
        expected = {'errorCode': -7, 'errorMsg': '参数不合法！'}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_03(self):
        """查询分组下便签input _groupId 1,中文 ''"""
        step('STEP1:新增一个分组便签')
        noteId = str(int(time.time() * 1000)) + '_noteId'
        groupId = str(int(time.time() * 1000)) + '_groupId'
        body = {
            'groupId': groupId,
            'groupName': '新增分组' + groupId,
            'order': 0
        }
        self.apiRequests.note_post(self.host + self.setNoteGroupPath, self.userId, self.sid, body)
        step('STEP2:新建一个便签主体')
        body = {
            'noteId': noteId,
            'groupId': groupId
        }
        res = self.apiRequests.note_post(self.host + self.setNoteInfoPath, self.userId, self.sid, body)
        contentVersion = res.json()['infoVersion']
        step('STEP3:新建便签内容')
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

        self.apiRequests.note_post(self.host + self.addNoteContentPath, self.userId, self.sid, body)
        step('STEP4:查看分组下便签')
        body = {
            'groupId': '你好'
        }
        res = self.apiRequests.note_post(self.host + self.getNoteInGroupPath, self.userId, self.sid, body)
        self.assertEqual(500, res.status_code)
        expected = {'errorCode': -7, 'errorMsg': str}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_04(self):
        """查询分组下便签input _groupId 1,超长参数''"""
        step('STEP1:新增一个分组便签')
        noteId = str(int(time.time() * 1000)) + '_noteId'
        groupId = str(int(time.time() * 1000)) + '_groupId'
        body = {
            'groupId': groupId,
            'groupName': '新增分组' + groupId,
            'order': 0
        }
        self.apiRequests.note_post(self.host + self.setNoteGroupPath, self.userId, self.sid, body)
        step('STEP2:新建一个便签主体')
        body = {
            'noteId': noteId,
            'groupId': groupId
        }
        res = self.apiRequests.note_post(self.host + self.setNoteInfoPath, self.userId, self.sid, body)
        contentVersion = res.json()['infoVersion']
        step('STEP3:新建便签内容')
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

        self.apiRequests.note_post(self.host + self.addNoteContentPath, self.userId, self.sid, body)
        step('STEP4:查看分组下便签')
        body = {
            'groupId': '999999999999999999999999999999999999999999999999999999999999999999999999999999999999999'
        }
        res = self.apiRequests.note_post(self.host + self.getNoteInGroupPath, self.userId, self.sid, body)
        self.assertEqual(500, res.status_code)
        expected = {'errorCode': -7, 'errorMsg': '参数不合法！'}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    must_key_contains_special_characters = ['!!!', '@@@']

    @parameterized.expand(must_key_contains_special_characters)
    def testCase_05(self, param):
        """查询分组下便签input _groupId 1,特殊字符''"""
        step('STEP1:新增一个分组便签')
        noteId = str(int(time.time() * 1000)) + '_noteId'
        groupId = str(int(time.time() * 1000)) + '_groupId'
        body = {
            'groupId': groupId,
            'groupName': '新增分组' + groupId,
            'order': 0
        }
        self.apiRequests.note_post(self.host + self.setNoteGroupPath, self.userId, self.sid, body)
        step('STEP2:新建一个便签主体')
        body = {
            'noteId': noteId,
            'groupId': groupId
        }
        res = self.apiRequests.note_post(self.host + self.setNoteInfoPath, self.userId, self.sid, body)
        contentVersion = res.json()['infoVersion']
        step('STEP3:新建便签内容')
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

        self.apiRequests.note_post(self.host + self.addNoteContentPath, self.userId, self.sid, body)
        step('STEP4:查看分组下便签')
        body = {
            'groupId': param
        }
        res = self.apiRequests.note_post(self.host + self.getNoteInGroupPath, self.userId, self.sid, body)
        self.assertEqual(200, res.status_code)
        expected = {'responseTime': 0, 'webNotes': []}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    optional_startIndex = [
        (None,),
        ('',)
    ]

    @parameterized.expand(optional_startIndex)
    def testCase_06(self, param):
        """查询分组下便签input _groupId 1,特殊字符''"""
        step('STEP1:新增一个分组便签')
        noteId = str(int(time.time() * 1000)) + '_noteId'
        groupId = str(int(time.time() * 1000)) + '_groupId'
        body = {
            'groupId': groupId,
            'groupName': '新增分组' + groupId,
            'order': 0
        }
        self.apiRequests.note_post(self.host + self.setNoteGroupPath, self.userId, self.sid, body)
        step('STEP2:新建一个便签主体')
        body = {
            'noteId': noteId,
            'groupId': groupId
        }
        res = self.apiRequests.note_post(self.host + self.setNoteInfoPath, self.userId, self.sid, body)
        contentVersion = res.json()['infoVersion']
        step('STEP3:新建便签内容')
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

        self.apiRequests.note_post(self.host + self.addNoteContentPath, self.userId, self.sid, body)
        step('STEP4:查看分组下便签')
        body = {
            'groupId': groupId,
            'startIndex': param
        }
        res = self.apiRequests.note_post(self.host + self.getNoteInGroupPath, self.userId, self.sid, body)
        self.assertEqual(200, res.status_code)
        expected = {'responseTime': 0, 'webNotes': list}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    optional_startIndex = [-1, 1.5]

    @parameterized.expand(optional_startIndex)
    def testCase_07(self, param):
        """查询分组下便签input optional_startIndex 1,负数2，小数点''"""
        step('STEP1:新增一个分组便签')
        noteId = str(int(time.time() * 1000)) + '_noteId'
        groupId = str(int(time.time() * 1000)) + '_groupId'
        body = {
            'groupId': groupId,
            'groupName': '新增分组' + groupId,
            'order': 0
        }
        self.apiRequests.note_post(self.host + self.setNoteGroupPath, self.userId, self.sid, body)
        step('STEP2:新建一个便签主体')
        body = {
            'noteId': noteId,
            'groupId': groupId
        }
        res = self.apiRequests.note_post(self.host + self.setNoteInfoPath, self.userId, self.sid, body)
        contentVersion = res.json()['infoVersion']
        step('STEP3:新建便签内容')
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

        self.apiRequests.note_post(self.host + self.addNoteContentPath, self.userId, self.sid, body)
        step('STEP4:查看分组下便签')
        body = {
            'groupId': groupId,
            'startIndex': param
        }
        res = self.apiRequests.note_post(self.host + self.getNoteInGroupPath, self.userId, self.sid, body)
        self.assertEqual(200, res.status_code)
        expected = {'responseTime': 0, 'webNotes': []}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    optional_startIndex_str = ['1', "1"]

    @parameterized.expand(optional_startIndex_str)
    def testCase_08(self, param):
        """查询分组下便签input optional_startIndex 1,负数2，小数点''"""
        step('STEP1:新增一个分组便签')
        noteId = str(int(time.time() * 1000)) + '_noteId'
        groupId = str(int(time.time() * 1000)) + '_groupId'
        body = {
            'groupId': groupId,
            'groupName': '新增分组' + groupId,
            'order': 0
        }
        self.apiRequests.note_post(self.host + self.setNoteGroupPath, self.userId, self.sid, body)
        step('STEP2:新建一个便签主体')
        body = {
            'noteId': noteId,
            'groupId': groupId
        }
        res = self.apiRequests.note_post(self.host + self.setNoteInfoPath, self.userId, self.sid, body)
        contentVersion = res.json()['infoVersion']
        step('STEP3:新建便签内容')
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

        self.apiRequests.note_post(self.host + self.addNoteContentPath, self.userId, self.sid, body)
        step('STEP4:查看分组下便签')
        body = {
            'groupId': groupId,
            'startIndex': param
        }
        res = self.apiRequests.note_post(self.host + self.getNoteInGroupPath, self.userId, self.sid, body)
        self.assertEqual(200, res.status_code)
        expected = {'responseTime': 0, 'webNotes': []}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    optional_startIndex_max = [
        (2147483648,)
    ]

    @parameterized.expand(optional_startIndex_max)
    def testCase_09(self, param):
        """查询分组下便签input optional_startIndex 1,负数2，小数点''"""
        step('STEP1:新增一个分组便签')
        noteId = str(int(time.time() * 1000)) + '_noteId'
        groupId = str(int(time.time() * 1000)) + '_groupId'
        body = {
            'groupId': groupId,
            'groupName': '新增分组' + groupId,
            'order': 0
        }
        self.apiRequests.note_post(self.host + self.setNoteGroupPath, self.userId, self.sid, body)
        step('STEP2:新建一个便签主体')
        body = {
            'noteId': noteId,
            'groupId': groupId
        }
        res = self.apiRequests.note_post(self.host + self.setNoteInfoPath, self.userId, self.sid, body)
        contentVersion = res.json()['infoVersion']
        step('STEP3:新建便签内容')
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

        self.apiRequests.note_post(self.host + self.addNoteContentPath, self.userId, self.sid, body)
        step('STEP4:查看分组下便签')
        body = {
            'groupId': groupId,
            'startIndex': param
        }
        res = self.apiRequests.note_post(self.host + self.getNoteInGroupPath, self.userId, self.sid, body)
        self.assertEqual(500, res.status_code)
        expected = {'errorCode': -7, 'errorMsg': ''}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    optional_rows = [
        (None,),
        ('',)
    ]

    @parameterized.expand(optional_rows)
    def testCase_10(self, param):
        """查询分组下便签input optional_startIndex 1,负数2，小数点''"""
        step('STEP1:新增一个分组便签')
        noteId = str(int(time.time() * 1000)) + '_noteId'
        groupId = str(int(time.time() * 1000)) + '_groupId'
        body = {
            'groupId': groupId,
            'groupName': '新增分组' + groupId,
            'order': 0
        }
        self.apiRequests.note_post(self.host + self.setNoteGroupPath, self.userId, self.sid, body)
        step('STEP2:新建一个便签主体')
        body = {
            'noteId': noteId,
            'groupId': groupId
        }
        res = self.apiRequests.note_post(self.host + self.setNoteInfoPath, self.userId, self.sid, body)
        contentVersion = res.json()['infoVersion']
        step('STEP3:新建便签内容')
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

        self.apiRequests.note_post(self.host + self.addNoteContentPath, self.userId, self.sid, body)
        step('STEP4:查看分组下便签')
        body = {
            'groupId': groupId,
            'rows': param
        }
        res = self.apiRequests.note_post(self.host + self.getNoteInGroupPath, self.userId, self.sid, body)
        self.assertEqual(200, res.status_code)
        expected = {'responseTime': int, 'webNotes': list}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    optional_rows_intMax = [
        (2147483648,)
    ]

    @parameterized.expand(optional_rows_intMax)
    def testCase_11(self, param):
        """查询分组下便签input optional_startIndex 1,负数2，小数点''"""
        step('STEP1:新增一个分组便签')
        noteId = str(int(time.time() * 1000)) + '_noteId'
        groupId = str(int(time.time() * 1000)) + '_groupId'
        body = {
            'groupId': groupId,
            'groupName': '新增分组' + groupId,
            'order': 0
        }
        self.apiRequests.note_post(self.host + self.setNoteGroupPath, self.userId, self.sid, body)
        step('STEP2:新建一个便签主体')
        body = {
            'noteId': noteId,
            'groupId': groupId
        }
        res = self.apiRequests.note_post(self.host + self.setNoteInfoPath, self.userId, self.sid, body)
        contentVersion = res.json()['infoVersion']
        step('STEP3:新建便签内容')
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

        self.apiRequests.note_post(self.host + self.addNoteContentPath, self.userId, self.sid, body)
        step('STEP4:查看分组下便签')
        body = {
            'groupId': groupId,
            'rows': param
        }
        res = self.apiRequests.note_post(self.host + self.getNoteInGroupPath, self.userId, self.sid, body)
        self.assertEqual(500, res.status_code)
        expected = {'errorCode': -7, 'errorMsg': ''}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    optional_rows_decimal = [10.5, -10]

    @parameterized.expand(optional_rows)
    def testCase_12(self, param):
        """查询分组下便签input optional_startIndex 1,负数2，小数点''"""
        step('STEP1:新增一个分组便签')
        noteId = str(int(time.time() * 1000)) + '_noteId'
        groupId = str(int(time.time() * 1000)) + '_groupId'
        body = {
            'groupId': groupId,
            'groupName': '新增分组' + groupId,
            'order': 0
        }
        self.apiRequests.note_post(self.host + self.setNoteGroupPath, self.userId, self.sid, body)
        step('STEP2:新建一个便签主体')
        body = {
            'noteId': noteId,
            'groupId': groupId
        }
        res = self.apiRequests.note_post(self.host + self.setNoteInfoPath, self.userId, self.sid, body)
        contentVersion = res.json()['infoVersion']
        step('STEP3:新建便签内容')
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

        self.apiRequests.note_post(self.host + self.addNoteContentPath, self.userId, self.sid, body)
        step('STEP4:查看分组下便签')
        body = {
            'groupId': groupId,
            'rows': param
        }
        res = self.apiRequests.note_post(self.host + self.getNoteInGroupPath, self.userId, self.sid, body)
        self.assertEqual(200, res.status_code)
        expected = {'responseTime': int, 'webNotes': list}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    optional_rows_str = ["10", '10']

    @parameterized.expand(optional_rows_str)
    def testCase_13(self, param):
        """查询分组下便签input optional_startIndex 1,负数2，小数点''"""
        step('STEP1:新增一个分组便签')
        noteId = str(int(time.time() * 1000)) + '_noteId'
        groupId = str(int(time.time() * 1000)) + '_groupId'
        body = {
            'groupId': groupId,
            'groupName': '新增分组' + groupId,
            'order': 0
        }
        self.apiRequests.note_post(self.host + self.setNoteGroupPath, self.userId, self.sid, body)
        step('STEP2:新建一个便签主体')
        body = {
            'noteId': noteId,
            'groupId': groupId
        }
        res = self.apiRequests.note_post(self.host + self.setNoteInfoPath, self.userId, self.sid, body)
        contentVersion = res.json()['infoVersion']
        step('STEP3:新建便签内容')
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

        self.apiRequests.note_post(self.host + self.addNoteContentPath, self.userId, self.sid, body)
        step('STEP4:查看分组下便签')
        body = {
            'groupId': groupId,
            'rows': param
        }
        res = self.apiRequests.note_post(self.host + self.getNoteInGroupPath, self.userId, self.sid, body)
        self.assertEqual(200, res.status_code)
        expected = {'responseTime': int, 'webNotes': list}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_14(self):
        """查询分组下便签身份验证''"""
        step('STEP1:新增一个分组便签')
        noteId = str(int(time.time() * 1000)) + '_noteId'
        groupId = str(int(time.time() * 1000)) + '_groupId'
        body = {
            'groupId': groupId,
            'groupName': '新增分组' + groupId,
            'order': 0
        }
        self.apiRequests.note_post(self.host + self.setNoteGroupPath, self.userId, self.sid, body)
        step('STEP2:新建一个便签主体')
        body = {
            'noteId': noteId,
            'groupId': groupId
        }
        res = self.apiRequests.note_post(self.host + self.setNoteInfoPath, self.userId, self.sid, body)
        contentVersion = res.json()['infoVersion']
        step('STEP3:新建便签内容')
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

        self.apiRequests.note_post(self.host + self.addNoteContentPath, self.userId, self.sid, body)
        step('STEP4:查看分组下便签')
        body = {
            'groupId': groupId,
            'rows': 50
        }
        res = self.apiRequests.note_post(self.host + self.getNoteInGroupPath, self.userId, self.sidB, body)
        self.assertEqual(412, res.status_code)
        expected = {'errorCode': -1011, 'errorMsg': 'user change!'}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_15(self):
        """查询分组下便签身份验证''"""
        step('STEP1:新增一个分组便签')
        noteId = str(int(time.time() * 1000)) + '_noteId'
        groupId = str(int(time.time() * 1000)) + '_groupId'
        body = {
            'groupId': groupId,
            'groupName': '新增分组' + groupId,
            'order': 0
        }
        self.apiRequests.note_post(self.host + self.setNoteGroupPath, self.userId, self.sid, body)
        step('STEP2:新建一个便签主体')
        body = {
            'noteId': noteId,
            'groupId': groupId
        }
        res = self.apiRequests.note_post(self.host + self.setNoteInfoPath, self.userId, self.sid, body)
        contentVersion = res.json()['infoVersion']
        step('STEP3:新建便签内容')
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

        self.apiRequests.note_post(self.host + self.addNoteContentPath, self.userId, self.sid, body)
        step('STEP4:查看分组下便签')
        new_header = {
            'Content-Type': 'application/json',
            'X-user-key': str(self.userId),
            'Cookie': f'wps_sid={self.sid}'
        }
        new_header.pop('Cookie')
        body = {
            'groupId': groupId,
            'rows': 50
        }
        res = self.apiRequests.note_post(self.host + self.getNoteInGroupPath, self.userId, self.sidB, body, new_header)
        self.assertEqual(401, res.status_code)
        expected = {'errorCode': -2009, 'errorMsg': ''}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_16(self):
        """查询分组下便签身份验证''"""
        step('STEP1:新增一个分组便签')
        noteId = str(int(time.time() * 1000)) + '_noteId'
        groupId = str(int(time.time() * 1000)) + '_groupId'
        body = {
            'groupId': groupId,
            'groupName': '新增分组' + groupId,
            'order': 0
        }
        self.apiRequests.note_post(self.host + self.setNoteGroupPath, self.userId, self.sid, body)
        step('STEP2:新建一个便签主体')
        body = {
            'noteId': noteId,
            'groupId': groupId
        }
        res = self.apiRequests.note_post(self.host + self.setNoteInfoPath, self.userId, self.sid, body)
        contentVersion = res.json()['infoVersion']
        step('STEP3:新建便签内容')
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

        self.apiRequests.note_post(self.host + self.addNoteContentPath, self.userId, self.sid, body)
        step('STEP4:查看分组下便签')
        new_header = {
            'Content-Type': 'application/json',
            'X-user-key': str(self.userId),
            'Cookie': f'wps_sid={self.sid}'
        }
        new_header.pop('Cookie')
        body = {
            'groupId': groupId,
            'rows': 50
        }
        res = self.apiRequests.note_post(self.host + self.getNoteInGroupPath, self.userId, self.notPresentSid, body,
                                         new_header)
        self.assertEqual(401, res.status_code)
        expected = {'errorCode': -2009, 'errorMsg': ''}
        self.outPutResult.check_out(expected=expected, actual=res.json())
