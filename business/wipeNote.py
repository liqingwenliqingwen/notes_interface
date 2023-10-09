from business.apiRequest import ApiRequests
from common.caseLog import step, info
from common.yamlOperator import YamlOperator


class WipeNote:
    apiRequest = ApiRequests()
    envConfig = YamlOperator().env_config()

    host = envConfig['host']
    recycleNotesConfig = YamlOperator.api_data_config('recycleNotes')
    deleteNoteSvr = recycleNotesConfig['deleteNoteSvr']

    pathCleanRecycle = recycleNotesConfig['pathCleanRecycle']

    getRecycleNotes = '/v3/notesvr/user/{}/invalid/startindex/{}/rows/{}/notes'.format('236948373', '0', '50')

    def wipeNote(self, userid, sid):
        """根据用户id软删除便签数据"""

        step('----------------------清空便签数据------------------------------')
        path = '/v3/notesvr/user/{}/home/startindex/{}/rows/{}/notes'.format(userid, 0, 50)

        res = self.apiRequest.note_get(self.host + path, userid, sid, )

        info(f'res.status_code:{res.status_code}')
        info(f'res.json():{res.json()}')
        # step('STEP2:for循环接口结果列表，把所有noteid存储在一个列表上 noteids')
        noteIds = [item['noteId'] for item in res.json()['webNotes']]
        info(f'noteIds列表为:{noteIds}')
        if len(noteIds) == 0:
            info('获取到的列表长度为空，无需清空')
        else:
            # step('STEP3:循环这个列表对象，逐一读取 请求删除接口')
            for noteId in range(len(noteIds)):
                body = {
                    'noteId': noteIds[noteId]
                }

                self.apiRequest.note_post(self.host + self.deleteNoteSvr, userid, sid, body)
        # step('STEP4:获取回收站便签数据')
        res = self.apiRequest.note_get(self.host + self.getRecycleNotes, userid, sid)
        noteIdsRes = [item['noteId'] for item in res.json()['webNotes']]
        info(f'回收站便签数据{noteIdsRes}')
        # step('STEP5:循环清空回收站')
        if len(noteIdsRes) == 0:
            info('回收站的数据为空，无需清空')
        else:
            body = {
                'noteIds': noteIdsRes

            }
            info(f'清空的回收站便签数据有{noteIdsRes}')
            res = self.apiRequest.note_post(self.host + self.pathCleanRecycle, userid, sid, body)
            res = self.apiRequest.note_post(self.host + self.pathCleanRecycle, userid, sid, body)
