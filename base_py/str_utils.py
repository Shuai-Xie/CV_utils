import re


def re_split_str():
    a = 'ni2hao3'
    a = re.split(r'[1-4]', a)
    a = ''.join([s.capitalize() for s in a])
    print(a)
