from hashlib import md5
from io import StringIO


def md5_check(data, md5sum):
    return md5(data.encode()).hexdigest() == md5sum
