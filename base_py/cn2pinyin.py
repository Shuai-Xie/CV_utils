import pinyin
import re

cfg = {
    "name": "Cigar Rotated Box",
    "cats_num": {
        "大重九_A": 73,
        "云烟_a": 29,
        "娇子_B": 22,
        "中华_B": 21,
        "利群_a": 20,
        "黄鹤楼_e": 20,
        "云烟_A": 17,
        "娇子_F": 16,
        "黄鹤楼_h": 16,
        "黄鹤楼_E": 14,
        "黄金叶_C": 13,
        "555_a": 11,
        "红塔山_b": 11,
        "玉溪_A": 11,
        "黄果树_a": 11,
        "娇子_K": 11,
        "黄鹤楼_A": 10,
        "娇子_E": 9,
        "天子_a": 9,
        "天子_A": 8
    },
    "classes": 20,
    "train": 182,
    "valid": 52,
    "test": 26
}


def get_en_name(cn_names):  # 不要拼音
    en_names = []
    for n in cn_names:
        cn = n[:-2]
        # en = pinyin.get(cn)  # 默认有读音
        en = pinyin.get(cn, format='strip', delimiter=' ')  # 无拼音
        en = ''.join([s.capitalize() for s in en.split(' ')])
        en_names.append(n.replace(cn, en))
    return en_names


if __name__ == '__main__':
    cn_names = list(cfg['cats_num'].keys())
    cigar_class_name = get_en_name(cn_names)
    print(cigar_class_name)
