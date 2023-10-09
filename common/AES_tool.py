from Crypto.Cipher import AES
import base64

BLOCK_SIZE = AES.block_size


def pad(text):
    return text + (BLOCK_SIZE - len(text.encode()) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(text.encode()) % BLOCK_SIZE)


def encry(text, k, v):
    encryptor = AES.new(k, AES.MODE_CBC, v)  # 声明加密器
    text = pad(text).encode()
    # text = text + (16 - (len(text) + 16) % 16) * '*'  # 数据加密规则，字符串长度必须时16位
    # print(text)
    # 对数据进行加密
    res = encryptor.encrypt(text)
    # 对加密后的数据进行base64解码
    res_base64 = base64.b64encode(res)
    # print(res_base64)
    return res_base64.decode('utf-8')


def decry(text, k, i):
    decryptor = AES.new(k, AES.MODE_CBC, i)  # 声明加密器

    res = base64.b64decode(text.encode('utf-8'))
    res = decryptor.decrypt(res)
    res = res.decode('utf-8').strip("*")
    return res


if __name__ == '__main__':
    key = 'H9n&S@oGohGpV6d7'.encode('utf-8')
    iv = '5150956153345366'.encode('utf-8')
    # print(encry('恭喜', key, iv))
    # print(decry('aiXhXKtVDyR9/L7DJTxhLg==', key, iv))
