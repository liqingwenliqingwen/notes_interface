import time

from business.apiRequest import ApiRequests
from common.AES_tool import encry
from common.yamlOperator import YamlOperator


class GenerateNote:
    apiRequest = ApiRequests()
    envConfig = YamlOperator().env_config()
    host = envConfig['host']
    getPageNoteConfig = YamlOperator.api_data_config('getPageNote')
    addNotePath = getPageNoteConfig['addNotePath']
    addNoteContent = getPageNoteConfig['addNoteContent']

    key = envConfig['key'].encode('utf-8')
    iv = envConfig['iv'].encode('utf-8')

    def generate_note_test(self, num, userid, sid):
        noteIds = []

        # step('STEP2:根据输入的num数据，循环，例如：新增为2，造2条数据')
        for item in range(num):
            note_id = str(int(time.time() * 1000)) + '_noteId' + str(item)

            body = {
                'noteId': note_id
            }
            # step('STEP3:循环调用新增便签主体方法')
            res = self.apiRequest.note_post(self.host + self.addNotePath, userid, sid, body)

            noteIds.append(note_id)
            contentVersion = res.json()['infoVersion']

            # step('STEP4:新增便签内容')

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
            self.apiRequest.note_post(self.host + self.addNoteContent, userid, sid, body)

        return noteIds
