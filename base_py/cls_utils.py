class A:
    num_classes = 20

    def __init__(self):
        self.name = 'cigar'
        self.data = [x ** 2 for x in range(10)]

    def __len__(self):
        return len(self.data)


class B:
    # 没有用，会调用 A 中 __init__ 方法
    # def __init__(self):
    #     self.name = 'coco'
    #     self.data = [x for x in range(10)]

    def __getitem__(self, index):
        val = self.data[index]
        return val


# 分离 Dataset 类中 __init__ 和 __getitem__ 两个方法
def get_dataset(dataset, task):
    # match dataset and task
    class Dataset(dataset, task):
        pass

    return Dataset


Dataset = get_dataset(A, B)
print(Dataset.num_classes)  # 20
dt = Dataset()
print(dt.name)  # cigar
print(dt.data)

for idx, val in enumerate(dt):
    print(idx, val)
