import pinyin
import re

cigar_class_name_cn = [
    '大重九_A', '云烟_a', '娇子_B', '中华_B',
    '利群_a', '黄鹤楼_e', '娇子_F', '云烟_A',
    '黄鹤楼_h', '黄鹤楼_E', '黄金叶_C', '555_a',
    '红塔山_b', '玉溪_A', '娇子_K', '黄鹤楼_A',
    '娇子_E', '天子_a', '天子_A', '王冠_A'
]


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
    cigar_class_name = get_en_name(cigar_class_name_cn)
    print(cigar_class_name)
