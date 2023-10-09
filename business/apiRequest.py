import json

import requests

from common.caseLog import info


class ApiRequests:
    """封装api的请求方法 get ,post,pitch"""

    @staticmethod
    def note_post(url, user_id, sid, body, new_header=None):

        if new_header is not None:
            headers = new_header
        else:
            headers = {
                'Content-Type': 'application/json',
                'X-user-key': str(user_id),
                'Cookie': f'wps_sid={sid}'

            }
        info(f'url:{url}')
        info(f'headers:{json.dumps(headers)}')
        info(f'body:{json.dumps(body)}')
        res = requests.post(url=url, headers=headers, json=body)
        info(f'res.code:{res.status_code}')
        info(f'res.json:{res.json()}')
        return res

    @staticmethod
    def note_get(url, user_id, sid,  new_header=None):
        if new_header is not None:
            headers = new_header
        else:
            headers = {
                'Content-Type': 'application/json',
                'X-user-key': str(user_id),
                'Cookie': f'wps_sid={sid}'
            }
        info(f'url:{url}')
        info(f'headers:{json.dumps(headers)}')
        # info(f'body:{json.dumps(body)}')
        res = requests.get(url=url, headers=headers)
        info(f'res.code:{res.status_code}')
        info(f'res.json:{res.json()}')
        return res

    @staticmethod
    def note_patch(url, user_id, sid, body, new_header=None):
        if new_header is not None:
            headers = new_header
        else:
            headers = {
                'Content-type': 'application/json',
                'X-user-key': str(user_id),
                'Cookie': f'wps_sid={sid}'
            }
        info(f'url:{url}')
        info(f'headers:{json.dumps(headers)}')
        info(f'body:{body}')
        res = requests.patch(url=url, headers=headers, json=body)
        info(f'res.code:{res.status_code}')
        # info(f'res.json:{res.json()}')
        return res
