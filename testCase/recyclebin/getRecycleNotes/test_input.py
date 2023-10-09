import unittest

from parameterized import parameterized

from business.apiRequest import ApiRequests
from business.generateNote import GenerateNote
from business.wipeNote import WipeNote
from common.caseLog import class_case_log, step
from common.checkResult import CheckResult
from common.yamlOperator import YamlOperator


@class_case_log
class TestCaseGetRecycleNoteTestInput(unittest.TestCase):
    apiRequests = ApiRequests()
    wipeNote = WipeNote()
    generateNote = GenerateNote()
    outPutResult = CheckResult()
    envConfig = YamlOperator().env_config()
    getRecycleNotesConfig = YamlOperator.api_data_config('recycleNotes')
    host = envConfig['host']
    userId = envConfig['user_id']
    sid = envConfig['sid']
    sibB = envConfig['sidB']
    notPresentSid = envConfig['notPresentSid']
    setNoteInfoPath = getRecycleNotesConfig['setNoteInfoPath']
    key = envConfig['key'].encode('utf-8')
    iv = envConfig['iv'].encode('utf-8')
    addNoteContentPath = getRecycleNotesConfig['addNoteContentPath']
    deleteNoteSvr = getRecycleNotesConfig['deleteNoteSvr']
    pathCleanRecycle = getRecycleNotesConfig['pathCleanRecycle']

    def setUp(self) -> None:
        """清除数据"""
        self.wipeNote.wipeNote(self.userId, self.sid)

    must_key_userid = [None, '9999999999999999999999999999999']

    @parameterized.expand(must_key_userid)
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
        getRecycleNotes = '/v3/notesvr/user/{}/invalid/startindex/{}/rows/{}/notes'.format(param, 0, 50)
        res = self.apiRequests.note_get(self.host + getRecycleNotes, self.userId, self.sid)
        self.assertEqual(500, res.status_code)
        expected = {'errorCode': -7, 'errorMsg': '参数类型错误！'}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    must_key_userid = ['', '！@#4909090']

    @parameterized.expand(must_key_userid)
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
        getRecycleNotes = '/v3/notesvr/user/{}/invalid/startindex/{}/rows/{}/notes'.format(param, 0, 50)
        res = self.apiRequests.note_get(self.host + getRecycleNotes, self.userId, self.sid)
        self.assertEqual(404, res.status_code)
        expected = {'timestamp': str, 'status': 404, 'error': 'Not Found',
                    'message': 'No message available', 'path': str}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    must_key_userid = [-1]

    @parameterized.expand(must_key_userid)
    def testCase_03(self, param):
        """负数"""
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
        getRecycleNotes = '/v3/notesvr/user/{}/invalid/startindex/{}/rows/{}/notes'.format(param, 0, 50)
        res = self.apiRequests.note_get(self.host + getRecycleNotes, self.userId, self.sid)
        self.assertEqual(412, res.status_code)
        expected = {'errorCode': -1011, 'errorMsg': 'user change!'}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    must_key_userid = ['你好']

    @parameterized.expand(must_key_userid)
    def testCase_04(self, param):
        """1，中文"""
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
        getRecycleNotes = '/v3/notesvr/user/{}/invalid/startindex/{}/rows/{}/notes'.format(param, 0, 50)
        res = self.apiRequests.note_get(self.host + getRecycleNotes, self.userId, self.sid)
        self.assertEqual(500, res.status_code)
        expected = {'errorCode': -7, 'errorMsg': '参数类型错误！'}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    must_key_userid = ['1111 ' or '1=1']

    @parameterized.expand(must_key_userid)
    def testCase_05(self, param):
        """中文"""
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
        getRecycleNotes = '/v3/notesvr/user/{}/invalid/startindex/{}/rows/{}/notes'.format(param, 0, 50)
        res = self.apiRequests.note_get(self.host + getRecycleNotes, self.userId, self.sid)
        self.assertEqual(412, res.status_code)
        expected = {'errorCode': -1011, 'errorMsg': 'user change!'}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    must_key_userid = ['111 "or"1=1']

    @parameterized.expand(must_key_userid)
    def testCase_06(self, param):
        """中文"""
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
        getRecycleNotes = '/v3/notesvr/user/{}/invalid/startindex/{}/rows/{}/notes'.format(param, 0, 50)
        res = self.apiRequests.note_get(self.host + getRecycleNotes, self.userId, self.sid)
        self.assertEqual(500, res.status_code)
        expected = {'errorCode': -7, 'errorMsg': '参数类型错误！'}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    must_key_startIndex = [None]

    @parameterized.expand(must_key_startIndex)
    def testCase_07(self, param):
        """中文"""
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
        getRecycleNotes = '/v3/notesvr/user/{}/invalid/startindex/{}/rows/{}/notes'.format(236948373, param, 50)
        res = self.apiRequests.note_get(self.host + getRecycleNotes, self.userId, self.sid)
        self.assertEqual(500, res.status_code)
        expected = {'errorCode': -7, 'errorMsg': '参数类型错误！'}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    must_key_startIndex = ['']

    @parameterized.expand(must_key_startIndex)
    def testCase_08t(self, param):
        """中文"""
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
        getRecycleNotes = '/v3/notesvr/user/{}/invalid/startindex/{}/rows/{}/notes'.format(236948373, param, 50)
        res = self.apiRequests.note_get(self.host + getRecycleNotes, self.userId, self.sid)
        self.assertEqual(404, res.status_code)
        expected = {'timestamp': str, 'status': 404, 'error': 'Not Found', 'message': 'No message available',
                    'path': '/v3/notesvr/user/236948373/invalid/startindex//rows/50/notes'}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    must_key_startIndex = [1.5]

    @parameterized.expand(must_key_startIndex)
    def testCase_09(self, param):
        """中文"""
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
        getRecycleNotes = '/v3/notesvr/user/{}/invalid/startindex/{}/rows/{}/notes'.format(236948373, param, 50)
        res = self.apiRequests.note_get(self.host + getRecycleNotes, self.userId, self.sid)
        self.assertEqual(500, res.status_code)
        expected = {'errorCode': -7, 'errorMsg': '参数类型错误！'}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    must_key_startIndex = [-2147483648]

    @parameterized.expand(must_key_startIndex)
    def testCase_10(self, param):
        """中文"""
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
        getRecycleNotes = '/v3/notesvr/user/{}/invalid/startindex/{}/rows/{}/notes'.format(236948373, param, 50)
        res = self.apiRequests.note_get(self.host + getRecycleNotes, self.userId, self.sid)
        self.assertEqual(200, res.status_code)
        expected = {'responseTime': 0, 'webNotes': []}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    must_key_startIndex = [2147483648]

    @parameterized.expand(must_key_startIndex)
    def testCase_11(self, param):
        """中文"""
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
        getRecycleNotes = '/v3/notesvr/user/{}/invalid/startindex/{}/rows/{}/notes'.format(236948373, param, 50)
        res = self.apiRequests.note_get(self.host + getRecycleNotes, self.userId, self.sid)
        self.assertEqual(500, res.status_code)
        expected = {'errorCode': -7, 'errorMsg': '参数类型错误！'}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    must_key_startIndex = ['1', "1"]

    @parameterized.expand(must_key_startIndex)
    def testCase_12(self, param):
        """中文"""
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
        getRecycleNotes = '/v3/notesvr/user/{}/invalid/startindex/{}/rows/{}/notes'.format(236948373, param, 50)
        res = self.apiRequests.note_get(self.host + getRecycleNotes, self.userId, self.sid)
        self.assertEqual(200, res.status_code)
        expected = {'responseTime': int, 'webNotes': list}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    must_key_rows = [None]

    @parameterized.expand(must_key_rows)
    def testCase_13(self, param):
        """中文"""
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
        getRecycleNotes = '/v3/notesvr/user/{}/invalid/startindex/{}/rows/{}/notes'.format(236948373, 0, param)
        res = self.apiRequests.note_get(self.host + getRecycleNotes, self.userId, self.sid)
        self.assertEqual(500, res.status_code)
        expected = {'errorCode': -7, 'errorMsg': '参数类型错误！'}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    must_key_rows = ['']

    @parameterized.expand(must_key_rows)
    def testCase_14(self, param):
        """中文"""
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
        getRecycleNotes = '/v3/notesvr/user/{}/invalid/startindex/{}/rows/{}/notes'.format(236948373, 0, param)
        res = self.apiRequests.note_get(self.host + getRecycleNotes, self.userId, self.sid)
        self.assertEqual(404, res.status_code)
        expected = {'timestamp': str, 'status': 404, 'error': 'Not Found', 'message': 'No message available',
                    'path': str}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    must_key_rows = [1.5]

    @parameterized.expand(must_key_rows)
    def testCase_15(self, param):
        """中文"""
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
        getRecycleNotes = '/v3/notesvr/user/{}/invalid/startindex/{}/rows/{}/notes'.format(236948373, 0, param)
        res = self.apiRequests.note_get(self.host + getRecycleNotes, self.userId, self.sid)
        self.assertEqual(500, res.status_code)
        expected = {'errorCode': -7, 'errorMsg': '参数类型错误！'}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    must_key_rows = [-2147483648]

    @parameterized.expand(must_key_rows)
    def testCase_16(self, param):
        """中文"""
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
        getRecycleNotes = '/v3/notesvr/user/{}/invalid/startindex/{}/rows/{}/notes'.format(236948373, 0, param)
        res = self.apiRequests.note_get(self.host + getRecycleNotes, self.userId, self.sid)
        self.assertEqual(200, res.status_code)
        expected = {'responseTime': 0, 'webNotes': []}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    must_key_rows = [2147483648]

    @parameterized.expand(must_key_rows)
    def testCase_17(self, param):
        """中文"""
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
        getRecycleNotes = '/v3/notesvr/user/{}/invalid/startindex/{}/rows/{}/notes'.format(236948373, 0, param)
        res = self.apiRequests.note_get(self.host + getRecycleNotes, self.userId, self.sid)
        self.assertEqual(500, res.status_code)
        expected = {'errorCode': -7, 'errorMsg': '参数类型错误！'}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    must_key_rows = ['1', "1"]

    @parameterized.expand(must_key_rows)
    def testCase_18(self, param):
        """中文"""
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
        getRecycleNotes = '/v3/notesvr/user/{}/invalid/startindex/{}/rows/{}/notes'.format(236948373, 0, param)
        res = self.apiRequests.note_get(self.host + getRecycleNotes, self.userId, self.sid)
        self.assertEqual(200, res.status_code)
        expected = {'responseTime': int, 'webNotes': list}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_19(self):
        """不存在的wps_sid"""
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
        getRecycleNotes = '/v3/notesvr/user/{}/invalid/startindex/{}/rows/{}/notes'.format(236948373, 0, 50)
        res = self.apiRequests.note_get(self.host + getRecycleNotes, self.userId, self.notPresentSid)
        self.assertEqual(401, res.status_code)
        expected = {'errorCode': -2010, 'errorMsg': ''}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_20(self):
        """用户A查询用户B的便签数据"""
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
        getRecycleNotes = '/v3/notesvr/user/{}/invalid/startindex/{}/rows/{}/notes'.format(236948373, 0, 50)
        res = self.apiRequests.note_get(self.host + getRecycleNotes, self.userId, self.sibB)
        self.assertEqual(412, res.status_code)
        expected = {'errorCode': -1011, 'errorMsg': 'user change!'}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_21(self):
        """用户A查询用户B的便签数据"""
        step('STEP1:造1条测试数据')
        noteIds = self.generateNote.generate_note_test(1, self.userId, self.sid)
        step('STEP2:删除创建的便签')
        for item in range(len(noteIds)):
            noteId = noteIds[item]
            body = {
                'noteId': noteId

            }
            self.apiRequests.note_post(self.host + self.deleteNoteSvr, self.userId, self.sid, body)

        new_header = {
            'Content-type': 'application/json',
            'X-user-key': str(self.userId),
            'Cookie': f'wps_sid={self.sid}'
        }
        new_header.pop('Cookie')

        step('STEP3:获取回收站下便签')
        getRecycleNotes = '/v3/notesvr/user/{}/invalid/startindex/{}/rows/{}/notes'.format(236948373, 0, 50)
        res = self.apiRequests.note_get(self.host + getRecycleNotes, self.userId, self.sibB, new_header)
        self.assertEqual(401, res.status_code)
        expected = {'errorCode': -2009, 'errorMsg': ''}
        self.outPutResult.check_out(expected=expected, actual=res.json())
