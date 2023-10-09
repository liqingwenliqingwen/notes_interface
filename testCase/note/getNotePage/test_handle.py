import unittest

from business.apiRequest import ApiRequests
from business.generateNote import GenerateNote
from common.caseLog import step, class_case_log, info
from common.checkResult import CheckResult


@class_case_log
class TestCaseGetNotePageHandel(unittest.TestCase):
    generateTestNote = GenerateNote()
    apiRequest = ApiRequests()
    outPutResult = CheckResult()

    userId = '236948373'
    sid = 'V02SzZhvW5p4R-F9xWxYg1FnX3fb6XI00a6c5883000e1f8b95'
    host = 'http://note-api.wps.cn'

    getPageNotePath = '/v3/notesvr/user/{}/home/startindex/{}/rows/{}/notes'.format(236948373, 0, 1)

    sidB = 'V02S35NyFBbexxp5lFEke0wbV5kCvd400a51247b001a52899b'
    userIdB = '441616795'

    def testCase01(self):
        """用户存在多条数据，rows=1,校验是否只能查询出一条数据"""
        step('STEP1:造两条数据')
        self.generateTestNote.generate_note_test(2, 236948373, 'V02SzZhvW5p4R-F9xWxYg1FnX3fb6XI00a6c5883000e1f8b95')

        res = self.apiRequest.note_get(self.host + self.getPageNotePath, self.userId, self.sid)
        noteId = [item['noteId'] for item in res.json()['webNotes']]
        if len(noteId) == 1:
            info('只查询到一条数据，校验成功')
        else:
            info('校验失败')

    def testCase02(self):
        """用户B下新增2条数据，用用户A查询"""
        step('STEP1:用户B造两条数据')
        self.generateTestNote.generate_note_test(2, self.userIdB, self.sidB)
        step('STEP2:用户A查询')
        res = self.apiRequest.note_get(self.host + self.getPageNotePath, self.userId, self.sidB)
        self.assertEqual(412, res.status_code, msg='参数正常')
        expected = {'errorCode': -1011, 'errorMsg': 'user change!'}
        self.outPutResult.check_out(expected=expected, actual=res.json())
