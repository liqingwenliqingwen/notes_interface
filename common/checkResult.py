import unittest


class CheckResult(unittest.TestCase):
    def check_out(self, expected, actual):
        """
        可校验点
        1，检查有多余的字段
        2，对齐接口文档字段的类型
        3，确保接口文档所描述的返回字段存在
        4，存在业务属性的字段值的一致性

        :param expected:接口实际返回的结果 dict
        :param actual: 接口期望返回结果 dict
        :return:
        """
        self.assertEqual(len(expected.keys()), len(actual.keys()),
                         msg=f'返回的字段长度和期望的不一致，actual:{actual.keys}'f'expect:{actual.keys}')
        for k, v in expected.items():
            self.assertIn(k, actual.keys(), msg=f'{k}字段不存在于结果中，返回的字段有{actual.keys}')
            if v is None:
                self.assertEqual(v, actual[k], msg=f'{k} 字段不为None, 值为{actual[k]}')
            elif isinstance(v, type):
                self.assertEqual(v, type(actual[k]), msg=f'{k}字段类型错误，期望值{v} 实际值{actual[k]}')
            elif isinstance(v, list):
                for item in range(len(v)):
                    if isinstance(v[item], type):
                        self.assertEqual(v[item], type(actual[k][item]))
                    elif isinstance(v[item], dict):
                        self.check_out(v[item], actual[k][item])
                    else:
                        self.assertEqual(v[item], actual[k][item])
            elif isinstance(v, dict):
                self.check_out(v, actual[k])
            else:
                self.assertEqual(v, actual[k])
