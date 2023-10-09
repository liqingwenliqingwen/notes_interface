import time
import unittest

from business.apiRequest import ApiRequests
from business.generateNote import GenerateNote
from business.wipeNote import WipeNote
from common.caseLog import step, class_case_log
from common.checkResult import CheckResult
from common.yamlOperator import YamlOperator

@class_case_log
class TestCaseSetNoteGroupHandle(unittest.TestCase):
    apiRequests = ApiRequests()
    wipeNote = WipeNote()
    generateNote = GenerateNote()
    outPutResult = CheckResult()
    envConfig = YamlOperator().env_config()
    setNoteGroupConfig = YamlOperator.api_data_config('setNoteGroup')
    host = envConfig['host']
    userId = envConfig['user_id']
    userIdB = envConfig['user_idB']
    sid = envConfig['sid']
    sidB = envConfig['sidB']
    setNoteGroupPath = setNoteGroupConfig['setNoteGroupPath']
    getNoteGroupPath = setNoteGroupConfig['getNoteGroupPath']

    key = envConfig['key'].encode('utf-8')
    iv = envConfig['iv'].encode('utf-8')

    def setUp(self) -> None:
        """清除数据"""
        self.wipeNote.wipeNote(self.userId, self.sid)

    def testCase_01_setNoteGroup_authority(self):
        """用户A新增用户B下的便签分组"""
        step('STEP1:用户A下新增用户B下的便签分组')
        groupId = str(int(time.time() * 1000)) + '_groupId'
        body = {
            'groupId': groupId,
            'groupName': '新增分组' + groupId,
            'order': 0
        }
        res = self.apiRequests.note_post(self.host + self.setNoteGroupPath, self.userIdB, self.sid, body)
        self.assertEqual(412, res.status_code)
        expected = {'errorCode': -1011, 'errorMsg': 'user change!'}
        self.outPutResult.check_out(expected=expected, actual=res.json())
