import matplotlib.pyplot as plt

# f, axs = plt.subplots(rows, cols)
# f.set_size_inches((cols * 4, rows * 2))  # 1:1 todo
#
# for cat_i in range(cat):  # plt heatmap of each cat
#     ax = axs.flat[cat_i]
#     ax.axis('off')
#     # ax.set_xticks([])
#     # ax.set_yticks([])
#     ax.imshow(hm[img_i][cat_i], cmap=plt.get_cmap('jet'))
#     ax.set_title(classnames[cat_i])
#
# # plt.suptitle('img: {}'.format(img_i))  # big title, so high!
# img_name = '{}_{}.png'.format(basename, img_i)
# plt.savefig(img_name, bbox_inches='tight', pad_inches=0.0)
# print('save', img_name)
