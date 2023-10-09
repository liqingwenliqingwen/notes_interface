import time
import unittest

from business.apiRequest import ApiRequests
from business.generateNote import GenerateNote
from business.wipeNote import WipeNote
from business.wipeNoteGroup import WipeNoteGroup
from common.caseLog import step, class_case_log
from common.checkResult import CheckResult
from common.yamlOperator import YamlOperator


@class_case_log
class TestCaseDeleteNoteGroupInput(unittest.TestCase):
    apiRequests = ApiRequests()
    wipeNote = WipeNote()
    wipeNoteGroup = WipeNoteGroup()
    generateNote = GenerateNote()
    outPutResult = CheckResult()
    envConfig = YamlOperator().env_config()
    deleteNoteGroupConfig = YamlOperator.api_data_config('deleteNoteGroup')
    host = envConfig['host']
    userId = envConfig['user_id']
    sid = envConfig['sid']
    setNoteGroupPath = deleteNoteGroupConfig['addNoteGroupPath']
    getNoteGroupPath = deleteNoteGroupConfig['getNoteGroupPath']
    delNoteGroup = deleteNoteGroupConfig['delNoteGroup']

    key = envConfig['key'].encode('utf-8')
    iv = envConfig['iv'].encode('utf-8')

    def setUp(self) -> None:
        """清除数据"""
        self.wipeNoteGroup.wipeNoteGroup(self.userId, self.sid)
        self.wipeNote.wipeNote(self.userId, self.sid)

    def testCase_01_deleteNoteGroup_smoking(self):
        """删除便签分组冒烟"""
        step('STEP1:新增一个分组便签')
        groupId = str(int(time.time() * 1000)) + '_groupId'
        body = {
            'groupId': groupId,
            'groupName': '新增分组' + groupId,
            'order': 0
        }
        self.apiRequests.note_post(self.host + self.setNoteGroupPath, self.userId, self.sid, body)
        step('STEP2:删除便签分组')
        body = {
            'groupId': groupId
        }
        res = self.apiRequests.note_post(self.host + self.delNoteGroup, self.userId, self.sid, body)
        self.assertEqual(200, res.status_code)
        expected = {'responseTime': int}
        self.outPutResult.check_out(expected=expected, actual=res.json())
        step('STEP3:获取便签分组')
        res = self.apiRequests.note_post(self.host + self.getNoteGroupPath, self.userId, self.sid, body)
        # for item in res.json()['noteGroups']:
        #     self.assertIn(groupId, item['groupId'])
