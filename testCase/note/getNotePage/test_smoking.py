import unittest

from business.apiRequest import ApiRequests
from business.generateNote import GenerateNote
from business.wipeNote import WipeNote
from common.caseLog import step, class_case_log, info
from common.checkResult import CheckResult
from common.yamlOperator import YamlOperator


@class_case_log
class GetPageNotePageSmoking(unittest.TestCase):
    outPutResult = CheckResult()
    apiRequests = ApiRequests()
    wipeNote = WipeNote()
    generateNote = GenerateNote()

    envConfig = YamlOperator().env_config()
    getPageNoteConfig = YamlOperator.api_data_config('getPageNote')

    host = envConfig['host']
    sid = envConfig['sid']
    userId = envConfig['user_id']
    key = envConfig['key'].encode('utf-8')
    iv = envConfig['iv'].encode('utf-8')

    addNotePath = getPageNoteConfig['addNotePath']
    addNoteContent = getPageNoteConfig['addNoteContent']
    getNotePath = '/v3/notesvr/user/{}/home/startindex/{}/rows/{}/notes'.format(236948373, 0, 50)

    def setUp(self) -> None:
        step('STEP1:清空当前历史数据')
        self.wipeNote.wipeNote(self.userId, self.sid)

    def testCase_01(self):
        """获取首页便签主流程"""

        step('STEP1:造1条测试数据')
        noteId = self.generateNote.generate_note_test(1, self.userId, self.sid)
        info(f'新建的便签数据为{noteId}')
        step('STEP2:获取便签列表')
        res = self.apiRequests.note_get(self.host + self.getNotePath, self.userId, self.sid)
        step('STEP3:校验返回值')
        expected = {'responseTime': int, 'webNotes': [
            {'noteId': noteId[0], 'createTime': int, 'star': 0, 'remindTime': 0,
             'remindType': 0, 'infoVersion': int, 'infoUpdateTime': int, 'groupId': None,
             'title': 'aiXhXKtVDyR9/L7DJTxhLg==', 'summary': '4ZTUOD5fyvtLawr5pV/D3w==', 'thumbnail': None,
             'contentVersion': int, 'contentUpdateTime': int}]}
        self.assertEqual(200, res.status_code)
        self.assertEqual(1, len(res.json()['webNotes']))
        self.outPutResult.check_out(expected=expected, actual=res.json())
