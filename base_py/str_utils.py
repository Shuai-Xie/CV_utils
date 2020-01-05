import re


def re_split_str():
    a = 'ni2hao3'
    a = re.split(r'[1-4]', a)
    a = ''.join([s.capitalize() for s in a])
    print(a)


# get a func in this way
b = globals()['re_split_str']()

print(b)

a = '123233.sdf.png'
a = a.rsplit('.', 1)[0]  # 最多分1次
print(a)

a = {
    '1': 12,
    '2': 12
}

print(sum(a.values()))
print(len(a))
