import matplotlib.pyplot as plt


# 设置 bar color 两种方式
def plt_freq_bar(frequency):
    plt.figure(figsize=(5, 4))
    x, y = range(len(frequency)), frequency

    colors = [[c / 255 for c in label_colors[i + 1]] for i in range(num_classes)]
    plt.bar(x, y, width=0.6, color=colors)

    # 为 bar 设置不同颜色
    # barlist = plt.bar(x, y, width=0.6)
    # for i in range(num_classes):
    #     barlist[i].set_color([c / 255 for c in label_colors[i + 1]])

    # x 轴标签
    plt.xticks(x, range(1, num_classes + 1))
    plt.ylim([0, 0.5])
    # y 轴数字标签
    for a, b in zip(x, y):
        plt.text(a, b + 0.002, '%.3f' % b, ha='center', va='bottom', fontsize=10)

    plt.show()


# 水平 bar
def vis_hist(bins=10):
    affine_ratios = np.load(f'{match_dir}/affine_ratios.npy')
    ys, xs = np.histogram(affine_ratios, bins=bins)

    plt.barh(range(bins), ys, align='center')  # horizontal bar
    plt.xlim([0, 600])
    plt.yticks(range(bins), labels=xs[:-1])
    ax = plt.gca()
    ax.set_xlabel('match_num')
    # https://matplotlib.org/3.3.2/api/text_api.html#matplotlib.text.Text
    ax.set_ylabel('match_ratio', rotation='horizontal')
    ax.yaxis.set_label_coords(-0.2, 0.97)  # 详细设置 label 位置

    for idx, y in enumerate(ys):
        plt.text(y + 5, idx, s=str(y))

    plt.show()
