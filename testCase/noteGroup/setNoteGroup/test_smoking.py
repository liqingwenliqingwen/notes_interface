import time
import unittest

from business.apiRequest import ApiRequests
from business.generateNote import GenerateNote
from business.wipeNote import WipeNote
from common.caseLog import step, info, class_case_log
from common.checkResult import CheckResult
from common.yamlOperator import YamlOperator


@class_case_log
class TestCaseSetNoteGroupSmoking(unittest.TestCase):
    apiRequests = ApiRequests()
    wipeNote = WipeNote()
    generateNote = GenerateNote()
    outPutResult = CheckResult()
    envConfig = YamlOperator().env_config()
    setNoteGroupConfig = YamlOperator.api_data_config('setNoteGroup')
    host = envConfig['host']
    userId = envConfig['user_id']
    sid = envConfig['sid']
    setNoteGroupPath = setNoteGroupConfig['setNoteGroupPath']
    getNoteGroupPath = setNoteGroupConfig['getNoteGroupPath']

    key = envConfig['key'].encode('utf-8')
    iv = envConfig['iv'].encode('utf-8')

    def setUp(self) -> None:
        """清除数据"""
        self.wipeNote.wipeNote(self.userId, self.sid)

    def testCase(self):
        """新增便签数据冒烟"""
        step('STEP1:新增一个分组便签')
        groupId = str(int(time.time() * 1000)) + '_groupId'
        body = {
            'groupId': groupId,
            'groupName': '新增分组' + groupId,
            'order': 0
        }
        self.apiRequests.note_post(self.host + self.setNoteGroupPath, self.userId, self.sid, body)
        step('STEP2:获取分组便签')
        body = {}
        res = self.apiRequests.note_post(self.host + self.getNoteGroupPath, self.userId, self.sid, body)
        groupNameRes = [item['groupName'] for item in res.json()['noteGroups']]
        for item in range(len(groupNameRes)):
            if (groupNameRes[item]) == '新增分组' + groupId:
                info('新增的分组在便签列表中')
