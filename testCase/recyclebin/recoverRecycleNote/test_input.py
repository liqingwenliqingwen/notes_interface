import unittest

from parameterized import parameterized

from business.apiRequest import ApiRequests
from business.generateNote import GenerateNote
from business.wipeNote import WipeNote
from common.caseLog import class_case_log, step, info
from common.checkResult import CheckResult
from common.yamlOperator import YamlOperator


@class_case_log
class TestCaseRecoverRecycleNoteInput(unittest.TestCase):
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

    recoverRecyclePath = '/v3/notesvr/user/{}/notes'.format(236948373)
    getNotePath = '/v3/notesvr/user/{}/home/startindex/{}/rows/{}/notes'.format(236948373, 0, 10)

    def setUp(self) -> None:
        """清除数据"""
        self.wipeNote.wipeNote(self.userId, self.sid)

    must_key_userId = [
        (None,)

    ]

    @parameterized.expand(must_key_userId)
    def testCase_01(self, param):
        """None '',"""
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
        step('STEP4:恢复回收站下的便签')
        recoverRecyclePath = '/v3/notesvr/user/{}/notes'.format(param)
        body = {
            'userId': param,
            'noteIds': noteIdsRes
        }
        res = self.apiRequests.note_patch(self.host + recoverRecyclePath, self.userId, self.sid, body)
        self.assertEqual(500, res.status_code)

    must_key_userId = [

        ('',)
    ]

    @parameterized.expand(must_key_userId)
    def testCase_02(self, param):
        """None '',"""
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
        step('STEP4:恢复回收站下的便签')
        recoverRecyclePath = '/v3/notesvr/user/{}/notes'.format(param)
        body = {
            'userId': param,
            'noteIds': noteIdsRes
        }
        res = self.apiRequests.note_patch(self.host + recoverRecyclePath, self.userId, self.sid, body)
        self.assertEqual(404, res.status_code)

    def testCase_03(self):
        """None '',"""
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
        step('STEP4:恢复回收站下的便签')
        recoverRecyclePath = '/v3/notesvr/user/{}/notes'.format(236948373)
        body = {
            'userId': 236948373,
            'noteIds': noteIdsRes
        }
        body.pop('userId')
        res = self.apiRequests.note_patch(self.host + recoverRecyclePath, self.userId, self.sid, body)
        self.assertEqual(412, res.status_code)

    must_key_userId = [(-236948373,), (0,)]

    @parameterized.expand(must_key_userId)
    def testCase_04(self, param):
        """None '',"""
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
        step('STEP4:恢复回收站下的便签')
        recoverRecyclePath = '/v3/notesvr/user/{}/notes'.format(param)
        body = {
            'userId': param,
            'noteIds': noteIdsRes
        }
        res = self.apiRequests.note_patch(self.host + recoverRecyclePath, self.userId, self.sid, body)
        self.assertEqual(412, res.status_code)

    must_key_userId = [(236948373.5,)]

    @parameterized.expand(must_key_userId)
    def testCase_05(self, param):
        """None '',"""
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
        step('STEP4:恢复回收站下的便签')
        recoverRecyclePath = '/v3/notesvr/user/{}/notes'.format(param)
        body = {
            'userId': param,
            'noteIds': noteIdsRes
        }
        res = self.apiRequests.note_patch(self.host + recoverRecyclePath, self.userId, self.sid, body)
        self.assertEqual(500, res.status_code)

    must_key_userId = [(236948373,)]

    @parameterized.expand(must_key_userId)
    def testCase_06(self, param):
        """None '',"""
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
        step('STEP4:恢复回收站下的便签')
        recoverRecyclePath = '/v3/notesvr/user/{}/notes'.format(param)
        body = {
            'userId': param,
            'noteIds': noteIdsRes
        }
        res = self.apiRequests.note_patch(self.host + recoverRecyclePath, self.userId, self.sid, body)
        self.assertEqual(200, res.status_code)

    must_key_userId = [(-1,), (0,)]

    @parameterized.expand(must_key_userId)
    def testCase_07(self, param):
        """-1,0"""
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
        step('STEP4:恢复回收站下的便签')
        recoverRecyclePath = '/v3/notesvr/user/{}/notes'.format(param)
        body = {
            'userId': param,
            'noteIds': noteIdsRes
        }
        res = self.apiRequests.note_patch(self.host + recoverRecyclePath, self.userId, self.sid, body)
        self.assertEqual(412, res.status_code)

    must_key_userId = ['1' or '1=1']

    @parameterized.expand(must_key_userId)
    def testCase_08(self, param):
        """-1,0"""
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
        step('STEP4:恢复回收站下的便签')
        recoverRecyclePath = '/v3/notesvr/user/{}/notes'.format(param)
        body = {
            'userId': param,
            'noteIds': noteIdsRes
        }
        res = self.apiRequests.note_patch(self.host + recoverRecyclePath, self.userId, self.sid, body)
        self.assertEqual(412, res.status_code)

    must_key_noteIds = [
        (None,),
        ('',)
    ]

    @parameterized.expand(must_key_noteIds)
    def testCase_09(self, param):
        """None '',"""
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
        step('STEP4:恢复回收站下的便签')
        recoverRecyclePath = '/v3/notesvr/user/{}/notes'.format(236948373)
        body = {
            'userId': self.userId,
            'noteIds': param
        }
        res = self.apiRequests.note_patch(self.host + recoverRecyclePath, self.userId, self.sid, body)
        self.assertEqual(500, res.status_code)

    def testCase_10(self):
        """None '',"""
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
        step('STEP4:恢复回收站下的便签')
        recoverRecyclePath = '/v3/notesvr/user/{}/notes'.format(236948373)
        body = {
            'userId': self.userId,
            'noteIds': noteIdsRes
        }
        body.pop('noteIds')
        res = self.apiRequests.note_patch(self.host + recoverRecyclePath, self.userId, self.sid, body)
        self.assertEqual(500, res.status_code)

    must_key_noteIds = [['999999999999999999999999999999999999999999999999999999999999999999'], ['你好']]

    @parameterized.expand(must_key_noteIds)
    def testCase_11(self, param):
        """None '',"""
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
        step('STEP4:恢复回收站下的便签')
        recoverRecyclePath = '/v3/notesvr/user/{}/notes'.format(236948373)
        body = {
            'userId': self.userId,
            'noteIds': param
        }
        res = self.apiRequests.note_patch(self.host + recoverRecyclePath, self.userId, self.sid, body)
        self.assertEqual(500, res.status_code)

    must_key_noteIds = [['！！@@@'], ['123 ' or '1=1']]

    @parameterized.expand(must_key_noteIds)
    def testCase_12(self, param):
        """None '',"""
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
        step('STEP4:恢复回收站下的便签')
        recoverRecyclePath = '/v3/notesvr/user/{}/notes'.format(236948373)
        body = {
            'userId': self.userId,
            'noteIds': param
        }
        res = self.apiRequests.note_patch(self.host + recoverRecyclePath, self.userId, self.sid, body)
        self.assertEqual(500, res.status_code)

    def testCase_13(self):
        """'',"""
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
        step('STEP4:恢复回收站下的便签')
        recoverRecyclePath = '/v3/notesvr/user/{}/notes'.format(236948373)
        body = {
            'userId': self.userId,
            'noteIds': noteIdsRes
        }
        res = self.apiRequests.note_patch(self.host + recoverRecyclePath, self.userId, self.sidB, body)
        self.assertEqual(412, res.status_code)

    def testCase_14(self):
        """'',"""
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
        step('STEP4:恢复回收站下的便签')
        recoverRecyclePath = '/v3/notesvr/user/{}/notes'.format(236948373)
        body = {
            'userId': self.userId,
            'noteIds': noteIdsRes
        }
        new_header = {
            'Content-type': 'application/json',
            'X-user-key': str(self.userId),
            'Cookie': f'wps_sid={self.sid}'
        }
        new_header.pop('Cookie')
        res = self.apiRequests.note_patch(self.host + recoverRecyclePath, self.userId, self.sid, body, new_header)
        self.assertEqual(401, res.status_code)

    def testCase_15(self):
        """'',"""
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
        step('STEP4:恢复回收站下的便签')
        recoverRecyclePath = '/v3/notesvr/user/{}/notes'.format(236948373)
        body = {
            'userId': self.userId,
            'noteIds': noteIdsRes
        }

        res = self.apiRequests.note_patch(self.host + recoverRecyclePath, self.userId, self.notPresentSid, body,
                                          )
        self.assertEqual(401, res.status_code)
