def test_dict_sort():
    # 字典排序与多标签排序
    a = {
        1: (10, 20, 1),
        10: (10, 1, 2),
        11: (20, 20, 3),
        8: (20, 2, 4),
    }
    print(sorted(a))  # sort the keys
    print(sorted(a.items(), key=lambda t: t[1]))  # sort by values
    print(sorted(a.items(), key=lambda t: t[1][0]))  # sort by v[0]
    print(sorted(a.items(), key=lambda t: t[1][1:]))  # sort by v[1],v[2]
