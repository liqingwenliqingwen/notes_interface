import time
import unittest

from parameterized import parameterized

from business.apiRequest import ApiRequests
from business.generateNote import GenerateNote
from business.wipeNote import WipeNote
from common.caseLog import class_case_log, step
from common.checkResult import CheckResult
from common.yamlOperator import YamlOperator


@class_case_log
class TestCaseSetNoteInfoInput(unittest.TestCase):
    wipeNote = WipeNote()
    apiRequest = ApiRequests()
    outPutResult = CheckResult()
    envConfig = YamlOperator().env_config()
    generateNote = GenerateNote()
    setNoteInfoConfig = YamlOperator.api_data_config('SetNoteInfo')
    userId = envConfig['user_id']
    sid = envConfig['sid']
    sidB = envConfig['sidB']
    path = setNoteInfoConfig['path']
    notPresentSid = envConfig['notPresentSid']

    host = envConfig['host']

    getNotePagePath = '/v3/notesvr/user/{}/home/startindex/{}/rows/{}/notes'.format(userId, 0, 10)
    addNoteContentPath = setNoteInfoConfig['addNoteContentPath']
    getNoteGroupPath = setNoteInfoConfig['get_note_group_path']

    noteId = str(int(time.time() * 1000)) + '_noteId'

    key = 'H9n&S@oGohGpV6d7'.encode('utf-8')
    iv = '5150956153345366'.encode('utf-8')

    def setUp(self) -> None:
        step('STEP1:清空数据')
        self.wipeNote.wipeNote(self.userId, self.sid)

    must_key_noteIds_null = [
        (None,),
        ('',)
    ]

    @parameterized.expand(must_key_noteIds_null)
    def testCase_01(self, param):
        """校验input-noteId必填项目校验"""
        step('STEP1:新建1条便签主体')
        body = {
            'noteId': param,
        }
        res = self.apiRequest.note_post(self.host + self.path, self.userId, self.sid, body)
        step('STEP2:校验code和返回值')
        self.assertEqual(500, res.status_code)
        expected = {'errorCode': -7, 'errorMsg': '参数不合法！'}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_02(self):
        """校验input-noteId必填项目校验,删除noteId的key"""

        step('STEP1:新建1条便签主体')
        body = {
            'noteId': self.noteId,
        }
        del body['noteId']
        res = self.apiRequest.note_post(self.host + self.path, self.userId, self.sid, body)
        step('STEP2:校验code和返回值')
        self.assertEqual(500, res.status_code)
        expected = {'errorCode': -7, 'errorMsg': '参数不合法！'}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    abnormal_noteId = ['99999999999999999999999999999', '123!!']

    @parameterized.expand(abnormal_noteId)
    def testCase_03(self, param):
        """校验input-noteId必填项目校验,noteId为特殊值,1,999999,2,包含特殊符号"""

        step('STEP1:新建1条便签主体')
        body = {
            'noteId': param,
        }

        res = self.apiRequest.note_post(self.host + self.path, self.userId, self.sid, body)
        step('STEP2:校验code和返回值')
        self.assertEqual(200, res.status_code)
        expected = {'responseTime': int, 'infoVersion': int, 'infoUpdateTime': int}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    abnormal_noteId_str = ['你好']

    @parameterized.expand(abnormal_noteId_str)
    def testCase_04(self, param):
        """校验input-noteId必填1，包含中文，"""

        step('STEP1:新建1条便签主体')
        body = {
            'noteId': param,
        }

        res = self.apiRequest.note_post(self.host + self.path, self.userId, self.sid, body)
        step('STEP2:校验code和返回值')
        self.assertEqual(500, res.status_code)
        expected = {'errorCode': -7, 'errorMsg': str}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    abnormal_noteId_str = ['123456ty or 1=1']

    @parameterized.expand(abnormal_noteId_str)
    def testCase_05(self, param):
        """校验input-noteId必填1，包含中文，2包含or 1=1"""

        step('STEP1:新建1条便签主体')
        body = {
            'noteId': param,
        }

        res = self.apiRequest.note_post(self.host + self.path, self.userId, self.sid, body)
        step('STEP2:校验code和返回值')
        self.assertEqual(200, res.status_code)
        expected = {'responseTime': int, 'infoVersion': int, 'infoUpdateTime': int}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    optional_star_None = [
        (None,),
        ('',)
    ]

    @parameterized.expand(optional_star_None)
    def testCase_06(self, param):
        """校验input-star选填项1,star为空字符串。2，参数为None"""

        step('STEP1:新建1条便签主体')
        body = {
            'noteId': self.noteId,
            'star': param
        }

        res = self.apiRequest.note_post(self.host + self.path, self.userId, self.sid, body)
        step('STEP2:校验code和返回值')
        self.assertEqual(200, res.status_code)
        expected = {'responseTime': int, 'infoVersion': int, 'infoUpdateTime': int}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    optional_star_negative = [(-1,),( 1.5,)]

    @parameterized.expand(optional_star_negative)
    def testCase_07(self, param):
        """校验input-star选填项1,star为负数。2，参数为小数点"""

        step('STEP1:新建1条便签主体')
        body = {
            'noteId': self.noteId,
            'star': param
        }

        res = self.apiRequest.note_post(self.host + self.path, self.userId, self.sid, body)
        step('STEP2:校验code和返回值')
        self.assertEqual(200, res.status_code)
        expected = {'responseTime': int, 'infoVersion': int, 'infoUpdateTime': int}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    optional_star_str = ['1', "1"]

    @parameterized.expand(optional_star_str)
    def testCase_08(self, param):
        """校验input-star选填项1,star为负数。2，参数为小数点"""

        step('STEP1:新建1条便签主体')
        body = {
            'noteId': self.noteId,
            'star': param
        }

        res = self.apiRequest.note_post(self.host + self.path, self.userId, self.sid, body)
        step('STEP2:校验code和返回值')
        self.assertEqual(200, res.status_code)
        expected = {'responseTime': int, 'infoVersion': int, 'infoUpdateTime': int}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    optional_star_ = [(1,),( 0,)]

    @parameterized.expand(optional_star_)
    def testCase_09(self, param):
        """校验input-star选填项1,star为负数。2，参数为小数点"""

        step('STEP1:新建1条便签主体')
        body = {
            'noteId': self.noteId,
            'star': param
        }

        res = self.apiRequest.note_post(self.host + self.path, self.userId, self.sid, body)
        step('STEP2:校验code和返回值')
        self.assertEqual(200, res.status_code)
        expected = {'responseTime': int, 'infoVersion': int, 'infoUpdateTime': int}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    optional_remindTime = [
        (None,),
        ('',)
    ]

    @parameterized.expand(optional_remindTime)
    def testCase_10(self, param):
        """校验input-remindTime选填项1,空,2,空字符串"""

        step('STEP1:新建1条便签主体')
        body = {
            'noteId': self.noteId,
            'remindTime': param
        }

        res = self.apiRequest.note_post(self.host + self.path, self.userId, self.sid, body)
        step('STEP2:校验code和返回值')
        self.assertEqual(200, res.status_code)
        expected = {'responseTime': int, 'infoVersion': int, 'infoUpdateTime': int}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    optional_remindTime_min_max = [(5387,),( 4070914187,)]

    @parameterized.expand(optional_remindTime_min_max)
    def testCase_11(self, param):
        """校验input-remindTime，1，很小的值，2099年很大值"""

        step('STEP1:新建1条便签主体')
        body = {
            'noteId': self.noteId,
            'remindTime': param
        }
        res = self.apiRequest.note_post(self.host + self.path, self.userId, self.sid, body)
        step('STEP2:校验code和返回值')
        self.assertEqual(200, res.status_code)
        expected = {'responseTime': int, 'infoVersion': int, 'infoUpdateTime': int}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    optional_remindTime_negative = [(-5387,),( 4070914187.90,)]

    @parameterized.expand(optional_remindTime_negative)
    def testCase_12(self, param):
        """校验input-remindTime，1，负数，2，小数"""

        step('STEP1:新建1条便签主体')
        body = {
            'noteId': self.noteId,
            'remindTime': param
        }
        res = self.apiRequest.note_post(self.host + self.path, self.userId, self.sid, body)
        step('STEP2:校验code和返回值')
        self.assertEqual(200, res.status_code)
        expected = {'responseTime': int, 'infoVersion': int, 'infoUpdateTime': int}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    optional_remindType = [
        (None,),
        ('',)
    ]

    @parameterized.expand(optional_remindType)
    def testCase_13(self, param):
        """校验input-NotesRemind，1，None，2，空字符串"""

        step('STEP1:新建1条便签主体')
        body = {
            'noteId': self.noteId,
            'remindType': param
        }
        res = self.apiRequest.note_post(self.host + self.path, self.userId, self.sid, body)
        step('STEP2:校验code和返回值')
        self.assertEqual(200, res.status_code)
        expected = {'responseTime': int, 'infoVersion': int, 'infoUpdateTime': int}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    optional_remindType_decimal = [(1.5,),( '1',)]

    @parameterized.expand(optional_remindType_decimal)
    def testCase_14(self, param):
        """校验input-NotesRemind，1，小数，2，字符串"""

        step('STEP1:新建1条便签主体')
        body = {
            'noteId': self.noteId,
            'remindType': param
        }
        res = self.apiRequest.note_post(self.host + self.path, self.userId, self.sid, body)
        step('STEP2:校验code和返回值')
        self.assertEqual(200, res.status_code)
        expected = {'responseTime': int, 'infoVersion': int, 'infoUpdateTime': int}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    optional_remindType_negative = [(-1,)]

    @parameterized.expand(optional_remindType_negative)
    def testCase_15(self, param):
        """校验input-NotesRemind，1，小数，2，字符串"""

        step('STEP1:新建1条便签主体')
        body = {
            'noteId': self.noteId,
            'remindType': param
        }
        res = self.apiRequest.note_post(self.host + self.path, self.userId, self.sid, body)
        step('STEP2:校验code和返回值')
        self.assertEqual(500, res.status_code)
        expected = {'errorCode': -7, 'errorMsg': '参数不合法！'}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    optional_groupId = [
        (None,),
        ('',)
    ]

    @parameterized.expand(optional_groupId)
    def testCase_16(self, param):
        """校验input-NotesRemind，1，None，2，空字符"""

        step('STEP1:新建1条便签主体')
        body = {
            'noteId': self.noteId,
            'groupId': param
        }
        res = self.apiRequest.note_post(self.host + self.path, self.userId, self.sid, body)
        step('STEP2:校验code和返回值')
        self.assertEqual(200, res.status_code)
        expected = {'responseTime': int, 'infoVersion': int, 'infoUpdateTime': int}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    optional_groupId_max = ['0000 ' or '1=1', "999999999999999999999999999999"]

    @parameterized.expand(optional_groupId_max)
    def testCase_17(self, param):
        """校验input-NotesRemind，1，包括’or‘1=1，2，99999999999999999999999999999999999"""

        step('STEP1:新建1条便签主体')
        body = {
            'noteId': self.noteId,
            'groupId': param
        }
        res = self.apiRequest.note_post(self.host + self.path, self.userId, self.sid, body)
        step('STEP2:校验code和返回值')
        self.assertEqual(200, res.status_code)
        expected = {'responseTime': int, 'infoVersion': int, 'infoUpdateTime': int}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    optional_groupId_chinese = [
        ("999你好",)
    ]

    @parameterized.expand(optional_groupId_chinese)
    def testCase_18(self, param):
        """校验input-NotesRemind，1，包括中文"""

        step('STEP1:新建1条便签主体')
        body = {
            'noteId': self.noteId,
            'groupId': param
        }
        res = self.apiRequest.note_post(self.host + self.path, self.userId, self.sid, body)
        step('STEP2:校验code和返回值')
        self.assertEqual(500, res.status_code)
        expected = {'errorCode': -7, 'errorMsg': str}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_19(self):
        """身份校验-不存在的wps_sid"""

        step('STEP1:新建1条便签主体')
        body = {
            'noteId': self.noteId,

        }
        res = self.apiRequest.note_post(self.host + self.path, self.userId, self.notPresentSid, body)
        step('STEP2:校验code和返回值')
        self.assertEqual(401, res.status_code)
        expected = {'errorCode': -2010, 'errorMsg': ''}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_20(self):
        """身份校验-不存在的wps_sid"""

        step('STEP1:新建1条便签主体')

        headers = {
            'Content-Type': 'application/json',
            'X-user-key': str(self.userId),
            'Cookie': f'wps_sid={self.sid}'

        }
        headers.pop('Cookie')  # 删除cookie
        body = {
            'noteId': self.noteId,

        }
        res = self.apiRequest.note_post(self.host + self.path, self.userId, self.sid, body,
                                        new_header=headers)
        step('STEP2:校验code和返回值')
        self.assertEqual(401, res.status_code)
        expected = {'errorCode': -2009, 'errorMsg': ''}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_21(self):
        """身份校验-不存在的wps_sid"""

        step('STEP1:新建1条便签主体')

        body = {
            'noteId': self.noteId,

        }
        res = self.apiRequest.note_post(self.host + self.path, self.userId, self.sidB, body,
                                        )
        step('STEP2:校验code和返回值')
        self.assertEqual(412, res.status_code)
        expected = {'errorCode': -1011, 'errorMsg': 'user change!'}
        self.outPutResult.check_out(expected=expected, actual=res.json())
