import time
import unittest

from business.apiRequest import ApiRequests
from business.wipeNote import WipeNote
from common.AES_tool import encry
from common.caseLog import step, class_case_log, info
from common.checkResult import CheckResult
from common.yamlOperator import YamlOperator


@class_case_log
class TestCaseSetNoteInfoSmoking(unittest.TestCase):
    apiRequest = ApiRequests()
    outPutResult = CheckResult()
    envConfig = YamlOperator().env_config()
    setNoteInfoConfig = YamlOperator.api_data_config('setNoteInfo')

    userId = envConfig['user_id']
    sid = envConfig['sid']

    host = envConfig['host']

    key = envConfig['key'].encode('utf-8')
    iv = envConfig['iv'].encode('utf-8')

    addNoteGroupPath = setNoteInfoConfig['addNoteGroupPath']
    addNoteContentPath = setNoteInfoConfig['addNoteContentPath']
    path = setNoteInfoConfig['path']
    getNoteGroupPath = setNoteInfoConfig['get_note_group_path']

    getNotePagePath = '/v3/notesvr/user/{}/home/startindex/{}/rows/{}/notes'.format(userId, 0, 50)

    def setUp(self) -> None:
        step('STEP1:清空数据')
        wipeNote = WipeNote()
        wipeNote.wipeNote(self.userId, self.sid)

    def testCase_01(self):
        """
        新增便签主体主流程
        :return:
        """
        step('STEP1:新建分组')
        group_id = str(int(time.time() * 1000)) + '_group_id'
        body = {
            'groupId': group_id,
            'groupName': '新建分组1',
            'order': 1,
        }
        self.apiRequest.note_post(self.host + self.addNoteGroupPath, self.userId, self.sid, body)
        step('STEP3:新增便签主体')
        note_id = str(int(time.time() * 1000)) + '_noteId'
        remindTime = 1727698720  # 2024-09-30 20:18:40
        body = {
            'noteId': note_id,
            'star': 0,
            # 'remindTime': remindTime,
            'NotesRemind': 0,
            'groupId': group_id

        }
        res = self.apiRequest.note_post(self.host + self.path, self.userId, self.sid, body)
        contentVersion = res.json()['infoVersion']
        step('STEP4:新增便签内容')

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

        self.apiRequest.note_post(self.host + self.addNoteContentPath, self.userId, self.sid, body)

        step('Step5:校验code')
        self.assertEqual(200, res.status_code)
        step('STEP6:获取分组下便签列表')
        body = {
            'groupId': group_id
        }
        res = self.apiRequest.note_post(self.host + self.getNoteGroupPath, self.userId, self.sid, body)
        info(res.json())
        getPageNoteId = [item['noteId'] for item in res.json()['webNotes']]
        self.assertEqual([note_id], getPageNoteId)
