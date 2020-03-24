import time
import base64
import hmac


def get_token(key, expire=3600):
    ts_str = str(time.time() + expire)
    ts_byte = ts_str.encode("utf-8")
    sha1_tshexstr = hmac.new(key.encode("utf-8"), ts_byte, 'sha1').hexdigest()
    token = ts_str + ':' + sha1_tshexstr
    b64_token = base64.urlsafe_b64encode(token.encode("utf-8"))
    return b64_token


def out_token(key, token):
    try:
        token_str = base64.urlsafe_b64decode(token).decode("utf-8")
        token_list = token_str.split(':')
        if len(token_list) != 2:
            return False
        ts_str = token_list[0]
        if float(ts_str) < time.time():
            # token expired
            return False
        know_sha1_tsstr = token_list[1]
        sha1 = hmac.new(key.encode('utf-8'), ts_str.encode('utf-8'), 'sha1').hexdigest()
        if sha1 != know_sha1_tsstr:
            return False
        return True
    except Exception as e:
        print(e)
