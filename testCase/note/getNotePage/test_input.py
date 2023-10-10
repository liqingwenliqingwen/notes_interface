import unittest

from parameterized import parameterized

from business.apiRequest import ApiRequests
from business.generateNote import GenerateNote
from business.wipeNote import WipeNote
from common.caseLog import step, class_case_log
from common.checkResult import CheckResult
from common.yamlOperator import YamlOperator


@class_case_log
class TestCaseGetNotePageInput(unittest.TestCase):
    outPutResult = CheckResult()
    apiRequests = ApiRequests()

    wipeNote = WipeNote()
    generateNote = GenerateNote()

    envConfig = YamlOperator().env_config()
    getPageNoteConfig = YamlOperator.api_data_config('getPageNote')

    host = envConfig['host']
    userId = envConfig['user_id']
    sid = envConfig['sid']
    key = envConfig['key'].encode('utf-8')
    iv = envConfig['iv'].encode('utf-8')
    addNotePath = getPageNoteConfig['addNotePath']
    addNoteContent = getPageNoteConfig['addNoteContent']

    def setUp(self) -> None:
        """数据清理"""

        self.wipeNote.wipeNote(self.userId, self.sid)

    must_key_userId = [
        (None,),
        (236948373.5,)
    ]

    @parameterized.expand(must_key_userId)
    def testCase_01(self, param):
        """获取首页便签input：user_id,参数化1,输入小数点 2，字段为空值"""

        step('STEP1:造1条测试数据')
        self.generateNote.generate_note_test(1, self.userId, self.sid)
        step('STEP2:获取便签列表')
        getNotePath = '/v3/notesvr/user/{}/home/startindex/{}/rows/{}/notes'.format(param, 1, 10)
        res = self.apiRequests.note_get(self.host + getNotePath, self.userId, self.sid)
        step('STEP3:校验code')
        self.assertEqual(500, res.status_code)
        step('STEP4:校验返回值')
        expected = {'errorCode': -7, 'errorMsg': '参数类型错误！'}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_02(self):
        """获取首页便签input：user_id,不存在的user_id"""

        step('STEP1:造1条测试数据')
        self.generateNote.generate_note_test(1, self.userId, self.sid)
        step('STEP2:获取便签列表')
        getNotePath = '/v3/notesvr/user/{}/home/startindex/{}/rows/{}/notes'.format(236948375, 1, 10)
        res = self.apiRequests.note_get(self.host + getNotePath, self.userId, self.sid)
        step('STEP3:校验code')
        self.assertEqual(412, res.status_code)
        step('STEP4:校验返回值')
        expected = {'errorCode': -1011, 'errorMsg': 'user change!'}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_03(self):
        """获取首页便签input：user_id,输入空字符串"""
        step('STEP1:造1条数据')
        self.generateNote.generate_note_test(1, self.userId, self.sid)

        step('STEP2:获取便签列表')
        getNotePath = '/v3/notesvr/user/{}/home/startindex/{}/rows/{}/notes'.format('', 1, 10)
        res = self.apiRequests.note_get(self.host + getNotePath, self.userId, self.sid)
        step('STEP3:校验code')
        self.assertEqual(404, res.status_code)
        step('STEP4:校验返回值')
        expected = {'timestamp': str, 'status': 404, 'error': 'Not Found', 'message': 'No message available',
                    'path': '/v3/notesvr/user//home/startindex/1/rows/10/notes'}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_04(self):
        """获取首页便签input——userId，输入负数"""

        step('STEP1:新建1条测试数据')
        self.generateNote.generate_note_test(1, self.userId, self.sid)
        step('STEP2:获取便签列表')
        getNotePath = '/v3/notesvr/user/{}/home/startindex/{}/rows/{}/notes'.format(-236948373, 1, 10)
        res = self.apiRequests.note_get(self.host + getNotePath, self.userId, self.sid)
        step('STEP3:校验code')
        self.assertEqual(412, res.status_code)
        step('STEP4:校验返回值')
        expected = {'errorCode': -1011, 'errorMsg': 'user change!'}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_05(self):
        """获取首页便签input-startIndex空值校验"""

        step('STEP1:造两条测试数据')
        self.generateNote.generate_note_test(1, self.userId, self.sid)
        step('STEP2:获取便签列表')
        getNotePath = '/v3/notesvr/user/{}/home/startindex/{}/rows/{}/notes'.format(236948373, '', 10)
        res = self.apiRequests.note_get(self.host + getNotePath, self.userId, self.sid)
        self.assertEqual(404, res.status_code)
        expected = {'timestamp': str, 'status': 404, 'error': 'Not Found',
                    'message': 'No message available',
                    'path': '/v3/notesvr/user/236948373/home/startindex//rows/10/notes'}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    must_key_userId = [
        ('236948373"or"1=1',)
    ]

    @parameterized.expand(must_key_userId)
    def testCase_06(self, param):
        """获取首页便签input：user_id,参数化1,输入小数点 2，字段为空值"""

        step('STEP1:造1条测试数据')
        self.generateNote.generate_note_test(1, self.userId, self.sid)
        step('STEP2:获取便签列表')
        getNotePath = '/v3/notesvr/user/{}/home/startindex/{}/rows/{}/notes'.format(param, 1, 10)
        res = self.apiRequests.note_get(self.host + getNotePath, self.userId, self.sid)
        step('STEP3:校验code')
        self.assertEqual(500, res.status_code)
        step('STEP4:校验返回值')
        expected = {'errorCode': -7, 'errorMsg': '参数类型错误！'}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_07(self):
        """获取首页便签input：user_id,参数化1,输入小数点 2，字段为空值"""

        step('STEP1:造1条测试数据')
        self.generateNote.generate_note_test(1, self.userId, self.sid)
        step('STEP2:获取便签列表')
        getNotePath = '/v3/notesvr/user/{}/home/startindex/{}/rows/{}/notes'.format('236948373' or '1=1', 1, 10)
        res = self.apiRequests.note_get(self.host + getNotePath, '236948373' or '1=1', self.sid)
        step('STEP3:校验code')
        self.assertEqual(200, res.status_code)
        step('STEP4:校验返回值')
        expected = {'responseTime': 0, 'webNotes': []}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_08(self):
        """获取首页便签input：user_id,参数化1,输入小数点 2，字段为空值"""

        step('STEP1:造1条测试数据')
        self.generateNote.generate_note_test(1, self.userId, self.sid)
        step('STEP2:获取便签列表')
        getNotePath = '/v3/notesvr/user/{}/home/startindex/{}/rows/{}/notes'.format('!@#$', 1, 10)
        res = self.apiRequests.note_get(self.host + getNotePath, self.userId, self.sid)
        step('STEP3:校验code')
        self.assertEqual(404, res.status_code)
        step('STEP4:校验返回值')
        expected = {'timestamp': str, 'status': 404, 'error': 'Not Found',
                    'message': 'No message available', 'path': str}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    abnormal_startIndex = [
        (None,),
        (1.5,)
    ]

    @parameterized.expand(abnormal_startIndex)
    def testCase_09(self, param):
        """获取首页便签input-startIndex1,空值校验2,小数点校验"""
        step('STEP1:新建1条测试数据')
        self.generateNote.generate_note_test(1, self.userId, self.sid)
        step('STEP2:获取便签列表')
        getNotePath = '/v3/notesvr/user/{}/home/startindex/{}/rows/{}/notes'.format(236948373, param, 10)
        res = self.apiRequests.note_get(self.host + getNotePath, self.userId, self.sid)
        step('STEP3:校验code')
        self.assertEqual(500, res.status_code)
        step('STEP4:校验返回值')
        expected = {'errorCode': -7, 'errorMsg': '参数类型错误！'}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    startIndex_int_MAX_MIN = [(2147483648,), (-2147483649,)]

    @parameterized.expand(startIndex_int_MAX_MIN)
    def testCase_10(self, param):
        """获取首页便签input-startIndex1,int的最大值校验，int的最小值"""

        step('STEP1:造1条测试数据')
        self.generateNote.generate_note_test(1, self.userId, self.sid)
        step('STEP2:获取便签列表')
        getNotePath = '/v3/notesvr/user/{}/home/startindex/{}/rows/{}/notes'.format(236948373, param, 10)

        res = self.apiRequests.note_get(self.host + getNotePath, self.userId, self.sid)
        self.assertEqual(500, res.status_code)
        expected = {'errorCode': -7, 'errorMsg': '参数类型错误！'}

        self.outPutResult.check_out(expected=expected, actual=res.json())

    startIndex_str = ['1', "1"]

    @parameterized.expand(startIndex_str)
    def testCase_11(self, param):
        """获取首页便签input-startIndex1,校验输入字符串1"""

        step('STEP1:造两条测试数据')
        self.generateNote.generate_note_test(1, self.userId, self.sid)
        step('STEP2:获取便签列表')
        getNotePath = '/v3/notesvr/user/{}/home/startindex/{}/rows/{}/notes'.format(236948373, param, 10)
        res = self.apiRequests.note_get(self.host + getNotePath, param, self.sid)
        self.assertEqual(200, res.status_code)

    startIndex_str = [
        (1.5,)
    ]

    @parameterized.expand(startIndex_str)
    def testCase_12(self, param):
        """获取首页便签input-startIndex1,校验输入字符串1"""

        step('STEP1:造两条测试数据')
        self.generateNote.generate_note_test(1, self.userId, self.sid)
        step('STEP2:获取便签列表')
        getNotePath = '/v3/notesvr/user/{}/home/startindex/{}/rows/{}/notes'.format(236948373, param, 10)
        res = self.apiRequests.note_get(self.host + getNotePath, param, self.sid)
        self.assertEqual(500, res.status_code)
        expected = {'errorCode': -7, 'errorMsg': '参数类型错误！'}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_13(self):
        """获取首页便签input-startIndex1,校验输入字符串1"""

        step('STEP1:造两条测试数据')
        self.generateNote.generate_note_test(1, self.userId, self.sid)
        step('STEP2:获取便签列表')
        getNotePath = '/v3/notesvr/user/{}/home/startindex/{}/rows/{}/notes'.format(236948373, -1, 10)
        res = self.apiRequests.note_get(self.host + getNotePath, -1, self.sid)
        self.assertEqual(200, res.status_code)
        expected = {'responseTime': 0, 'webNotes': list}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    must_key_rows = [
        (None,),
        (1.5,)
    ]

    @parameterized.expand(must_key_rows)
    def testCase_14(self, param):
        """获取首页便签input-rows,1，输入None,2,输入小数"""

        step('STEP1:造1条测试数据')
        self.generateNote.generate_note_test(1, self.userId, self.sid)

        step('STEP2:获取便签列表')
        getNotePath = '/v3/notesvr/user/{}/home/startindex/{}/rows/{}/notes'.format(236948373, param, 10)
        res = self.apiRequests.note_get(self.host + getNotePath, param, self.sid)
        self.assertEqual(500, res.status_code)
        expected = {'errorCode': -7, 'errorMsg': '参数类型错误！'}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    must_key_rows = [
        ('',)
    ]

    @parameterized.expand(must_key_rows)
    def testCase_15(self, param):
        """获取首页便签input-rows,校验输入空字符串"""
        step('STEP1:造1条测试数据')
        self.generateNote.generate_note_test(1, self.userId, self.sid)
        step('STEP2:获取便签列表')
        getNotePath = '/v3/notesvr/user/{}/home/startindex/{}/rows/{}/notes'.format(236948373, 0, param)
        res = self.apiRequests.note_get(self.host + getNotePath, self.userId, self.sid)
        step('STEP3:校验code')
        self.assertEqual(404, res.status_code)
        step('STEP4:校验返回值')
        expected = {'timestamp': str, 'status': 404, 'error': 'Not Found', 'message': 'No message available',
                    'path': '/v3/notesvr/user/236948373/home/startindex/0/rows//notes'}

        self.outPutResult.check_out(expected=expected, actual=res.json())

    must_key_rows = [(-10,), ("10",), ('10',)]

    @parameterized.expand(must_key_rows)
    def testCase_16(self, param):
        """获取首页便签input-rows,校验1,输入负数2,输入单引号字符串3，输入双引号字符串"""

        step('STEP1:造1条测试数据')
        self.generateNote.generate_note_test(1, self.userId, self.sid)
        step('STEP2:获取便签列表')

        getNotePath = '/v3/notesvr/user/{}/home/startindex/{}/rows/{}/notes'.format(236948373, 0, param)
        res = self.apiRequests.note_get(self.host + getNotePath, self.userId, self.sid)
        self.assertEqual(200, res.status_code)
        expected = {}

    must_key_rows = [(-2147483649,), (2147483649,)]

    @parameterized.expand(must_key_rows)
    def testCase_17(self, param):
        """获取首页便签input-rows,校验1,输入负数2,输入单引号字符串3，输入双引号字符串"""

        step('STEP1:造1条测试数据')
        self.generateNote.generate_note_test(1, self.userId, self.sid)
        step('STEP2:获取便签列表')

        getNotePath = '/v3/notesvr/user/{}/home/startindex/{}/rows/{}/notes'.format(236948373, 0, param)
        res = self.apiRequests.note_get(self.host + getNotePath, self.userId, self.sid)
        self.assertEqual(500, res.status_code)
        expected = {'errorCode': -7, 'errorMsg': '参数类型错误！'}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    wps_sid_param = ['V02SzZhvW5p4R-F9xWxYg1FnX3fb6XI00a6c5883000e1f8b94', '']

    @parameterized.expand(wps_sid_param)
    def testCase_18(self, param):
        """wps——sid身份校验-不存在的wps_id"""

        step('STEP1:造1条测试数据')
        self.generateNote.generate_note_test(1, self.userId, self.sid)
        step('STEP2:获取便签列表')
        getNotePath = '/v3/notesvr/user/{}/home/startindex/{}/rows/{}/notes'.format(236948373, 0, 10)
        res = self.apiRequests.note_get(self.host + getNotePath, self.userId, param)
        step('STEP3:校验code')
        self.assertEqual(401, res.status_code)
        step('STEP4:校验返回值')
        expected = {'errorCode': -2010, 'errorMsg': ''}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    wps_sid_param = [
        ('V02SzZhvW5p4R-F9xWxYg1FnX3fb6XI00a6c5883000e1f8b85',)
    ]

    @parameterized.expand(wps_sid_param)
    def testCase_19(self, param):
        """wps——sid删除key,wps-sid"""

        step('STEP1:造数据')
        self.generateNote.generate_note_test(1, self.userId, self.sid)
        step('STEP2:获取便签列表')

        getNotePath = '/v3/notesvr/user/{}/home/startindex/{}/rows/{}/notes'.format(236948373, 0, 10)

        res = self.apiRequests.note_get(self.host + getNotePath, self.userId, param)
        self.assertEqual(401, res.status_code)
        expected = {'errorCode': -2010, 'errorMsg': ''}
        self.outPutResult.check_out(expected=expected, actual=res.json())
