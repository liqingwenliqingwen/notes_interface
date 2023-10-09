import time
import unittest

from business.apiRequest import ApiRequests
from business.generateNote import GenerateNote
from business.wipeNote import WipeNote
from business.wipeNoteGroup import WipeNoteGroup
from common.AES_tool import encry
from common.caseLog import step, info, class_case_log
from common.checkResult import CheckResult
from common.yamlOperator import YamlOperator


@class_case_log
class TestCaseGetNoteInGroupSmoking(unittest.TestCase):
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

    def testCase_01_getNoteInGroup_smoking(self):
        """查询分组下便签"""
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
        noteIdRes = [item['noteId'] for item in res.json()['webNotes']]
        step('STEP5:校验noteId')
        if noteIdRes[0] == noteId:
            info('noteId查询成功')
        step('STEP6:校验groupId')
        groupIdRes = [item['groupId'] for item in res.json()['webNotes']]
        if groupIdRes[0] == groupId:
            info('groupId查询成功')
