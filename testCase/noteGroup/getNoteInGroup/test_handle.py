import time
import unittest

from business.apiRequest import ApiRequests
from business.generateNote import GenerateNote
from business.wipeNote import WipeNote
from business.wipeNoteGroup import WipeNoteGroup
from common.AES_tool import encry
from common.caseLog import step, class_case_log
from common.checkResult import CheckResult
from common.yamlOperator import YamlOperator


@class_case_log
class TestCaseGetNoteInGroupHandle(unittest.TestCase):
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

    def testCase_01(self):
        """查询分组下数据便签"""
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
            'startIndex': 0,
            'rows': 50

        }
        res = self.apiRequests.note_post(self.host + self.getNoteInGroupPath, self.userId, self.sid, body)
        expected = {'responseTime': int, 'webNotes': [
            {'noteId': noteId, 'createTime': int, 'star': 0, 'remindTime': 0, 'remindType': 0,
             'infoVersion': contentVersion, 'infoUpdateTime': int, 'groupId': groupId,
             'title': title, 'summary': summary, 'thumbnail': None,
             'contentVersion': contentVersion, 'contentUpdateTime': int}]}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_02(self):
        """查询分组下用户A下查询用户B下的便签分组"""
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
            'startIndex': 0,
            'rows': 50

        }
        res = self.apiRequests.note_post(self.host + self.getNoteInGroupPath, self.userIdB, self.sid, body)
        self.assertEqual(412, res.status_code)
        expected = {'errorCode': -1011, 'errorMsg': 'user change!'}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_03(self):
        """查询分组下数据便签rows限制"""

        step('STEP1:新增一个分组便签')

        groupId = str(int(time.time() * 1000)) + '_groupId'
        body = {
            'groupId': groupId,
            'groupName': '新增分组' + groupId,
            'order': 0
        }
        self.apiRequests.note_post(self.host + self.setNoteGroupPath, self.userId, self.sid, body)
        step('STEP2:创建2个便签主体+内容')
        for item in range(2):
            noteId = str(int(time.time() * 1000)) + '_noteId' + str(item)
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
            'startIndex': 0,
            'rows': 1

        }
        res = self.apiRequests.note_post(self.host + self.getNoteInGroupPath, self.userId, self.sid, body)
        self.assertEqual(1, len(res.json()['webNotes']))
        expected = {'responseTime': int, 'webNotes': [
            {'noteId': str, 'createTime': int, 'star': 0, 'remindTime': 0,
             'remindType': 0, 'infoVersion': 1, 'infoUpdateTime': int, 'groupId': groupId,
             'title': 'aiXhXKtVDyR9/L7DJTxhLg==', 'summary': '4ZTUOD5fyvtLawr5pV/D3w==', 'thumbnail': None,
             'contentVersion': 1, 'contentUpdateTime': int}]}
        self.outPutResult.check_out(expected=expected, actual=res.json())
