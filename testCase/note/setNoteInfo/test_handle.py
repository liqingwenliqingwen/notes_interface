import time
import unittest

from parameterized import parameterized

from business.apiRequest import ApiRequests
from business.generateNote import GenerateNote
from business.wipeNote import WipeNote
from common.AES_tool import encry
from common.caseLog import class_case_log, step, info
from common.checkResult import CheckResult
from common.yamlOperator import YamlOperator


@class_case_log
class TestCaseSetNoteInfoHandle(unittest.TestCase):
    apiRequests = ApiRequests()
    outPutResult = CheckResult()
    envConfig = YamlOperator().env_config()

    generateNote = GenerateNote()
    setNoteInfoConfig = YamlOperator().api_data_config('setNoteInfo')

    userId = envConfig['user_id']
    user_idB = envConfig['user_idB']
    sid = envConfig['sid']
    sidB = envConfig['sidB']
    path = setNoteInfoConfig['path']
    notPresentSid = envConfig['notPresentSid']
    wipeNote = WipeNote()

    host = envConfig['host']

    getNotePagePath = '/v3/notesvr/user/{}/home/startindex/{}/rows/{}/notes'.format(userId, 0, 10)
    addNoteContentPath = setNoteInfoConfig['addNoteContentPath']
    getNoteGroupPath = setNoteInfoConfig['get_note_group_path']
    getNotesRemind = setNoteInfoConfig['getNotesRemind']

    key = 'H9n&S@oGohGpV6d7'.encode('utf-8')
    iv = '5150956153345366'.encode('utf-8')

    def setUp(self) -> None:
        """清空数据"""
        self.wipeNote.wipeNote(self.userId, self.sid)

    star_enum = [0, 1]

    @parameterized.expand(star_enum)
    def testCase_01(self, param):
        """star的枚举值0，1"""
        step('STEP1:新建1条便签主体')
        noteId = str(int(time.time() * 1000)) + '_noteId'
        body = {
            'noteId': noteId,
            'star': param
        }
        res = self.apiRequests.note_post(self.host + self.path, self.userId, self.sid, body)
        contentVersion = res.json()['infoVersion']

        step('STEP2:校验code和返回值')
        self.assertEqual(200, res.status_code)
        expected = {'responseTime': int, 'infoVersion': int, 'infoUpdateTime': int}
        self.outPutResult.check_out(expected=expected, actual=res.json())
        step('STEP校验数据：查询首页便签')
        step('STEP3:新建便签内容')

        title = encry('恭喜', self.key, self.iv)
        summary = encry('恭喜发财', self.key, self.iv)
        text_body = encry('zzzzzzzzz', self.key, self.iv)
        body = {
            'noteId': noteId,
            'title': title,
            'summary': summary,
            'body': text_body,
            'localContentVersion': contentVersion,
            'BodyType': 0

        }

        self.apiRequests.note_post(self.host + self.addNoteContentPath, self.userId, self.sid, body)
        step('STEP4:获取首页便签')
        res = self.apiRequests.note_get(self.host + self.getNotePagePath, self.userId, self.sid)
        resStar = [item['star'] for item in res.json()['webNotes']]
        resNoteId = [item['noteId'] for item in res.json()['webNotes']]

        step('新建便签主体的star和查询便签主体的star一致')
        self.assertEqual([noteId], resNoteId)
        self.assertEqual([param], resStar)

    remindType_enum = [0, 1, 2]

    @parameterized.expand(remindType_enum)
    def testCase_02(self, param):
        """remindType的枚举值0,1,2"""
        step('STEP1:新建1条便签主体')
        noteId = str(int(time.time() * 1000)) + '_noteId'
        body = {
            'noteId': noteId,
            'remindTime': 1704072587,
            'remindType': param
        }
        res = self.apiRequests.note_post(self.host + self.path, self.userId, self.sid, body)
        contentVersion = res.json()['infoVersion']

        step('STEP2:新建便签内容')

        title = encry('恭喜', self.key, self.iv)
        summary = encry('恭喜发财', self.key, self.iv)
        text_body = encry('zzzzzzzzz', self.key, self.iv)
        body = {
            'noteId': noteId,
            'title': title,
            'summary': summary,
            'body': text_body,
            'localContentVersion': contentVersion,
            'BodyType': 0

        }

        self.apiRequests.note_post(self.host + self.addNoteContentPath, self.userId, self.sid, body)
        step('STEP4:获取日历下便签')
        body = {
            'remindStartTime': 5387,
            'remindEndTime': 4070914187,
            'startIndex': 0,
            'rows': 100

        }
        res = self.apiRequests.note_post(self.host + self.getNotesRemind, self.userId, self.sid, body)

        noteIds = [item['noteId'] for item in res.json()['webNotes']]
        step('STEP:如果新建的便签主体和日历便签下的便签id相等，判断设置的remindType')
        if noteId == noteIds:
            resRemindType = [item['star'] for item in res.json()['webNotes']]
            info(f'打印的参数为{[param]},{resRemindType}')
            self.assertEqual([param], resRemindType)

    def testCase_03(self):
        """新增重复的noteId"""
        noteId = str(int(time.time() * 1000)) + '_noteId'
        step('STEP1:新增一个不存在的noteId的便签')
        set_body = {
            'noteId': noteId,
            'star': 1

        }
        res = self.apiRequests.note_post(self.host + self.path, self.userId, self.sid, set_body)
        contentVersion = res.json()['infoVersion']
        step('STEP2:新建便签内容')
        title = encry('恭喜', self.key, self.iv)
        summary = encry('恭喜发财', self.key, self.iv)
        text_body = encry('zzzzzzzzz', self.key, self.iv)
        body = {
            'noteId': noteId,
            'title': title,
            'summary': summary,
            'body': text_body,
            'localContentVersion': contentVersion,
            'BodyType': 0

        }

        self.apiRequests.note_post(self.host + self.addNoteContentPath, self.userId, self.sid, body)

        step('STEP2:更新这个新建的noteId便签主体')
        update_body = {
            'noteId': noteId,
            'star': 0

        }
        res = self.apiRequests.note_post(self.host + self.path, self.userId, self.sid, update_body)
        step('STEP3:更新这个便签的便签内容')

        body = {
            'noteId': noteId,
            'title': title,
            'summary': summary,
            'body': text_body,
            'localContentVersion': contentVersion,
            'BodyType': 0

        }
        self.apiRequests.note_post(self.host + self.addNoteContentPath, self.userId, self.sid, body)

        step('STEP4:获取首页便签')
        res = self.apiRequests.note_get(self.host + self.getNotePagePath, self.userId, self.sid)
        noteIds = [item['noteId'] for item in res.json()['webNotes']]
        resStar = [item['star'] for item in res.json()['webNotes']]

        self.assertEqual(200, res.status_code)
        self.assertEqual([noteId], noteIds)
        self.assertEqual([update_body['star']], resStar)

    def testCase_04(self):
        """用户A更新用户B下的便签数据-权限校验"""
        step('STEP1:用户A创建1条用户数据')
        noteId = str(int(time.time() * 1000)) + '_noteId'
        body = {
            'noteId': noteId,
            'star': 0

        }
        self.apiRequests.note_post(self.host + self.path, self.userId, self.sid, body)
        step('STEP2:用户B更改用户A的数据')
        body = {
            'noteId': noteId,
            'star': 0

        }
        res = self.apiRequests.note_post(self.host + self.path, self.user_idB, self.sid, body)
        self.assertEqual(412, res.status_code)
        expected = {'errorCode': -1011, 'errorMsg': 'user change!'}
        self.outPutResult.check_out(expected=expected, actual=res.json())
