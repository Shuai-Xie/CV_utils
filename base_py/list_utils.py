import numpy as np
import random

# python 中 None, False, 空字符串”“, 0, 空列表[], 空字典{}, 空元组() 都相当于False
# a = not [0]
# b = not []  # empty
#
# print(a)
# print(b)
#
# a = np.array([(1, 2), (3, 4)]).reshape(1, -1).tolist()  # 转 list
# print(a)


a = [1, 2, 3, 4, 5]

# list 中随机取 n 个元素
print(random.sample(a, 3))

random.shuffle(a)
print(a[:3])
