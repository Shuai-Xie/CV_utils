import torch

a = torch.Tensor([-1, 0, 1])
print(a)

b = a.sigmoid_()  # in-place, will also change a!
print(b)  # [0.2689, 0.5000, 0.7311]
print(a)  # [0.2689, 0.5000, 0.7311]
