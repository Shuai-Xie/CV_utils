def cal_set_diff(s1, s2):
    # 使用 set 会忽视 重复元素
    return ''.join(set(s1).symmetric_difference(set(s2)))  # 对称差集，与直接减不同


def cal_str_diff(s1, s2):
    """ 逐位置比较两个 str """
    LEN = max(len(s1), len(s2))
    diff = [1] * LEN
    for idx, (c1, c2) in enumerate(zip(s1, s2)):
        if c1 == c2:
            diff[idx] = 0
    s = s1 if len(s1) > len(s2) else s2
    return ''.join([s[i] for i, elem in enumerate(diff) if elem == 1])


def cmp_list(l1, l2):
    idx = 0
    for idx, (s1, s2) in enumerate(zip(l1, l2)):
        print(idx, cal_str_diff(s1, s2))
    # 不管 l1,l2 那个长，都可以这样
    for i in range(idx + 1, len(l1)):
        print(i, l1[i])
    for i in range(idx + 1, len(l2)):
        print(i, l2[i])


def test_cmp_list():
    strs = 'strs', 's', 'ok', 'man'
    strs2 = 'ssakhfae', 'ssanfklaflafasf'
    cmp_list(strs, strs2)
    cmp_list(strs2, strs)
