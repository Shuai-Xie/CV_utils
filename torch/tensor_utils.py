import torch

# a = torch.Tensor([-1, 0, 1])
# print(a)
#
# b = a.sigmoid_()  # in-place, will also change a!
# print(b)  # [0.2689, 0.5000, 0.7311]
# print(a)  # [0.2689, 0.5000, 0.7311]
#
# 查看数据类型
# print(a.dtype)
# print(a.device)

# gpu tensor -> cpu np
# 只要没用 in-place 操作，就不会影响 a
# b = a.detach().cpu().numpy()


# topk
# a = torch.arange(1, 17).view(4, 4)
# print(a)
# topk_scores, topk_inds = torch.topk(a, k=3)  # default dim=-1, 最后1维为基本单位，取出3个 top 值
#
# for i, s in zip(topk_inds, topk_scores):
#     print(i, s)

# expand a tensor, only dim=1 can expand
# ind = torch.arange(1, 4).view(3, 1)
# print(ind.size())
# print(ind)
# dim = 2
# a = ind.unsqueeze(2).expand(ind.size(0), ind.size(1), dim)  # last dim?
# print(a.size())
# print(a)
# b = ind.unsqueeze(2).expand(ind.size(0), dim, dim)
# print(b.size())
# print(b)

# gather
# 设 ind element 所在位置的 k, 则 out[k] = out[ind[k]]
a = torch.Tensor([[1, 2], [3, 4]])  # 2x2
ind = torch.LongTensor([[0], [1]])
b = a.gather(1, index=ind)  # 逐行
print(a)
print(b)
