import time
import unittest

from parameterized import parameterized

from business.apiRequest import ApiRequests
from business.generateNote import GenerateNote
from business.wipeNote import WipeNote
from common.AES_tool import encry
from common.caseLog import class_case_log, step
from common.checkResult import CheckResult
from common.yamlOperator import YamlOperator


@class_case_log
class TestCaseSetNoteContentInput(unittest.TestCase):
    apiRequests = ApiRequests()
    wipeNote = WipeNote()
    generateNote = GenerateNote()
    outPutResult = CheckResult()
    envConfig = YamlOperator().env_config()
    setNoteContentConfig = YamlOperator.api_data_config('setNoteContent')
    host = envConfig['host']
    userId = envConfig['user_id']
    sid = envConfig['sid']
    sidB = envConfig['sid']
    notPresentSid = envConfig['notPresentSid']
    setNoteInfoPath = setNoteContentConfig['setNoteInfoPath']
    key = envConfig['key'].encode('utf-8')
    iv = envConfig['iv'].encode('utf-8')
    addNoteContentPath = setNoteContentConfig['addNoteContentPath']

    def setUp(self) -> None:
        """清空数据"""
        self.wipeNote.wipeNote(self.userId, self.sid)

    must_key = [
        (None,),
        ('',)
    ]

    @parameterized.expand(must_key)
    def testCase_01(self, param):
        """新建便签内容input_title1,None,2,空字符串"""
        step('STEP1:设置便签主体')
        noteId = str(int(time.time() * 1000)) + '_noteId'
        body = {
            'noteId': noteId
        }
        res = self.apiRequests.note_post(self.host + self.setNoteInfoPath, self.userId, self.sid, body)
        contentVersion = res.json()['infoVersion']
        step('STEP2:新建便签内容')
        title = encry('恭喜', self.key, self.iv)
        summary = encry('恭喜发财', self.key, self.iv)
        text_body = encry('中秋节快乐', self.key, self.iv)
        body = {
            'noteId': param,
            'title': title,
            'summary': summary,
            'body': text_body,
            'localContentVersion': contentVersion,
            'BodyType': 0

        }
        res = self.apiRequests.note_post(self.host + self.addNoteContentPath, self.userId, self.sid, body)
        self.assertEqual(500, res.status_code)
        expected = {'errorCode': -7, 'errorMsg': '参数不合法！'}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_02(self):
        """新建便签内容input_title1,None,2,空字符串"""
        step('STEP1:设置便签主体')
        noteId = str(int(time.time() * 1000)) + '_noteId'
        body = {
            'noteId': noteId
        }
        res = self.apiRequests.note_post(self.host + self.setNoteInfoPath, self.userId, self.sid, body)
        contentVersion = res.json()['infoVersion']
        step('STEP2:新建便签内容')
        title = encry('恭喜', self.key, self.iv)
        summary = encry('恭喜发财', self.key, self.iv)
        text_body = encry('中秋节快乐', self.key, self.iv)
        body = {
            'noteId': noteId,
            'title': title,
            'summary': summary,
            'body': text_body,
            'localContentVersion': contentVersion,
            'BodyType': 0

        }
        body.pop('noteId')
        res = self.apiRequests.note_post(self.host + self.addNoteContentPath, self.userId, self.sid, body)
        self.assertEqual(500, res.status_code)
        expected = {'errorCode': -7, 'errorMsg': '参数不合法！'}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    must_key = [
        ('9999999999999999999999999999999999999999999999999999999999999999999999999999',)
    ]

    @parameterized.expand(must_key)
    def testCase_03(self, param):
        """新建便签内容input_title1,None,2,空字符串"""
        step('STEP1:设置便签主体')
        noteId = str(int(time.time() * 1000)) + '_noteId'
        body = {
            'noteId': noteId
        }
        res = self.apiRequests.note_post(self.host + self.setNoteInfoPath, self.userId, self.sid, body)
        contentVersion = res.json()['infoVersion']
        step('STEP2:新建便签内容')
        title = encry('恭喜', self.key, self.iv)
        summary = encry('恭喜发财', self.key, self.iv)
        text_body = encry('中秋节快乐', self.key, self.iv)
        body = {
            'noteId': param,
            'title': title,
            'summary': summary,
            'body': text_body,
            'localContentVersion': contentVersion,
            'BodyType': 0

        }
        res = self.apiRequests.note_post(self.host + self.addNoteContentPath, self.userId, self.sid, body)
        self.assertEqual(500, res.status_code)
        expected = {'errorCode': -7, 'errorMsg': '参数不合法！'}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    must_key = ['！@#￥', '你好']

    @parameterized.expand(must_key)
    def testCase_04(self, param):
        """新建便签内容input_title1,None,2,空字符串"""
        step('STEP1:设置便签主体')
        noteId = str(int(time.time() * 1000)) + '_noteId'
        body = {
            'noteId': noteId
        }
        res = self.apiRequests.note_post(self.host + self.setNoteInfoPath, self.userId, self.sid, body)
        contentVersion = res.json()['infoVersion']
        step('STEP2:新建便签内容')
        title = encry('恭喜', self.key, self.iv)
        summary = encry('恭喜发财', self.key, self.iv)
        text_body = encry('中秋节快乐', self.key, self.iv)
        body = {
            'noteId': param,
            'title': title,
            'summary': summary,
            'body': text_body,
            'localContentVersion': contentVersion,
            'BodyType': 0

        }
        res = self.apiRequests.note_post(self.host + self.addNoteContentPath, self.userId, self.sid, body)
        self.assertEqual(500, res.status_code)
        expected = {'errorCode': -7, 'errorMsg': str}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    must_key = ['1', "1"]

    @parameterized.expand(must_key)
    def testCase_05(self, param):
        """新建便签内容input_title1,None,2,空字符串"""
        step('STEP1:设置便签主体')
        noteId = str(int(time.time() * 1000)) + '_noteId'
        body = {
            'noteId': noteId
        }
        res = self.apiRequests.note_post(self.host + self.setNoteInfoPath, self.userId, self.sid, body)
        contentVersion = res.json()['infoVersion']
        step('STEP2:新建便签内容')
        title = encry('恭喜', self.key, self.iv)
        summary = encry('恭喜发财', self.key, self.iv)
        text_body = encry('中秋节快乐', self.key, self.iv)
        body = {
            'noteId': param,
            'title': title,
            'summary': summary,
            'body': text_body,
            'localContentVersion': contentVersion,
            'BodyType': 0

        }
        res = self.apiRequests.note_post(self.host + self.addNoteContentPath, self.userId, self.sid, body)
        self.assertEqual(200, res.status_code)
        expected = {'responseTime': int, 'contentVersion': int, 'contentUpdateTime': int}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    title_None = [
        (None,),
        ('',)
    ]

    @parameterized.expand(title_None)
    def testCase_06(self, param):
        """新建便签内容input_title1,None,2,空字符串"""
        step('STEP1:设置便签主体')
        noteId = str(int(time.time() * 1000)) + '_noteId'
        body = {
            'noteId': noteId
        }
        res = self.apiRequests.note_post(self.host + self.setNoteInfoPath, self.userId, self.sid, body)
        contentVersion = res.json()['infoVersion']
        step('STEP2:新建便签内容')
        # title = encry(param, self.key, self.iv)
        summary = encry('恭喜发财', self.key, self.iv)
        text_body = encry('中秋节快乐', self.key, self.iv)
        body = {
            'noteId': noteId,
            'title': param,
            'summary': summary,
            'body': text_body,
            'localContentVersion': contentVersion,
            'BodyType': 0

        }
        res = self.apiRequests.note_post(self.host + self.addNoteContentPath, self.userId, self.sid, body)
        self.assertEqual(200, res.status_code)
        expected = {'responseTime': int, 'contentVersion': contentVersion, 'contentUpdateTime': int}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    max_title = [

        ('散文是表达作自由，多种题材，它可以让我们感受到生活的美好和世界的宽广。总之，散文是一种非常自由、灵活、贴近生活的文学体裁，它可以让人们感受到生活的美好和世界的宽广,散文通常没有固定的情节和结构，它不需要像小说那样考虑故事情节的发展和人物性格的塑造。相反，散文更加注重表达作者对于某个主题或者某些现象的看法、感受和思考，以及对于自身经历和心境的描写。散文的表现手法也非常自由，可以运用各种写作技巧如寓言、象征、隐喻等，但也可以不用任何技巧，直接表达自己的感受和思考',)
    ]

    @parameterized.expand(max_title)
    def testCase_07(self, param):
        """新建便签内容，超长字符串"""
        step('STEP1:设置便签主体')
        noteId = str(int(time.time() * 1000)) + '_noteId'
        body = {
            'noteId': noteId
        }
        res = self.apiRequests.note_post(self.host + self.setNoteInfoPath, self.userId, self.sid, body)
        contentVersion = res.json()['infoVersion']
        step('STEP2:新建便签内容')
        title = encry(param, self.key, self.iv)
        summary = encry('恭喜发财', self.key, self.iv)
        text_body = encry('中秋节快乐', self.key, self.iv)
        body = {
            'noteId': noteId,
            'title': title,
            'summary': summary,
            'body': text_body,
            'localContentVersion': contentVersion,
            'BodyType': 0

        }
        res = self.apiRequests.note_post(self.host + self.addNoteContentPath, self.userId, self.sid, body)
        self.assertEqual(500, res.status_code)
        expected = {'errorCode': -7, 'errorMsg': str}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    title = ['!!!!@@@qwqwqw', '123 ' or ' 1=1']

    @parameterized.expand(title)
    def testCase_08(self, param):
        """title包含特殊字符"""
        step('STEP1:设置便签主体')
        noteId = str(int(time.time() * 1000)) + '_noteId'
        body = {
            'noteId': noteId
        }
        res = self.apiRequests.note_post(self.host + self.setNoteInfoPath, self.userId, self.sid, body)
        contentVersion = res.json()['infoVersion']
        step('STEP2:新建便签内容')
        title = encry(param, self.key, self.iv)
        summary = encry('恭喜发财', self.key, self.iv)
        text_body = encry('中秋节快乐', self.key, self.iv)
        body = {
            'noteId': noteId,
            'title': title,
            'summary': summary,
            'body': text_body,
            'localContentVersion': contentVersion,
            'BodyType': 0

        }
        res = self.apiRequests.note_post(self.host + self.addNoteContentPath, self.userId, self.sid, body)
        self.assertEqual(200, res.status_code)

    def testCase_09(self):
        """title删除key"""
        step('STEP1:设置便签主体')
        noteId = str(int(time.time() * 1000)) + '_noteId'
        body = {
            'noteId': noteId
        }
        res = self.apiRequests.note_post(self.host + self.setNoteInfoPath, self.userId, self.sid, body)
        contentVersion = res.json()['infoVersion']
        step('STEP2:新建便签内容')
        title = encry('恭喜', self.key, self.iv)
        summary = encry('恭喜发财', self.key, self.iv)
        text_body = encry('中秋节快乐', self.key, self.iv)
        body = {
            'noteId': noteId,
            'title': title,
            'summary': summary,
            'body': text_body,
            'localContentVersion': contentVersion,
            'BodyType': 0

        }
        body.pop('title')
        res = self.apiRequests.note_post(self.host + self.addNoteContentPath, self.userId, self.sid, body)
        self.assertEqual(200, res.status_code)
        expected = {'responseTime': int, 'contentVersion': contentVersion, 'contentUpdateTime': int}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    summary_None = [
        (None,),
        ('',)
    ]

    @parameterized.expand(summary_None)
    def testCase_10(self, param):
        """summary为1，None,2空字符串"""
        step('STEP1:设置便签主体')
        noteId = str(int(time.time() * 1000)) + '_noteId'
        body = {
            'noteId': noteId
        }
        res = self.apiRequests.note_post(self.host + self.setNoteInfoPath, self.userId, self.sid, body)
        contentVersion = res.json()['infoVersion']
        step('STEP2:新建便签内容')
        title = encry('恭喜', self.key, self.iv)
        # summary = encry(param, self.key, self.iv)
        text_body = encry('中秋节快乐', self.key, self.iv)
        body = {
            'noteId': noteId,
            'title': title,
            'summary': param,
            'body': text_body,
            'localContentVersion': contentVersion,
            'BodyType': 0

        }
        res = self.apiRequests.note_post(self.host + self.addNoteContentPath, self.userId, self.sid, body)
        self.assertEqual(200, res.status_code)

    summary_max = [

        ('你的问题看起来像是在描述一个程序行为或结果的状态，但语言组织得不够清晰，我无法直接理解你的问题。看起来你正在尝试测试一个字符串是否等于"中秋节快乐"，但是在你尝试的字符串中存在一些额外的非打印字符，如这可能是因为在字符串被创建、接收或处理的过程中，这些字符被添加到了字符串中。你可以使用Python的 str.strip() 方法来删除字符串开头和结尾的空白字符（包括。这个方法会返回一个新的字符串，这个新的字符串不包含原始字符串开头和结尾的空白字符。在你的情况下，这应该可以解决问题。你的代码应该看起来像这样状态码为400"，但我需要更多的上下文信息才能帮助你。你能否提供更多的详细信息？例如，你正在使用的编程语言和框架，你试图执行的操作，或者你遇到的具体错误消息。这将有助于我更好地理解你的问题并提供更有效的帮助这将有助于我更好地理解你这将有助于我更好地理解你这将有助于我更好地理解你这将有助于我更好地理解你这将有助于我更好地理解你这将有助于我更好地理解你你的问题看起来像是在描述一个程序行为或结果的状态，但语言组织得不够清晰，我无法直接理解你的问题。看起来你正在尝试测试一个字符串是否等于你的问题看起来像是在描述一个程序行为或结果的状态，但语言组织得不够清晰，我无法直接理解你的问题。看起来你正在尝试测试一个字符串是否等于你的问题看起来像是在描述一个程序行为或结果的状态，但语言组织得不够清晰，我无法直接理解你的问题。看起来你正在尝试测试一个字符串是否等于你的问题看起来像是在描述一个程序行为或结果的状态，但语言组织得不够清晰，我无法直接理解你的问题。看起来你正在尝试测试一个字符串是否等于你的问题看起来像是在描述一个程序行为或结果的状态，但语言组织得不够清晰，我无法直接理解你的问题。看起来你正在尝试测试一个字符串是否等于你的问题看起来像是在描述一个程序行为或结果的状态，但语言组织得不够清晰，我无法直接理解你的问题。看起来你正在尝试测试一个字符串是否等于你的问题看起来像是在描述一个程序行为或结果的状态，但语言组织得不够清晰，我无法直接理解你的问题。看起来你正在尝试测试一个字符串是否等于你的问题看起来像是在描述一个程序行为或结果的状态，但语言组织得不够清晰，我无法直接理解你的问题。看起来你正在尝试测试一个字符串是否等于你的问题看起来像是在描述一个程序行为或结果的状态，但语言组织得不够清晰，我无法直接理解你的问题。看起来你正在尝试测试一个字符串是否等于你的问题看起来像是在描述一个程序行为或结果的状态，但语言组织得不够清晰，我无法直接理解你的问题。看起来你正在尝试测试一个字符串是否等于你的问题看起来像是在描述一个程序行为或结果的状态，但语言组织得不够清晰，我无法直接理解你的问题。看起来你正在尝试测试一个字符串是否等于你的问题看起来像是在描述一个程序行为或结果的状态，但语言组织得不够清晰，我无法直接理解你的问题。看起来你正在尝试测试一个字符串是否等于你的问题看起来像是在描述一个程序行为或结果的状态，但语言组织得不够清晰，我无法直接理解你的问题。看起来你正在尝试测试一个字符串是否等于你的问题看起来像是在描述一个程序行为或结果的状态，但语言组织得不够清晰，我无法直接理解你的问题。看起来你正在尝试测试一个字符串是否等于你的问题看起来像是在描述一个程序行为或结果的状态，但语言组织得不够清晰，我无法直接理解你的问题。看起来你正在尝试测试一个字符串是否等于你的问题看起来像是在描述一个程序行为或结果的状态，但语言组织得不够清晰，我无法直接理解你的问题。看起来你正在尝试测试一个字符串是否等于你的问题看起来像是在描述一个程序行为或结果的状态，但语言组织得不够清晰，我无法直接理解你的问题。看起来你正在尝试测试一个字符串是否等于你的问题看起来像是在描述一个程序行为或结果的状态，但语言组织得不够清晰，我无法直接理解你的问题。看起来你正在尝试测试一个字符串是否等于你的问题看起来像是在描述一个程序行为或结果的状态，但语言组织得不够清晰，我无法直接理解你的问题。看起来你正在尝试测试一个字符串是否等于你的问题看起来像是在描述一个程序行为或结果的状态，但语言组织得不够清晰，我无法直接理解你的问题。看起来你正在尝试测试一个字符串是否等于你的问题看起来像是在描述一个程序行为或结果的状态，但语言组织得不够清晰，我无法直接理解你的问题。看起来你正在尝试测试一个字符串是否等于你的问题看起来像是在描述一个程序行为或结果的状态，但语言组织得不够清晰，我无法直接理解你的问题。看起来你正在尝试测试一个字符串是否等于你的问题看起来像是在描述一个程序行为或结果的状态，但语言组织得不够清晰，我无法直接理解你的问题。看起来你正在尝试测试一个字符串是否等于你的问题看起来像是在描述一个程序行为或结果的状态，但语言组织得不够清晰，我无法直接理解你的问题。看起来你正在尝试测试一个字符串是否等于你的问题看起来像是在描述一个程序行为或结果的状态，但语言组织得不够清晰，我无法直接理解你的问题。看起来你正在尝试测试一个字符串是否等于你的问题看起来像是在描述一个程序行为或结果的状态，但语言组织得不够清晰，我无法直接理解你的问题。看起来你正在尝试测试一个字符串是否等于你的问题看起来像是在描述一个程序行为或结果的状态，但语言组织得不够清晰，我无法直接理解你的问题。看起来你正在尝试测试一个字符串是否等于你的问题看起来像是在描述一个程序行为或结果的状态，但语言组织得不够清晰，我无法直接理解你的问题。看起来你正在尝试测试一个字符串是否等于你的问题看起来像是在描述一个程序行为或结果的状态，但语言组织得不够清晰，我无法直接理解你的问题。看起来你正在尝试测试一个字符串是否等于你的问题看起来像是在描述一个程序行为或结果的状态，但语言组织得不够清晰，我无法直接理解你的问题。看起来你正在尝试测试一个字符串是否等于',)]

    @parameterized.expand(summary_max)
    def testCase_11(self, param):
        """summary字符串超出最大字符"""
        step('STEP1:设置便签主体')
        noteId = str(int(time.time() * 1000)) + '_noteId'
        body = {
            'noteId': noteId
        }
        res = self.apiRequests.note_post(self.host + self.setNoteInfoPath, self.userId, self.sid, body)
        contentVersion = res.json()['infoVersion']
        step('STEP2:新建便签内容')
        title = encry('恭喜', self.key, self.iv)
        summary = encry(param, self.key, self.iv)
        text_body = encry('中秋节快乐', self.key, self.iv)
        body = {
            'noteId': noteId,
            'title': title,
            'summary': summary,
            'body': text_body,
            'localContentVersion': contentVersion,
            'BodyType': 0

        }
        res = self.apiRequests.note_post(self.host + self.addNoteContentPath, self.userId, self.sid, body)
        self.assertEqual(500, res.status_code)

    summary_contains_or = ['你好 ' or '1=1', '中秋"or" 1=1']

    @parameterized.expand(summary_contains_or)
    def testCase_12(self, param):
        """summary包括or的2种情况你好 ' or '1=1；2，中秋"or" 1=1 """
        step('STEP1:设置便签主体')
        noteId = str(int(time.time() * 1000)) + '_noteId'
        body = {
            'noteId': noteId
        }
        res = self.apiRequests.note_post(self.host + self.setNoteInfoPath, self.userId, self.sid, body)
        contentVersion = res.json()['infoVersion']
        step('STEP2:新建便签内容')
        title = encry('恭喜', self.key, self.iv)
        summary = encry(param, self.key, self.iv)
        text_body = encry('中秋节快乐', self.key, self.iv)
        body = {
            'noteId': noteId,
            'title': title,
            'summary': summary,
            'body': text_body,
            'localContentVersion': contentVersion,
            'BodyType': 0

        }
        res = self.apiRequests.note_post(self.host + self.addNoteContentPath, self.userId, self.sid, body)
        self.assertEqual(200, res.status_code)
        expected = {'responseTime': int, 'contentVersion': contentVersion, 'contentUpdateTime': int}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_13(self):
        """summary删除key"""
        step('STEP1:设置便签主体')
        noteId = str(int(time.time() * 1000)) + '_noteId'
        body = {
            'noteId': noteId
        }
        res = self.apiRequests.note_post(self.host + self.setNoteInfoPath, self.userId, self.sid, body)
        contentVersion = res.json()['infoVersion']
        step('STEP2:新建便签内容')
        title = encry('恭喜', self.key, self.iv)
        summary = encry('恭喜发财', self.key, self.iv)
        text_body = encry('中秋节快乐', self.key, self.iv)
        body = {
            'noteId': noteId,
            'title': title,
            'summary': summary,
            'body': text_body,
            'localContentVersion': contentVersion,
            'BodyType': 0

        }
        body.pop('summary')
        res = self.apiRequests.note_post(self.host + self.addNoteContentPath, self.userId, self.sid, body)
        self.assertEqual(200, res.status_code)
        expected = {'responseTime': int, 'contentVersion': int, 'contentUpdateTime': int}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    body_text = [
        (None,),
        ('',)
    ]

    @parameterized.expand(body_text)
    def testCase_14(self, param):
        """body为空 1,body_text为None;2,body_text为空字符串"""
        step('STEP1:设置便签主体')
        noteId = str(int(time.time() * 1000)) + '_noteId'
        body = {
            'noteId': noteId
        }
        res = self.apiRequests.note_post(self.host + self.setNoteInfoPath, self.userId, self.sid, body)
        contentVersion = res.json()['infoVersion']
        step('STEP2:新建便签内容')
        title = encry('恭喜', self.key, self.iv)
        summary = encry('恭喜发财', self.key, self.iv)
        # text_body = encry(param, self.key, self.iv)
        body = {
            'noteId': noteId,
            'title': title,
            'summary': summary,
            'body': param,
            'localContentVersion': contentVersion,
            'BodyType': 0

        }
        res = self.apiRequests.note_post(self.host + self.addNoteContentPath, self.userId, self.sid, body)
        self.assertEqual(412, res.status_code)
        expected = {'errorCode': -1012, 'errorMsg': 'Note body Requested!'}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_15(self):
        """body删除key"""
        step('STEP1:设置便签主体')
        noteId = str(int(time.time() * 1000)) + '_noteId'
        body = {
            'noteId': noteId
        }
        res = self.apiRequests.note_post(self.host + self.setNoteInfoPath, self.userId, self.sid, body)
        contentVersion = res.json()['infoVersion']
        step('STEP2:新建便签内容')
        title = encry('恭喜', self.key, self.iv)
        summary = encry('恭喜发财', self.key, self.iv)
        text_body = encry('中秋节快乐', self.key, self.iv)
        body = {
            'noteId': noteId,
            'title': title,
            'summary': summary,
            'body': text_body,
            'localContentVersion': contentVersion,
            'BodyType': 0

        }
        body.pop('body')
        res = self.apiRequests.note_post(self.host + self.addNoteContentPath, self.userId, self.sid, body)
        self.assertEqual(412, res.status_code)
        expected = {'errorCode': -1012, 'errorMsg': 'Note body Requested!'}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_16(self):
        """localContentVersion删除key"""
        step('STEP1:设置便签主体')
        noteId = str(int(time.time() * 1000)) + '_noteId'
        body = {
            'noteId': noteId
        }
        res = self.apiRequests.note_post(self.host + self.setNoteInfoPath, self.userId, self.sid, body)
        step('STEP2:新建便签内容')
        title = encry('恭喜', self.key, self.iv)
        summary = encry('恭喜发财', self.key, self.iv)
        text_body = encry('中秋节快乐', self.key, self.iv)
        body = {
            'noteId': noteId,
            'title': title,
            'summary': summary,
            'body': text_body,
            'BodyType': 0

        }

        res = self.apiRequests.note_post(self.host + self.addNoteContentPath, self.userId, self.sid, body)
        self.assertEqual(200, res.status_code)
        expected = {'responseTime': int, 'contentVersion': int, 'contentUpdateTime': int}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    localContentVersion_None = [
        (None,),
        ('',)
    ]

    @parameterized.expand(localContentVersion_None)
    def testCase_17(self, param):
        """localContentVersion为空值"""
        step('STEP1:设置便签主体')
        noteId = str(int(time.time() * 1000)) + '_noteId'
        body = {
            'noteId': noteId
        }
        res = self.apiRequests.note_post(self.host + self.setNoteInfoPath, self.userId, self.sid, body)
        step('STEP2:新建便签内容')
        title = encry('恭喜', self.key, self.iv)
        summary = encry('恭喜发财', self.key, self.iv)
        text_body = encry('中秋节快乐', self.key, self.iv)
        body = {
            'noteId': noteId,
            'title': title,
            'summary': summary,
            'body': text_body,
            'localContentVersion': param,
            'BodyType': 0

        }

        res = self.apiRequests.note_post(self.host + self.addNoteContentPath, self.userId, self.sid, body)
        self.assertEqual(200, res.status_code)
        expected = {'responseTime': int, 'contentVersion': int, 'contentUpdateTime': int}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    localContentVersion_negative = [-1, 1.5]

    @parameterized.expand(localContentVersion_negative)
    def testCase_18(self, param):
        """localContentVersion为小数"""
        step('STEP1:设置便签主体')
        noteId = str(int(time.time() * 1000)) + '_noteId'
        body = {
            'noteId': noteId
        }
        res = self.apiRequests.note_post(self.host + self.setNoteInfoPath, self.userId, self.sid, body)
        step('STEP2:新建便签内容')
        title = encry('恭喜', self.key, self.iv)
        summary = encry('恭喜发财', self.key, self.iv)
        text_body = encry('中秋节快乐', self.key, self.iv)
        body = {
            'noteId': noteId,
            'title': title,
            'summary': summary,
            'body': text_body,
            'localContentVersion': param,
            'BodyType': 0

        }

        res = self.apiRequests.note_post(self.host + self.addNoteContentPath, self.userId, self.sid, body)
        self.assertEqual(200, res.status_code)
        expected = {'responseTime': int, 'contentVersion': int, 'contentUpdateTime': int}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    localContentVersion_str = ['1', "1"]

    @parameterized.expand(localContentVersion_str)
    def testCase_19(self, param):
        """localContentVersion为字符串"""
        step('STEP1:设置便签主体')
        noteId = str(int(time.time() * 1000)) + '_noteId'
        body = {
            'noteId': noteId
        }
        res = self.apiRequests.note_post(self.host + self.setNoteInfoPath, self.userId, self.sid, body)
        step('STEP2:新建便签内容')
        title = encry('恭喜', self.key, self.iv)
        summary = encry('恭喜发财', self.key, self.iv)
        text_body = encry('中秋节快乐', self.key, self.iv)
        body = {
            'noteId': noteId,
            'title': title,
            'summary': summary,
            'body': text_body,
            'localContentVersion': param,
            'BodyType': 0

        }

        res = self.apiRequests.note_post(self.host + self.addNoteContentPath, self.userId, self.sid, body)
        self.assertEqual(200, res.status_code)
        expected = {'responseTime': int, 'contentVersion': int, 'contentUpdateTime': int}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    BodyType = [
        (None,),
        ('',)
    ]

    @parameterized.expand(BodyType)
    def testCase_20(self, param):
        """BodyType为1,None,2,'',"""
        step('STEP1:设置便签主体')
        noteId = str(int(time.time() * 1000)) + '_noteId'
        body = {
            'noteId': noteId
        }
        res = self.apiRequests.note_post(self.host + self.setNoteInfoPath, self.userId, self.sid, body)
        contentVersion = res.json()['infoVersion']
        step('STEP2:新建便签内容')
        title = encry('恭喜', self.key, self.iv)
        summary = encry('恭喜发财', self.key, self.iv)
        text_body = encry('中秋节快乐', self.key, self.iv)
        body = {
            'noteId': noteId,
            'title': title,
            'summary': summary,
            'body': text_body,
            'localContentVersion': contentVersion,
            'BodyType': param

        }

        res = self.apiRequests.note_post(self.host + self.addNoteContentPath, self.userId, self.sid, body)
        self.assertEqual(200, res.status_code)
        expected = {'responseTime': int, 'contentVersion': int, 'contentUpdateTime': int}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_21(self):
        """BodyType删除key"""
        step('STEP1:设置便签主体')
        noteId = str(int(time.time() * 1000)) + '_noteId'
        body = {
            'noteId': noteId
        }
        res = self.apiRequests.note_post(self.host + self.setNoteInfoPath, self.userId, self.sid, body)
        contentVersion = res.json()['infoVersion']
        step('STEP2:新建便签内容')
        title = encry('恭喜', self.key, self.iv)
        summary = encry('恭喜发财', self.key, self.iv)
        text_body = encry('中秋节快乐', self.key, self.iv)
        body = {
            'noteId': noteId,
            'title': title,
            'summary': summary,
            'body': text_body,
            'localContentVersion': contentVersion,
            'BodyType': 0

        }
        body.pop('BodyType')

        res = self.apiRequests.note_post(self.host + self.addNoteContentPath, self.userId, self.sid, body)
        self.assertEqual(200, res.status_code)
        expected = {'responseTime': int, 'contentVersion': int, 'contentUpdateTime': int}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_22(self):
        """身份验证"""
        step('STEP1:设置便签主体')
        noteId = str(int(time.time() * 1000)) + '_noteId'
        body = {
            'noteId': noteId
        }
        res = self.apiRequests.note_post(self.host + self.setNoteInfoPath, self.userId, self.sid, body)
        contentVersion = res.json()['infoVersion']
        step('STEP2:新建便签内容')
        title = encry('恭喜', self.key, self.iv)
        summary = encry('恭喜发财', self.key, self.iv)
        text_body = encry('中秋节快乐', self.key, self.iv)
        body = {
            'noteId': noteId,
            'title': title,
            'summary': summary,
            'body': text_body,
            'localContentVersion': contentVersion,
            'BodyType': 0

        }

        res = self.apiRequests.note_post(self.host + self.addNoteContentPath, self.userId, self.sidB, body)
        self.assertEqual(200, res.status_code)
        expected = {'responseTime': int, 'contentVersion': int, 'contentUpdateTime': int}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_23(self):
        """身份验证"""
        step('STEP1:设置便签主体')
        noteId = str(int(time.time() * 1000)) + '_noteId'
        body = {
            'noteId': noteId
        }
        res = self.apiRequests.note_post(self.host + self.setNoteInfoPath, self.userId, self.sid, body)
        contentVersion = res.json()['infoVersion']
        step('STEP2:新建便签内容')
        title = encry('恭喜', self.key, self.iv)
        summary = encry('恭喜发财', self.key, self.iv)
        text_body = encry('中秋节快乐', self.key, self.iv)
        body = {
            'noteId': noteId,
            'title': title,
            'summary': summary,
            'body': text_body,
            'localContentVersion': contentVersion,
            'BodyType': 0

        }

        res = self.apiRequests.note_post(self.host + self.addNoteContentPath, self.userId, self.notPresentSid, body)
        self.assertEqual(401, res.status_code)
        expected = {'errorCode': -2010, 'errorMsg': ''}
        self.outPutResult.check_out(expected=expected, actual=res.json())

    def testCase_24(self):
        """身份验证-删除cookie"""
        step('STEP1:设置便签主体')
        noteId = str(int(time.time() * 1000)) + '_noteId'
        body = {
            'noteId': noteId
        }
        res = self.apiRequests.note_post(self.host + self.setNoteInfoPath, self.userId, self.sid, body)
        contentVersion = res.json()['infoVersion']
        step('STEP2:新建便签内容')
        title = encry('恭喜', self.key, self.iv)
        summary = encry('恭喜发财', self.key, self.iv)
        text_body = encry('中秋节快乐', self.key, self.iv)
        body = {
            'noteId': noteId,
            'title': title,
            'summary': summary,
            'body': text_body,
            'localContentVersion': contentVersion,
            'BodyType': 0

        }
        new_header = {
            'Content-type': 'application/json',
            'X-user-key': str(self.userId),
            'Cookie': f'wps_sid={self.sid}'
        }
        new_header.pop('Cookie')

        res = self.apiRequests.note_post(self.host + self.addNoteContentPath, self.userId, self.sid, body, new_header)
        self.assertEqual(401, res.status_code)
        expected = {'errorCode': -2009, 'errorMsg': ''}
        self.outPutResult.check_out(expected=expected, actual=res.json())
