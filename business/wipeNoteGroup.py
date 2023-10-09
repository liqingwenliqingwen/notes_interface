from business.apiRequest import ApiRequests
from common.caseLog import step, info
from common.yamlOperator import YamlOperator


class WipeNoteGroup:
    apiRequest = ApiRequests()
    envConfig = YamlOperator().env_config()
    deleteNoteGroupConfig = YamlOperator.api_data_config('deleteNoteGroup')
    host = envConfig['host']
    getNoteGroupPath = deleteNoteGroupConfig['getNoteGroupPath']
    delNoteGroup = deleteNoteGroupConfig['delNoteGroup']

    def wipeNoteGroup(self, userid, sid):
        """根据用户id删除便签分组"""
        step('------------清空便签分组----------------------')
        body = {}
        res = self.apiRequest.note_post(self.host + self.getNoteGroupPath, userid, sid, body)
        info(f'res.status_code：{res.status_code}')
        info(f'res.json:{res.json()}')
        # step('STEP2:for循环接口结果列表，把所有groupId存储在一个列表上 groupIds')
        groupIds = [item['groupId'] for item in res.json()['noteGroups']]
        info(f'noteIds列表为:{groupIds}')
        if len(groupIds) == 0:
            info('获取到的便签分组列表长度为空，无需清空')
        else:
            # step('STEP3:循环这个列表对象，逐一读取 请求删除接口')
            for groupId in range(len(groupIds)):
                body = {
                    'groupId': groupIds[groupId]
                }
                self.apiRequest.note_post(self.host + self.delNoteGroup, userid, sid, body)
                self.apiRequest.note_post(self.host + self.delNoteGroup, userid, sid, body)


