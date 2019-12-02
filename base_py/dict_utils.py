from pprint import pprint


class Struct:
    """
    make a dict a class instance, which can index its keys by `dict.key`, like java oop
    """

    def __init__(self, a_dict):
        for k, v in a_dict.items():
            self.__setattr__(k, v)


def test_attr():
    a = {
        'default_resolution': [384, 1280],
        'num_classes': 3,
        'mean': [0.485, 0.456, 0.406],
        'std': [0.229, 0.224, 0.225],
        'dataset': 'kitti'
    }  # 注意：定义字典时，如果这里多个 , 就变成 tuple 了
    a = Struct(a)
    print(a.dataset)


def get_subdict(ori_dict, sub_keys):
    """
    create a sub dict with sub keys
    """
    sub_dict = {}
    for key in sub_keys:
        sub_dict[key] = ori_dict[key]
    return sub_dict


def get_subdict_v2(ori_dict, sub_keys):
    """
    create a sub dict with sub keys
    """
    return {
        k: v for k, v in ori_dict.items() if k in sub_keys
    }


def test_dict_update():
    a = {
        'a': 1
    }
    a.update({  # actually, update and add
        'a': 2,
        'reg_t': 2,
        'reg_l': 2,
        'reg_b': 2,
        'reg_r': 2}
    )
    pprint(a)


if __name__ == '__main__':
    test_dict_update()
