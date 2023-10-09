import unittest

from parameterized import parameterized

from business.apiRequest import ApiRequests
from business.generateNote import GenerateNote
from business.wipeNote import WipeNote
from common.caseLog import class_case_log, step, info
from common.checkResult import CheckResult
from common.yamlOperator import YamlOperator


@class_case_log
class TestCaseCleanRecycleNoteTestInput(unittest.TestCase):
    apiRequests = ApiRequests()
    wipeNote = WipeNote()
    generateNote = GenerateNote()
    outPutResult = CheckResult()
    envConfig = YamlOperator().env_config()
    getRecycleNotesConfig = YamlOperator.api_data_config('recycleNotes')
    host = envConfig['host']
    userId = envConfig['user_id']
    sid = envConfig['sid']
    sidB = envConfig['sidB']
    notPresentSid = envConfig['notPresentSid']
    setNoteInfoPath = getRecycleNotesConfig['setNoteInfoPath']
    key = envConfig['key'].encode('utf-8')
    iv = envConfig['iv'].encode('utf-8')
    addNoteContentPath = getRecycleNotesConfig['addNoteContentPath']
    deleteNoteSvr = getRecycleNotesConfig['deleteNoteSvr']
    pathCleanRecycle = getRecycleNotesConfig['pathCleanRecycle']
    getRecycleNotes = '/v3/notesvr/user/{}/invalid/startindex/{}/rows/{}/notes'.format('236948373', '0', '50')

    def setUp(self) -> None:
        """清除数据"""
        self.wipeNote.wipeNote(self.userId, self.sid)

    must_key = [None]

    @parameterized.expand(must_key)
    def testCase_01(self, param):
        """None"""
        step('STEP1:造1条测试数据')
        noteIds = self.generateNote.generate_note_test(1, self.userId, self.sid)
        step('STEP2:删除创建的便签')
        for item in range(len(noteIds)):
            noteId = noteIds[item]
            body = {
                'noteId': noteId

            }
            self.apiRequests.note_post(self.host + self.deleteNoteSvr, self.userId, self.sid, body)

        step('STEP3:获取回收站下便签')
        res = self.apiRequests.note_get(self.host + self.getRecycleNotes, self.userId, self.sid)
        noteIdsRes = [item['noteId'] for item in res.json()['webNotes']]
        info(f'获取的回收站下的便签{noteIdsRes}')
        step('STEP4:清空回收站')
        body = {
            'noteIds': param
        }
        res = self.apiRequests.note_post(self.host + self.pathCleanRecycle, self.userId, self.sid, body)
        expected = {'errorCode': -7, 'errorMsg': '参数不合法！'}
        self.assertEqual(500, res.status_code)
        self.outPutResult.check_out(expected=expected, actual=res.json())

    must_key = ['']

    @parameterized.expand(must_key)
    def testCase_02(self, param):
        """空字符串"""
        step('STEP1:造1条测试数据')
        noteIds = self.generateNote.generate_note_test(1, self.userId, self.sid)
        step('STEP2:删除创建的便签')
        for item in range(len(noteIds)):
            noteId = noteIds[item]
            body = {
                'noteId': noteId

            }
            self.apiRequests.note_post(self.host + self.deleteNoteSvr, self.userId, self.sid, body)

        step('STEP3:获取回收站下便签')
        res = self.apiRequests.note_get(self.host + self.getRecycleNotes, self.userId, self.sid)
        noteIdsRes = [item['noteId'] for item in res.json()['webNotes']]
        info(f'获取的回收站下的便签{noteIdsRes}')
        step('STEP4:清空回收站')
        body = {
            'noteIds': param
        }
        res = self.apiRequests.note_post(self.host + self.pathCleanRecycle, self.userId, self.sid, body)
        expected = {'errorCode': -7, 'errorMsg': ''}
        self.assertEqual(500, res.status_code)
        self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_03(self):
        """删除主键"""
        step('STEP1:造1条测试数据')
        noteIds = self.generateNote.generate_note_test(1, self.userId, self.sid)
        step('STEP2:删除创建的便签')
        for item in range(len(noteIds)):
            noteId = noteIds[item]
            body = {
                'noteId': noteId

            }
            self.apiRequests.note_post(self.host + self.deleteNoteSvr, self.userId, self.sid, body)

        step('STEP3:获取回收站下便签')
        res = self.apiRequests.note_get(self.host + self.getRecycleNotes, self.userId, self.sid)
        noteIdsRes = [item['noteId'] for item in res.json()['webNotes']]
        info(f'获取的回收站下的便签{noteIdsRes}')
        step('STEP4:清空回收站')
        body = {
            'noteIds': noteIdsRes
        }
        body.pop('noteIds')
        res = self.apiRequests.note_post(self.host + self.pathCleanRecycle, self.userId, self.sid, body)
        expected = {'errorCode': -7, 'errorMsg': '参数不合法！'}
        self.assertEqual(500, res.status_code)
        self.outPutResult.check_out(expected=expected, actual=res.json())

    must_key = [['9999999999999999999999999999999999999999'], ['你好']]

    @parameterized.expand(must_key)
    def testCase_04(self, param):
        """空字符串"""
        step('STEP1:造1条测试数据')
        noteIds = self.generateNote.generate_note_test(1, self.userId, self.sid)
        step('STEP2:删除创建的便签')
        for item in range(len(noteIds)):
            noteId = noteIds[item]
            body = {
                'noteId': noteId

            }
            self.apiRequests.note_post(self.host + self.deleteNoteSvr, self.userId, self.sid, body)

        step('STEP3:获取回收站下便签')
        res = self.apiRequests.note_get(self.host + self.getRecycleNotes, self.userId, self.sid)
        noteIdsRes = [item['noteId'] for item in res.json()['webNotes']]
        info(f'获取的回收站下的便签{noteIdsRes}')
        step('STEP4:清空回收站')
        body = {
            'noteIds': param
        }
        res = self.apiRequests.note_post(self.host + self.pathCleanRecycle, self.userId, self.sid, body)
        expected = {'errorCode': -7, 'errorMsg': ''}
        self.assertEqual(500, res.status_code)
        self.outPutResult.check_out(expected=expected, actual=res.json())

    must_key = [['！@#￥sdsd'], ['123 ' or '1=1']]

    @parameterized.expand(must_key)
    def testCase_05(self, param):
        """空字符串"""
        step('STEP1:造1条测试数据')
        noteIds = self.generateNote.generate_note_test(1, self.userId, self.sid)
        step('STEP2:删除创建的便签')
        for item in range(len(noteIds)):
            noteId = noteIds[item]
            body = {
                'noteId': noteId

            }
            self.apiRequests.note_post(self.host + self.deleteNoteSvr, self.userId, self.sid, body)

        step('STEP3:获取回收站下便签')
        res = self.apiRequests.note_get(self.host + self.getRecycleNotes, self.userId, self.sid)
        noteIdsRes = [item['noteId'] for item in res.json()['webNotes']]
        info(f'获取的回收站下的便签{noteIdsRes}')
        step('STEP4:清空回收站')
        body = {
            'noteIds': param
        }
        res = self.apiRequests.note_post(self.host + self.pathCleanRecycle, self.userId, self.sid, body)
        expected = {'errorCode': -7, 'errorMsg': ''}
        self.assertEqual(500, res.status_code)
        self.outPutResult.check_out(expected=expected, actual=res.json())

    must_key = [['123 " or "1=1']]

    @parameterized.expand(must_key)
    def testCase_06(self, param):
        """空字符串"""
        step('STEP1:造1条测试数据')
        noteIds = self.generateNote.generate_note_test(1, self.userId, self.sid)
        step('STEP2:删除创建的便签')
        for item in range(len(noteIds)):
            noteId = noteIds[item]
            body = {
                'noteId': noteId

            }
            self.apiRequests.note_post(self.host + self.deleteNoteSvr, self.userId, self.sid, body)

        step('STEP3:获取回收站下便签')
        res = self.apiRequests.note_get(self.host + self.getRecycleNotes, self.userId, self.sid)
        noteIdsRes = [item['noteId'] for item in res.json()['webNotes']]
        info(f'获取的回收站下的便签{noteIdsRes}')
        step('STEP4:清空回收站')
        body = {
            'noteIds': param
        }
        res = self.apiRequests.note_post(self.host + self.pathCleanRecycle, self.userId, self.sid, body)
        expected = {'errorCode': -7, 'errorMsg': ''}
        self.assertEqual(500, res.status_code)
        self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_07(self):
        """用户B删除用户A的数据"""
        step('STEP1:造1条测试数据')
        noteIds = self.generateNote.generate_note_test(1, self.userId, self.sid)
        step('STEP2:删除创建的便签')
        for item in range(len(noteIds)):
            noteId = noteIds[item]
            body = {
                'noteId': noteId

            }
            self.apiRequests.note_post(self.host + self.deleteNoteSvr, self.userId, self.sid, body)

        step('STEP3:获取回收站下便签')
        res = self.apiRequests.note_get(self.host + self.getRecycleNotes, self.userId, self.sid)
        noteIdsRes = [item['noteId'] for item in res.json()['webNotes']]
        info(f'获取的回收站下的便签{noteIdsRes}')
        step('STEP4:清空回收站')
        body = {
            'noteIds': noteIdsRes
        }
        res = self.apiRequests.note_post(self.host + self.pathCleanRecycle, self.userId, self.sidB, body)
        expected = {'errorCode': -1011, 'errorMsg': 'user change!'}
        self.assertEqual(412, res.status_code)
        self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_08(self):
        """用户B删除用户A的数据"""
        step('STEP1:造1条测试数据')
        noteIds = self.generateNote.generate_note_test(1, self.userId, self.sid)
        step('STEP2:删除创建的便签')
        for item in range(len(noteIds)):
            noteId = noteIds[item]
            body = {
                'noteId': noteId

            }
            self.apiRequests.note_post(self.host + self.deleteNoteSvr, self.userId, self.sid, body)

        step('STEP3:获取回收站下便签')
        res = self.apiRequests.note_get(self.host + self.getRecycleNotes, self.userId, self.sid)
        noteIdsRes = [item['noteId'] for item in res.json()['webNotes']]
        info(f'获取的回收站下的便签{noteIdsRes}')
        step('STEP4:清空回收站')
        body = {
            'noteIds': noteIdsRes
        }
        res = self.apiRequests.note_post(self.host + self.pathCleanRecycle, self.userId, self.notPresentSid, body)
        expected = {'errorCode': -2010, 'errorMsg': ''}
        self.assertEqual(401, res.status_code)
        self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_09(self):
        """用户B删除用户A的数据"""
        step('STEP1:造1条测试数据')
        noteIds = self.generateNote.generate_note_test(1, self.userId, self.sid)
        step('STEP2:删除创建的便签')
        for item in range(len(noteIds)):
            noteId = noteIds[item]
            body = {
                'noteId': noteId

            }
            self.apiRequests.note_post(self.host + self.deleteNoteSvr, self.userId, self.sid, body)

        step('STEP3:获取回收站下便签')
        res = self.apiRequests.note_get(self.host + self.getRecycleNotes, self.userId, self.sid)
        noteIdsRes = [item['noteId'] for item in res.json()['webNotes']]
        info(f'获取的回收站下的便签{noteIdsRes}')
        step('STEP4:清空回收站')
        body = {
            'noteIds': noteIdsRes
        }
        new_header = {
            'Content-type': 'application/json',
            'X-user-key': str(self.userId),
            'Cookie': f'wps_sid={self.sid}'

        }
        new_header.pop('Cookie')
        res = self.apiRequests.note_post(self.host + self.pathCleanRecycle, self.userId, self.sid, body, new_header)
        expected = {'errorCode': -2009, 'errorMsg': ''}
        self.assertEqual(401, res.status_code)
        self.outPutResult.check_out(expected=expected, actual=res.json())
